

``` 
mvn clean package
```

```
spark-2.4.3-bin-hadoop2.7/bin/spark-submit  --class ml.dmlc.xgboost4j.scala.example.spark.OwnMLlibPipeline --jars /***/scala_workSpace/test/xgboost4j-example_2.11-1.0.0-jar-with-dependencies.jar /***/scala_workSpace/test/xgboost4j-example_2.11-1.0.0.jar /tmp/rd/lp/ownPipelineModel 
```

