/*
  * @Author: guoyilin
  * @Date: 2019-08-20
  * @Time: 10:26    
  */

//import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.ml.feature._
import org.apache.spark.sql.SaveMode
//import org.apache.spark.ml.linalg.Vectors
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.mllib.linalg._
import org.apache.spark.sql.DataFrameWriter
import org.apache.spark.ml.{Pipeline, PipelineModel, PipelineStage}
import org.apache.spark.ml.classification.RandomForestClassifier
import org.apache.spark.ml.classification.RandomForestClassificationModel
import org.jpmml.model.JAXBUtil
import org.jpmml.sparkml.PMMLBuilder
import org.dmg.pmml.PMML
import javax.xml.transform.stream.StreamResult
import java.io.FileOutputStream
import org.apache.spark.ml.linalg.DenseVector

import org.apache.spark.ml.feature.Mytransformer
import org.jpmml.sparkml.feature.MytransformerConverter

object TestPmml extends App{
//        val mytransformer = new Mytransformer()
    println("666666")
    val spark = SparkSession.builder().master("local").appName("TestPmml").getOrCreate()

    //val label: Map[String, Double] = Map("Iris-setosa"->0.0,
    //                "Iris-versicolor"->1.0,
    //                "Iris-virginica"->2.0)

    val str2Int: Map[String, Double] = Map(
        "Iris-setosa" -> 0.0,
        "Iris-versicolor" -> 1.0,
        "Iris-virginica" -> 2.0
    )
    var str2double = (x: String) => str2Int(x)
    var myFun = udf(str2double)
    val data = spark.read.textFile("D:\\gyl\\scalaProgram\\PMML\\iris1.txt").toDF()
        .withColumn("splitcol", split(col("value"), ","))
        .select(
            col("splitcol").getItem(0).as("sepal_length"),
            col("splitcol").getItem(1).as("sepal_width"),
            col("splitcol").getItem(2).as("petal_length"),
            col("splitcol").getItem(3).as("petal_width"),
            col("splitcol").getItem(4).as("label")
        )
        .withColumn("label", myFun(col("label")))
        .select(
            col("sepal_length").cast(DoubleType),
            col("sepal_width").cast(DoubleType),
            col("petal_length").cast(DoubleType),
            col("petal_width").cast(DoubleType),
            col("label").cast(DoubleType)
        )

    //    val data2=data("sepal_length").apply(double2vectors)
    val data1 = data.na.drop()
    println("data: " + data1.count().toString)
    val schema = data1.schema
    println("data1 schema: " + schema)


    //    data2.write.mode("overwrite").parquet("D:\\\\gyl\\\\scalaProgram\\PMML\\data1.parquet")
    //    data2.write.format(\"parquet\").save(\"D:\\\\gyl\\\\scalaProgram\\PMML\\data1.parquet")
    // load parquet to dataframe
    //    val data1 = spark.read.load("D:\\gyl\\scalaProgram\\PMML\\data1.parquet")

    val features: Array[String] = Array("sepal_length", "sepal_width", "petal_length", "petal_width")
    //    // merge multi-feature to vector features
    val assembler: VectorAssembler = new VectorAssembler().setInputCols(features).setOutputCol("features")
    val data2 = assembler.transform(data1)
    println("data2 schema: " + data2.schema)
    println("assembler transform class: "+assembler.getClass )


    // convert features vector-data to string
    val convertFunction = (x: DenseVector) => {
        x.toString
    }
    val convertUDF = udf(convertFunction)
    val newdata = data2.withColumn("features", convertUDF(col("features")))
    newdata.write.mode(SaveMode.Overwrite).format("parquet").save("D:\\gyl\\scalaProgram\\PMML\\data1.parquet")

    // convert features string to vector-data
    var string2vector = (x: String) => {
        var length = x.length()
        var a = x.substring(1, length - 1).split(",").map(i => i.toDouble)
        Vectors.dense(a)
    }
    var str2vec = udf(string2vector)
    val newdata1 = spark.read.load("D:\\gyl\\scalaProgram\\PMML\\data1.parquet")
    println("newdata1: " + newdata1.schema)
//        val newdata2 = newdata1.withColumn("features", str2vec(col("features")))
//        println(newdata2.schema)

    val mytransformer = new Mytransformer().setInputCol(features).setOutputCol("features")
    println(mytransformer.getClass)

    val rf = new RandomForestClassifier()
        .setLabelCol("label")
        .setFeaturesCol("features")
        .setMaxDepth(8)
        .setNumTrees(30)
        .setSeed(1234)
        .setMinInfoGain(0)
        .setMinInstancesPerNode(1)

    val pipeline = new Pipeline().setStages(Array(mytransformer, rf))
    //
    val pipelineModel = pipeline.fit(newdata1)

    //////    val pre = pipelineModel.transform(data)
    ////    //val prediction = pre.select("prediction")
    //////    import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
    //////    val evaluator = new MulticlassClassificationEvaluator()
    //////        .setLabelCol("label").setMetricName("accuracy").setPredictionCol("prediction")
    //////    val acc = evaluator.evaluate(pre)
    //////    print("acc "+acc)
    ////
    ////
    val pmml = new PMMLBuilder(newdata1.schema, pipelineModel).build()
    val targetFile = "D:\\gyl\\scalaProgram\\PMML\\pipemodel.pmml"
    val fis: FileOutputStream = new FileOutputStream(targetFile)
    val fout: StreamResult = new StreamResult(fis)
    JAXBUtil.marshalPMML(pmml, fout)
    println("pipelineModel success......")

}