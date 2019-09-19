package com.sam.spark.demo.data.config

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf

object SparkConfig {
  val conf = new SparkConf().setAppName("testSpark")
  val sc = new SparkContext(conf)
}

