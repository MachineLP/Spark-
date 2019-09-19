package com.sam.spark.demo.akka

import akka.actor.Actor
import org.slf4j.LoggerFactory
import com.sam.spark.demo.data.service.DataService
import com.sam.spark.demo.akka.msg.TextMessage
import java.util.UUID
import scala.collection.mutable.ArrayBuffer

class Worker extends Actor {
  
  val dataService = new DataService()
  
  def receive = {
    case x: ArrayBuffer[String] => {
      val tm = new TextMessage()
      tm.msg = dataService.handler(x)
      sender ! tm
    }
  }
}