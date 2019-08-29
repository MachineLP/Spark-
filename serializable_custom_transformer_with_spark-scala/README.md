

``` 
mvn clean package
```

```
spark-2.4.3-bin-hadoop2.7/bin/spark-submit  --class ml.dmlc.xgboost4j.scala.example.spark.OwnMLlibPipeline --jars /***/scala_workSpace/test/xgboost4j-example_2.11-1.0.0-jar-with-dependencies.jar /***/scala_workSpace/test/xgboost4j-example_2.11-1.0.0.jar /tmp/rd/lp/ownPipelineModel 
```


参考：
scala下扩展spark pipeline：
（1）https://www.oreilly.com/learning/extend-spark-ml-for-your-own-modeltransformer-types
（2）https://n3xtchen.github.io/n3xtchen/scala/2018/03/06/spark-ml-customer-modeltransformer-type 
 (3)  https://docs.databricks.com/spark/latest/mllib/advanced-mllib.html#custom-transformers-and-estimators
 (**) https://qikaigu.com/serializable-custom-transformer-with-spark-2/
spark开发文档：
（1）https://jaceklaskowski.gitbooks.io/mastering-apache-spark/spark-mllib/spark-mllib-transformers.html

