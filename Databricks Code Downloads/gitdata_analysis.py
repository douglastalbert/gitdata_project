# Databricks notebook source
import pyspark.sql
from pyspark.sql.types import StructField, StringType, IntegerType, StructType, ArrayType, BooleanType, TimestampType, DataType

dbutils.widgets.text("Repository", "REPOSITORY")
getArgument("Repository")
df_schema=StructField('repo',StringType(),True),StructField('user',StringType(),True),StructField('state',StringType(),True),StructField('url',StringType(),True),StructField('created',TimestampType(),True),StructField('updated',TimestampType(),True),StructField('closed',TimestampType(),True),StructField('assignees',ArrayType(StringType()),True),StructField('reviewers',ArrayType(StringType()),True),StructField('review_teams',ArrayType(StringType()),True),StructField('labels',ArrayType(StringType()),True),StructField('branch',StringType(),True),StructField('merged',BooleanType(),True),StructField('comments',IntegerType(),True),StructField('review_comments',IntegerType(),True),StructField('commits',IntegerType(),True),StructField('additions',IntegerType(),True),StructField('deletions',IntegerType(),True),StructField('changed_files',IntegerType(),True)

df_schema = StructType(fields=df_schema)

raw = spark.read.json('FileStore/tables/output.json',schema=df_schema)
display(raw.filter(raw.state=='open'))
# raw.describe().show()

# COMMAND ----------

#The user and repository with metrics to be charted
# USER_FOR_METRICS = getArgument("User")
REPOSITORY_FOR_METRICS = getArgument("Repository")

# COMMAND ----------

from pyspark.sql import functions, Row, Column
raw = raw.withColumn('closed', functions.when(raw.closed.isNull(), functions.current_timestamp()).otherwise(raw.closed))
duration = functions.unix_timestamp(raw.closed) - functions.unix_timestamp(raw.created)

processed_data = raw.withColumn('age', duration)
# processed_data.show()
# print(processed_data.count())
# display(processed_data)

# COMMAND ----------

#Finds number of rows in which url (id) appears, generating count for number of review teams
df1 = raw.withColumn('exploded_review_team',functions.explode(raw.review_teams))

num_teams = df1.groupBy(df1.url).count()
num_teams = num_teams.withColumnRenamed('count','team_count').withColumnRenamed('url','URL')

processed_data = processed_data.join(num_teams, processed_data.url==num_teams.URL, "left")
# display(processed_data)
#Not finished

# COMMAND ----------

#Displays Open PR Ages Chart 
chart1_dataframe = processed_data.withColumn("age_in_days", processed_data.age/86400)
# chart1_dataframe = chart1_dataframe.filter(chart1_dataframe.age_in_days<=30)
chart1_dataframe = chart1_dataframe.filter(chart1_dataframe.repo == REPOSITORY_FOR_METRICS)
chart1_dataframe = chart1_dataframe.sort(chart1_dataframe.user.desc())
display(chart1_dataframe.filter(chart1_dataframe.state=='open'))

# COMMAND ----------

chart2_dataframe = chart1_dataframe.withColumn('seconds_since_creation', functions.unix_timestamp(functions.current_timestamp()) - functions.unix_timestamp(chart1_dataframe.created))
chart2_dataframe = chart2_dataframe.withColumn('weeks_since_creation', chart2_dataframe.seconds_since_creation / 604800)
chart2_dataframe = chart2_dataframe.withColumn('weeks_ago',chart2_dataframe.weeks_since_creation.cast(IntegerType()))
chart2_dataframe = chart2_dataframe.sort(chart2_dataframe.weeks_ago.desc())
display(chart2_dataframe)

# COMMAND ----------

# #Create line graph for commits by week for user
# chart2_dataframe = chart1_dataframe.withColumn('seconds_since_creation', functions.unix_timestamp(functions.current_timestamp()) - functions.unix_timestamp(chart1_dataframe.created))
# chart2_dataframe = chart2_dataframe.withColumn('weeks_since_creation', chart2_dataframe.seconds_since_creation / 604800)
# chart2_dataframe = chart2_dataframe.withColumn('weeks_ago',chart2_dataframe.weeks_since_creation.cast(IntegerType()))

# chart2_dataframe = chart2_dataframe.filter(chart2_dataframe.weeks_ago < 14)
# chart2_dataframe = chart2_dataframe.sort(chart2_dataframe.weeks_ago.desc())
# display(chart2_dataframe.filter(chart2_dataframe.user == USER_FOR_METRICS))

# COMMAND ----------

# display(chart2_dataframe.filter(chart2_dataframe.user == USER_FOR_METRICS))

# COMMAND ----------

#Create histogram for pr close time by repository
chart3_dataframe = chart1_dataframe.filter(chart1_dataframe.state == 'closed').filter(chart1_dataframe.repo == REPOSITORY_FOR_METRICS)
display(chart3_dataframe.withColumnRenamed('age_in_days','days_before_closed'))

# COMMAND ----------

# display(chart1_dataframe.sort(chart1_dataframe.commits.desc()))
chart4_dataframe = chart1_dataframe.groupBy("user").count()
chart4_dataframe = chart4_dataframe.withColumnRenamed("count","pull_requests")
display(chart4_dataframe.sort(chart4_dataframe.pull_requests.desc()))

# COMMAND ----------


