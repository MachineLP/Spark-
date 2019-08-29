/*
-------------------------------------------------
   Description :  Serializable Custom Transformer with Spark 2.0 (Scala)
   Author :       liupeng
   Date :         2019/08/29
-------------------------------------------------
 */

package ml.dmlc.xgboost4j.scala.example.spark

import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.PipelineStage
import org.apache.spark.ml.Transformer
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.LabeledPoint
import org.apache.spark.ml.linalg.DenseVector
import org.apache.spark.ml.linalg.Vectors
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.sql.Dataset
import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.catalyst.encoders.RowEncoder
import org.apache.spark.sql.catalyst.expressions.GenericRowWithSchema
import org.apache.spark.sql.types.StructType



import org.apache.spark.ml.Transformer
import org.apache.spark.ml.param.{ Param, ParamMap }
import org.apache.spark.ml.util.{ DefaultParamsReadable, DefaultParamsWritable, Identifiable }
import org.apache.spark.sql.{ DataFrame, Dataset }
import org.apache.spark.sql.types.StructType


class ColRenameTransformer(override val uid: String) extends Transformer with DefaultParamsWritable {

  def this() = this(Identifiable.randomUID("ColRenameTransformer"))
  def setInputCol(value: String): this.type = set(inputCol, value)
  def setOutputCol(value: String): this.type = set(outputCol, value)
  def getOutputCol: String = getOrDefault(outputCol)

  val inputCol = new Param[String](this, "inputCol", "input column")
  val outputCol = new Param[String](this, "outputCol", "output column")

  override def transform(dataset: Dataset[_]): DataFrame = {
    val outCol = extractParamMap.getOrElse(outputCol, "output")
    val inCol = extractParamMap.getOrElse(inputCol, "input")

    dataset.drop(outCol).withColumnRenamed(inCol, outCol)
  }

  override def copy(extra: ParamMap): ColRenameTransformer = defaultCopy(extra)
  override def transformSchema(schema: StructType): StructType = schema
}

object ColRenameTransformer extends DefaultParamsReadable[ColRenameTransformer] {
  override def load(path: String): ColRenameTransformer = super.load(path)
}


object OwnMLlibPipeline {

  def main(args: Array[String]): Unit = {

    val pipelineModelPath = args(0)

    val spark = SparkSession.builder().getOrCreate()
    val data = spark.createDataFrame(Seq(
                     ("hi,there", 1),
                     ("a,b,c", 2),
                     ("no", 3) )).toDF("myInputCol", "id")
    data.show(false)
    val myTransformer = new ColRenameTransformer().setInputCol( "id" ).setOutputCol( "lpid" )
    println(s"Original data has ${data.count()} rows.")
    // val output = myTransformer.transform(data)
    // println(s"Output data has ${output.count()} rows.")
    // output.show(false)
  
    val pipeline = new Pipeline().setStages(Array( myTransformer ))
    val model = pipeline.fit(data)
    // ML pipeline persistence
    model.write.overwrite().save(pipelineModelPath)
    // Load a saved model and serving
    val model2 = PipelineModel.load(pipelineModelPath)
    model2.transform(data).show(false)
  }
}




