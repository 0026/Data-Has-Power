import findspark
findspark.init()

import pyspark.sql.functions as f
from pyspark import SparkFiles
from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql.session import SparkSession



conf = SparkConf() \
    .setAppName("Quest_001") \
    .setMaster("local") \
    .set("spark.jars", "/opt/bitnami/spark/quest/mysql-connector-java-8.0.29.jar")


sc = SparkContext(conf=conf)
spark = SparkSession(sc)

url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
sc.addFile(url)
df = spark.read.csv("file://"+SparkFiles.get("titanic.csv"), header=True, inferSchema= True)

preprocessed_df = df.select("Survived","Age","Sex","Pclass").withColumn("age_interval", f.expr(
    "CASE WHEN Age<18 THEN 'young_adult' "+
    "WHEN Age<40 THEN 'middle_aged_adult' "+
    "ELSE 'old_adult' "+
    "END"
))

survive_group_with_age_and_sex = preprocessed_df.groupBy("age_interval","Sex").count()


df_count_survive_tmp = preprocessed_df.filter(preprocessed_df["Survived"]==1) \
    .groupBy("age_interval","Sex") \
    .agg(f.count("*").alias("survived_count"))   \
    .join(survive_group_with_age_and_sex, ["Sex","age_interval"])

survive_rate_by_age_and_sex = df_count_survive_tmp.withColumn("survival_rate", f.col("survived_count")/f.col("count")) \
    .select("Sex","age_interval","survival_rate")

survive_rate_by_age_and_sex.write.mode("append").format("jdbc").option("url", "jdbc:mysql://db:3306/mydb") \
	.option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "survive_rate_by_age_and_sex") \
	.option("user", "root") \
    .option("password", "root").save()


survive_group_df=survive_group_with_age_and_sex.groupBy("age_interval") \
    .agg(f.sum("count").alias("sum"))

survive_rate_by_age = df_count_survive_tmp.groupBy("age_interval").agg(f.sum("survived_count").alias("survival_sum")) \
    .join(survive_group_df, "age_interval") \
    .withColumn("survival_rate",f.col("survival_sum")/f.col("sum")) \
    .select("age_interval","survival_rate")

survive_rate_by_age.write.mode("append").format("jdbc").option("url", "jdbc:mysql://db:3306/mydb") \
	.option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "survive_rate_by_age") \
	.option("user", "root") \
    .option("password", "root").save()


count_by_class_and_sex = preprocessed_df.groupBy("Sex","Pclass") \
    .agg(f.count("*").alias("count")) \

survive_rate_by_class_and_sex =preprocessed_df.filter(preprocessed_df["Survived"]==1) \
    .groupBy("Sex","Pclass") \
    .agg(f.count("*").alias("survived_count")) \
    .join(count_by_class_and_sex,["Sex","Pclass"]) \
    .withColumn("survival_rate",f.col("survived_count")/f.col("count")) \
    .select("Sex","Pclass","survival_rate")

survive_rate_by_class_and_sex.write.mode("append").format("jdbc").option("url", "jdbc:mysql://db:3306/mydb") \
	.option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "survive_rate_by_class_and_sex") \
	.option("user", "root") \
    .option("password", "root").save()

