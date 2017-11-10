import jenkins.model.*

def queue = Jenkins.instance.queue

println "Number of items in Build Queue: ${queue.items.length}\n"

queue.items.each {
    println it.task.name
}

queue.clear()
println "\nQueue cleared"
