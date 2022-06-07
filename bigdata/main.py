from pyspark.sql import SparkSession
import json
import sys

calendar_file_name = sys.argv[1]
product_file_name = sys.argv[2]
sales_file_name = sys.argv[3]
store_file_name = sys.argv[4]

appName = "Nike Spark test"
master = 'local'
spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

calender = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load(calendar_file_name)

#consumption = spark.read.format('csv') \
#                .option('header',True) \
#                .option('multiLine', True) \
#                .load('./consumption.csv')

product = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load(product_file_name)

sales = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load(sales_file_name)

store = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load(store_file_name)

calender = calender.selectExpr("datekey as dateId", "datecalendarday as datecalendarday",
                               "datecalendaryear as datecalendaryear", "weeknumberofseason as weeknumberofseason")

product_sales = product.join(sales, on='productid')
data = store.join(product_sales, on='storeId')
data = data.join(calender, on='dateId', how='left')

data_json = data.toJSON().collect()
data_json = [json.loads(string_data) for string_data in data_json]
def create_week_format(_data):
    week_target = _data['weeknumberofseason']
    week_dict = {}
    for weekly_year in range(1, 53):
        if weekly_year == int(week_target):
            week_dict[f'W{weekly_year}'] = _data['salesUnits'] # should be multiplied by salesUnits?
        else:
            week_dict[f'W{weekly_year}'] = 0

    return week_dict

def create_unique_key(_data):
    unique_key = f"RY{str(_data['datecalendaryear'])[-2:]}_{_data['channel'].upper()}_{_data['division']}_{_data['gender']}_{_data['category']}"
    return unique_key

for element in data_json:
    element['unique_key'] = create_unique_key(element)
    element['dataRow'] = create_week_format(element)
    element['rowId'] = element['netSales']
    element.pop('weeknumberofseason')
    element.pop('salesUnits')
    element.pop('rowId')
data_json = spark.createDataFrame(data_json)
data_json = data_json.toJSON().collect()

for file in data_json:
    with open(f"./json files/{json.loads(file)['saleId']}.json", 'w') as outfile:
        json.dump(file, outfile)
