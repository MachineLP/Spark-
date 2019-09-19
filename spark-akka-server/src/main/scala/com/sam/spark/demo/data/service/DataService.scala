package com.sam.spark.demo.data.service

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import com.sam.spark.demo.data.config.SparkConfig
import scala.collection.mutable.ArrayBuffer


class DataService {

  def handler(list: ArrayBuffer[String]) : String = {
    val array = SparkConfig.sc.parallelize(list).max()
    array
  }
}