# myTransformer_Spark
利用JPMML-Spark将Spark模型转换为pmml格式
+ 主函数：src/main/pmml/TestPmml.scala
+ 自定义transformer函数：src/main/pmml/Mytransformer.scala
+ JPMML-Spark中注册自定义transformer函数里需要：src/main/pmml/MytransformerConverter.java
+ 将自定义的transformer函数与transformerConverter函数在资源文件里定义一下：src/main/resources/META-INF/sparkml2pmml.properties


# 博客
https://blog.csdn.net/NOT_GUY/article/details/100054852
