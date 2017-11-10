import jenkins.model.*

def jobsToDelete = Jenkins.instance.items.findAll { job ->
    job.name =~ /regexp/
}

jobsToDelete.each { job ->
    print "${job.name}:  "
    job.delete()
    println "Deleted"
}
