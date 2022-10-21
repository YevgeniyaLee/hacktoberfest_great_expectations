from pyspark import Row
from pyspark.sql import SparkSession
from great_expectations.dataset import SparkDFDataset

# requirements
# great_expectations==0.15.28
# pyspark==3.2.1
# pytest==6.0.1

def reproduce_4295_issue():
    # given
    columns = ["country", "city", "area"]
    data = [
        ("Poland", "Warsaw", 1000),
        ("Poland", "Warsaw", 500),
        ("Poland", "Warsaw", 1500)
    ]

    spark = SparkSession.builder.master("local[*]").appName("reproduce_4295_issue").getOrCreate()
    df = spark.createDataFrame(map(lambda x: Row(*x), data), columns)
    ge_df = SparkDFDataset(df)

    # when
    result = ge_df.expect_compound_columns_to_be_unique(column_list=['country', 'city'], result_format={'result_format': "COMPLETE"})

    # then
    assert result['result']['details']['partial_unexpected_counts_error'] == 'partial_unexpected_counts requested, but requires a hashable type'