
import akka.actor._
import akka.event.Logging

class ClientActor(serverPath: String) extends Actor {
  val log = Logging(context.system, this)
  val serverActor = context.actorSelection(serverPath)

  def receive = {
    case msg: String =>
        log.info(s"ClientActor received message '$msg'")
        serverActor ! 10000L
  }
}
