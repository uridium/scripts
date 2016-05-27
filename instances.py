#!/usr/bin/python

import boto.ec2
import boto.ec2.elb

LINE_OUTPUT_FORMAT = '%-16s %-12s %-12s %-16s %-16s %-40s %-76s %-36s %40s'

AWS_REGION = "eu-west-1"
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""


class Instance(object):
    def __init__(
            self, id, state, type, private_ip, public_ip, name, sg_name,
            asg_name, elb, instance_health):
        self.id = id
        self.state = state
        self.type = type
        self.private_ip = private_ip
        self.public_ip = public_ip
        self.name = name
        self.sg_name = sg_name
        self.asg_name = asg_name
        self.elb = elb
        self.instance_health = instance_health

    def __str__(self):
        "State", "Id", "Type", "Private IP", "Public IP", "Name", "SG", "ASG", "ELB"
        if self.elb:
            elb_part = '(%s) %s' % (
                self.instance_health.state if self.instance_health else '-',
                self.elb.name if self.elb else '-'
            )
        else:
            elb_part = '-'
        output = LINE_OUTPUT_FORMAT % (
            self.state,
            self.id,
            self.type,
            self.private_ip,
            self.public_ip,
            self.name,
            self.sg_name,
            self.asg_name,
            elb_part,
        )
        return output

    @classmethod
    def create_from_boto_instance(cls, instance, elb_for_instance, instance_health):
        sg_name = []
        for sg in instance.groups:
            sg_name.append(sg.name)
        return cls(
            id=instance.id,
            state=instance.state,
            type=instance.instance_type,
            private_ip=instance.private_ip_address,
            public_ip=instance.ip_address,
            sg_name=str(sg_name)[1:-1].replace("',", ",", 15).replace('u\'', '', 15).replace('\'', '', 15),
            name=instance.tags.get('Name'),
            asg_name=instance.tags.get('aws:autoscaling:groupName'),
            elb=elb_for_instance,
            instance_health=instance_health,
        )

    def __lt__(self, other):
        asg_name = self.asg_name.lower() if self.asg_name else None
        other_asg_name = other.asg_name.lower() if other.asg_name else None

        name = self.name.lower() if self.name else None
        other_name = other.name.lower() if other.name else None
        if asg_name == other_asg_name:
            return name < other_name
        if asg_name < other_asg_name:
            return True
        return False


def get_instances():
    ec2_connection = get_ec2_connection()
    instances = ec2_connection.get_only_instances()
    elb_connection = get_elb_connection()

    instances_elb = {}
    instances_elb_health = {}

    for elb in elb_connection.get_all_load_balancers():
        for instance in elb.instances:
            instances_elb[instance.id] = elb
        for instance_health in elb_connection.describe_instance_health(elb.name):
            instances_elb_health[instance_health.instance_id] = instance_health

    for instance in instances:
        elb_for_instance = instances_elb.get(instance.id)
        instance_health = instances_elb_health.get(instance.id)
        yield Instance.create_from_boto_instance(
            instance, elb_for_instance, instance_health)


def get_ec2_connection():
    return boto.ec2.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def get_elb_connection():
    return boto.ec2.elb.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def print_legend():
    print '-' * 272
    print LINE_OUTPUT_FORMAT % (
        'State',
        'Id',
        'Type',
        'Private IP',
        'Public IP',
        'Name',
        'SG',
        'ASG',
        'ELB',
    )
    print '-' * 272


def main():
    print_legend()
    for instance in sorted(get_instances(), reverse=True):
        print instance
    print_legend()


if __name__ == '__main__':
    main()
