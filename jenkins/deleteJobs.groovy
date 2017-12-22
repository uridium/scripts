import jenkins.model.*

def jobsToDelete = Jenkins.instance.items.findAll {
    it.name =~ /regexp/
}

jobsToDelete.each {
    print "${it.name}:  "
    it.delete()
    println "deleted"
}

println "\n${jobsToDelete.size()} elements deleted"
