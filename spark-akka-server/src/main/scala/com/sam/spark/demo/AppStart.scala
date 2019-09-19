package com.sam.spark.demo


import com.sam.spark.demo.akka.AkkaConfig
import com.sam.spark.demo.data.config.SparkConfig
import scala.concurrent.duration.Duration
import scala.concurrent.Await
import java.util.concurrent.TimeUnit

object AppStart {
  def main(args: Array[String]): Unit = {
    SparkConfig
    println ("11111111111111111111111")
    AkkaConfig
  }
}

