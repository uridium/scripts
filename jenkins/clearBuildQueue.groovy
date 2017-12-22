import jenkins.model.*

def elements = Jenkins.instance.queue

def jobsToClear = elements.items.findAll {
    it.task.name =~ /regexp/
}

jobsToClear.each {
    print "${it.task.name}:  "
    elements.cancel(it.task)
    println "cleared"
}

println "\n${jobsToClear.size()} elements cleared"
