package com.sam.spark.demo.akka

import java.io.File
import akka.actor.ActorSystem
import akka.actor.Props
import com.typesafe.config.ConfigFactory
import com.sam.spark.demo.akka.Worker

import akka.http.scaladsl.server.{HttpApp, Route}
import akka.util.Timeout
import scala.concurrent.{ExecutionContext, Future}

object AkkaConfig {

  // 准备配置
  // s""" |akka.actor.provider = "akka.remote.RemoteActorRefProvider" |akka.remote.netty.tcp.hostname = "$host" |akka.remote.netty.tcp.port = "$port" """.stripMargin
  // val config = ConfigFactory.parseString(configStr)

  // val system = ActorSystem("ReactiveEnterprise", config) //,ConfigFactory.load().getConfig("serverSystem"))
  // val system = ActorSystem( "ReactiveEnterprise", ConfigFactory.load("resources/application.conf").getConfig("serverSystem") )

  println ("222222222222222222")
  //val conf = ConfigFactory.parseFile(new File("src/main/resources/application.conf"))
  //println ("333333333333333333")
  //println ( conf )
  val system = ActorSystem( "ReactiveEnterprise", ConfigFactory.load()) //, ConfigFactory.load( conf ).getConfig("serverSystem") )

  val workerRef = system.actorOf(Props[Worker], "worker")
}
