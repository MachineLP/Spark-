import com.typesafe.config.ConfigFactory
import akka.actor._
import akka.remote.RemoteScope
import akka.util._
import java.io.File

import java.util.concurrent.TimeUnit

import scala.concurrent._
import scala.concurrent.duration._

object ClientApp {
  def main(args: Array[String]): Unit = {

    println ( "222222222222222" )

    val configFile = getClass.getClassLoader.getResource("client.conf").getFile
    val config = ConfigFactory.parseFile(new File(configFile))
    val system = ActorSystem("RemoteSystem" , config)
    // val system = ActorSystem("LocalSystem", ConfigFactory.load("client"))

    println ( "3333333333333" )
    
    // get the remote actor via the server actor system's address
    val serverAddress = AddressFromURIString("akka.tcp://ServerActorSystem@127.0.0.1:2552")
    val actor = system.actorOf(Props[ServerActor].withDeploy(Deploy(scope = RemoteScope(serverAddress))))
    
    println ( "44444444444444" )
    // invoke the remote actor via a client actor.
    // val remotePath = "akka.tcp://ServerActorSystem@127.0.0.1:2552/user/serverActor"
    // val actor = system.actorOf(Props(classOf[ClientActor], remotePath), "clientActor")

    buildReaper(system, actor)

    // tell
    actor ! 10000L
    
    waitShutdown(system, actor)
  }

  private def buildReaper(system: ActorSystem, actor: ActorRef): Unit = {
    import Reaper._
    val reaper = system.actorOf(Props(classOf[ProductionReaper]))
    
    // Watch the action
    reaper ! WatchMe(actor)
  }

  private def waitShutdown(system: ActorSystem, actor: ActorRef): Unit = {
    // trigger the shutdown operation in ProductionReaper
    system.stop(actor)
    
    // wait to shutdown
    Await.result(system.whenTerminated, 60.seconds)
  }
}