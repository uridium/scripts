def elements = org.jenkins.plugins.lockableresources.LockableResourcesManager.get()

def locksToDelete = elements.getResources().findAll {
    it.name =~ /regexp/
}

locksToDelete.each {
    print "${it.name}:  "
    elements.getResources().remove(it)
    println "deleted"
}

println "\n${locksToDelete.size()} elements deleted"
