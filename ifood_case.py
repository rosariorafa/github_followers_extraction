import os
import api_extraction
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField,StructType, StringType, IntegerType
from pyspark.sql.functions import udf, lit, col, regexp_replace, to_date, date_format

def get_config_env_vars() -> tuple[str, str, str]:
  """
  Retorna variáveis necessárias para execução, levantando um erro caso alguma não exista.

  :return : em ordem, as variáveis com o id do usuário fonte, a chave de acesso da api, e o caminho a serem salvos os arquivos csv
  """ 
  MANDATORY_ENV_VARS = ['SOURCEUSER', 'APIKEY',"CSVPATH"]
  for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError('Failed, {} was not set to a value.'.format(var))
  return os.environ['SOURCEUSER'],os.environ['APIKEY'], os.environ['CSVPATH']
  
def main():
  """
  Executa o caminho principal da extração.
  """
  source_user, api_key, csv_save_path = get_config_env_vars()
  spark = SparkSession.builder.getOrCreate()

  user_response_schema = StructType(
    [StructField("ApiResponse", IntegerType(), False),
    StructField("Result", StructType(
        [StructField("name", StringType(), True),
         StructField("company", StringType(), True),
         StructField("blog", StringType(), True),
         StructField("email", StringType(), True),
         StructField("bio", StringType(), True),
         StructField("public_repos", IntegerType(), True),
         StructField("followers", IntegerType(), True),
         StructField("following", IntegerType(), True),
         StructField("created_at", StringType(), True)
         ]
    ), True)
    ])
  udf_get_user_from_api = udf(api_extraction.get_user_from_api, user_response_schema)

  followers = api_extraction.tail_rec_get_followers_from_api(api_key,source_user)

  followers_df = spark.sparkContext.parallelize(followers).toDF().withColumnRenamed("_1","follower")
  users_df = followers_df.withColumn("user_response", udf_get_user_from_api(lit(api_key),followers_df.follower))
  valid_responses_users_df = users_df.filter(users_df.user_response.ApiResponse == 200)\
  .select("follower","user_response.Result.*")

  fixed_company_users_df = valid_responses_users_df.withColumn("company",regexp_replace("company", r'^(\@)\d*',''))

  formated_date_users_df = fixed_company_users_df\
  .withColumn("created_at", to_date( col("created_at"), "yyyy-MM-dd'T'HH:mm:ss'Z'")) \
  .withColumn("created_at", date_format("created_at", "dd/MM/yyyy"))

  formated_date_users_df.write.options(header = 'True', delimiter=',') \
  .csv(csv_save_path)

if __name__ == '__main__':
   main()