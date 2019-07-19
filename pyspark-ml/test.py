import os
import sys

#下面这些目录都是你自己机器的Spark安装目录和Java安装目录
os.environ['SPARK_HOME'] = "/Users/***/spark-2.4.3-bin-hadoop2.7/"

sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/bin")
sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/python")
sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/python/pyspark")
sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/python/lib")
sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/python/lib/pyspark.zip")
sys.path.append("/Users/***/spark-2.4.3-bin-hadoop2.7/lib/py4j-0.9-src.zip")
# sys.path.append("/Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk/Contents/Home")
os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home"

from pyspark import SparkContext
from pyspark import SparkConf


sc = SparkContext("local","testing")

print (sc.version)
print ('hello world!!')


import pyspark.sql.types as typ
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

labels = [
    ('INFANT_ALIVE_AT_REPORT', typ.IntegerType()),
    ('BIRTH_PLACE', typ.StringType()),
    ('MOTHER_AGE_YEARS', typ.IntegerType()),
    ('FATHER_COMBINED_AGE', typ.IntegerType()),
    ('CIG_BEFORE', typ.IntegerType()),
    ('CIG_1_TRI', typ.IntegerType()),
    ('CIG_2_TRI', typ.IntegerType()),
    ('CIG_3_TRI', typ.IntegerType()),
    ('MOTHER_HEIGHT_IN', typ.IntegerType()),
    ('MOTHER_PRE_WEIGHT', typ.IntegerType()),
    ('MOTHER_DELIVERY_WEIGHT', typ.IntegerType()),
    ('MOTHER_WEIGHT_GAIN', typ.IntegerType()),
    ('DIABETES_PRE', typ.IntegerType()),
    ('DIABETES_GEST', typ.IntegerType()),
    ('HYP_TENS_PRE', typ.IntegerType()),
    ('HYP_TENS_GEST', typ.IntegerType()),
    ('PREV_BIRTH_PRETERM', typ.IntegerType())
]

schema = typ.StructType([
    typ.StructField(e[0], e[1], False) for e in labels
])

births = spark.read.csv('births_transformed.csv.gz', 
                        header=True, 
                        schema=schema)


print ('births>>>', births)


import pyspark.ml.feature as ft

births = births \
    .withColumn(       'BIRTH_PLACE_INT', 
                births['BIRTH_PLACE'] \
                    .cast(typ.IntegerType()))
# 此处打印出来还是string
print ('births>>>', births)

# 构建第一个转换器
encoder = ft.OneHotEncoder(
    inputCol='BIRTH_PLACE_INT', 
    outputCol='BIRTH_PLACE_VEC')

print ('encoder>>>', encoder)
print ('encoder.getOutputCol():', encoder.getOutputCol())

import pyspark as spark

# 将所有的特征整和到一起
featuresCreator = ft.VectorAssembler(
    inputCols=[
        col[0] 
        for col 
        in labels[2:]] + \
    [encoder.getOutputCol()], 
    outputCol='features'
)

print ('featuresCreator:', featuresCreator)

# 创建评估器
import pyspark.ml.classification as cl
logistic = cl.LogisticRegression(
    maxIter=10, 
    regParam=0.01, 
    labelCol='INFANT_ALIVE_AT_REPORT')
print ('logistic:', logistic)


# 创建一个管道
from pyspark.ml import Pipeline

pipeline = Pipeline(stages=[
        encoder, 
        featuresCreator, 
        logistic
    ])

# fit 
births_train, births_test = births \
    .randomSplit([0.7, 0.3], seed=666)

print ('births_train', births_train)
print ( 'births_test', births_test )

# 运行管道，评估模型。
model = pipeline.fit(births_train)
test_model = model.transform(births_test)

print ('test_model:', test_model)


test_model.take(1)

print ('test_model.take(1):', test_model.take(1))


# 评估模型性能
import pyspark.ml.evaluation as ev

evaluator = ev.BinaryClassificationEvaluator(
    rawPredictionCol='probability', 
    labelCol='INFANT_ALIVE_AT_REPORT')

print(evaluator.evaluate(test_model, 
     {evaluator.metricName: 'areaUnderROC'}))
print(evaluator.evaluate(test_model, {evaluator.metricName: 'areaUnderPR'}))


# 保存模型
pipelinePath = './infant_oneHotEncoder_Logistic_Pipeline'
pipeline.write().overwrite().save(pipelinePath)

# 在之前模型上继续训练
loadedPipeline = Pipeline.load(pipelinePath)
loadedPipeline.fit(births_train).transform(births_test).take(1)


# 保存整个模型
from pyspark.ml import PipelineModel

modelPath = './infant_oneHotEncoder_Logistic_PipelineModel'
model.write().overwrite().save(modelPath)

loadedPipelineModel = PipelineModel.load(modelPath)
test_loadedModel = loadedPipelineModel.transform(births_test)
print ('test_loadedModel:', test_loadedModel)


# 超参调优
import pyspark.ml.tuning as tune

# 使用网格搜索
logistic = cl.LogisticRegression(
    labelCol='INFANT_ALIVE_AT_REPORT')

grid = tune.ParamGridBuilder() \
    .addGrid(logistic.maxIter,  
             [2, 10, 50]) \
    .addGrid(logistic.regParam, 
             [0.01, 0.05, 0.3]) \
    .build()


evaluator = ev.BinaryClassificationEvaluator(
    rawPredictionCol='probability', 
    labelCol='INFANT_ALIVE_AT_REPORT')



cv = tune.CrossValidator(
    estimator=logistic, 
    estimatorParamMaps=grid, 
    evaluator=evaluator
)


# 创建转换通道
pipeline = Pipeline(stages=[encoder,featuresCreator])
data_transformer = pipeline.fit(births_train)

# fit
cvModel = cv.fit(data_transformer.transform(births_train))

data_train = data_transformer \
    .transform(births_test)
results = cvModel.transform(data_train)

print(evaluator.evaluate(results, 
     {evaluator.metricName: 'areaUnderROC'}))
print(evaluator.evaluate(results, 
     {evaluator.metricName: 'areaUnderPR'}))



# Train-Validation splitting
selector = ft.ChiSqSelector(
    numTopFeatures=5, 
    featuresCol=featuresCreator.getOutputCol(), 
    outputCol='selectedFeatures',
    labelCol='INFANT_ALIVE_AT_REPORT'
)

logistic = cl.LogisticRegression(
    labelCol='INFANT_ALIVE_AT_REPORT',
    featuresCol='selectedFeatures'
)

pipeline = Pipeline(stages=[encoder,featuresCreator,selector])
data_transformer = pipeline.fit(births_train)


tvs = tune.TrainValidationSplit(
    estimator=logistic, 
    estimatorParamMaps=grid, 
    evaluator=evaluator
)


tvsModel = tvs.fit(
    data_transformer \
        .transform(births_train)
)

data_train = data_transformer \
    .transform(births_test)
results = tvsModel.transform(data_train)

print(evaluator.evaluate(results, 
     {evaluator.metricName: 'areaUnderROC'}))
print(evaluator.evaluate(results, 
     {evaluator.metricName: 'areaUnderPR'}))






