#!/bin/bash

function usage {
    echo "Usage: $0 [-h] [-u <username>] [-p <password>] [-i <dockerimage>] [-s <sourcetag>] [-n <newtag>]"
    exit 1
} >&2

while getopts "hu:p:i:s:n:" opt; do
    case $opt in
        h)
            echo "Add a new tag on docker hub without pulling an image"
            echo
            echo "Options:"
            echo " -h"
            echo "   Print detailed help screen"
            echo " -u Username"
            echo "   Docker registry username"
            echo " -p Password"
            echo "   Docker registry password"
            echo " -i Image"
            echo "   Docker image in the 'organization/name' format"
            echo " -s SourceTag"
            echo "   Docker image tag you want to add a new tag to"
            echo " -n NewTag"
            echo "   New docker image tag"
            echo
            echo "Example:"
            echo " $0 -u username -p password -i uridium/latex -s latest -n 1.0"
            echo
            usage
            ;;
        u)
            username=${OPTARG}
            ;;
        p)
            password=${OPTARG}
            ;;
        i)
            if [[ "${OPTARG}" =~ "/" ]]; then
                dockerimage=${OPTARG}
            else
                echo "Docker image must be in the 'organization/name' format!" >&2
                exit 1
            fi
            ;;
        s)
            sourcetag=${OPTARG}
            ;;
        n)
            newtag=${OPTARG}
            ;;
        \?)
            usage
            ;;
    esac >&2

done

if [[ -z "${username}" ]] || [[ -z "${password}" ]] || [[ -z "${dockerimage}" ]] || [[ -z "${sourcetag}" ]] || [[ -z "${newtag}" ]]; then
    usage
fi

manifest="application/vnd.docker.distribution.manifest.v2+json"

token=$(curl -s -u "${username}:${password}" \
    "https://auth.docker.io/token?scope=repository:${dockerimage}:pull,push&service=registry.docker.io" \
    | jq -r '.token')

curl -s -S \
    -H "Authorization: Bearer ${token}" \
    -H "Accept: ${manifest}" \
    "https://registry-1.docker.io/v2/${dockerimage}/manifests/${sourcetag}" \
    | curl -s -S \
        -i \
        -X PUT \
        -d @- \
        -H "Authorization: Bearer ${token}" \
        -H "Content-type: ${manifest}" \
        "https://registry-1.docker.io/v2/${dockerimage}/manifests/${newtag}"
