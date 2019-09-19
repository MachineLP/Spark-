import akka.actor.Actor
import akka.actor.Props
import akka.event.Logging

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

class ServerActor extends Actor {
  val log = Logging(context.system, this)

  def receive = {
    case n: Long =>
        squareSum(n)
  }

  private def squareSum(n: Long): Long = {
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)

    val squareSum = sc.parallelize(1L until n).map { i => 
      i * i
    }.reduce(_ + _)

    log.info(s"============== The square sum of $n is $squareSum. ==============")

    squareSum
  }
}