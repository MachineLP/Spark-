
## 基于akka的spark server

### server start
```
/di_software/emr-package/spark-2.4.3-bin-hadoop2.7/bin/spark-submit --master local --class ServerApp --jars  /home/rd/machinelp/test_akka/qdspark-1.0.0-jar-with-dependencies.jar /home/rd/machinelp/test_akka/qdspark-1.0.0.jar
```

### client start
```
/di_software/emr-package/spark-2.4.3-bin-hadoop2.7/bin/spark-submit --master local --class ClientApp --jars  /home/rd/machinelp/test_akka/qdspark-1.0.0-jar-with-dependencies.jar /home/rd/machinelp/test_akka/qdspark-1.0.0.jar
```
