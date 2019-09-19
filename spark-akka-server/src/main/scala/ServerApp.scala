import scala.concurrent.duration._
import com.typesafe.config.ConfigFactory
import akka.actor.ActorSystem
import akka.actor.Props
import java.io.File
import akka.actor._

object ServerApp {
  def main(args: Array[String]): Unit = {
    val configFile = getClass.getClassLoader.getResource("application.conf").getFile
    val config = ConfigFactory.parseFile(new File(configFile))
    val system = ActorSystem("RemoteSystem" , config)
    println ( "11111111111111111" )
    // val system = ActorSystem("ServerActorSystem", ConfigFactory.load("application") )
    val actor = system.actorOf(Props[ServerActor], name = "serverActor")
  }
}