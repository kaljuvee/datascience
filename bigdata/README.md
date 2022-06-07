# Overview

The aim of this sample job is to create a set of simple JSON extract files from various csv sources based on specific conditionis (weekly aggregation).

Below are the instructions to run the job from command line and we have also included an illustrative notebook called sample_notebook.ipynb.

# Intstallation

After cloning this repository, set up Python environment and install any dependencies as follows:

* `export PYTHONPATH=$(pwd):$PYTHONPATH`
* `cd ./<project_dir>`
* `pip3 install -r requirements.txt`

# Running Job

On a machine with Spark cluster installed, run the following command:

`spark-submit main.py calendar.csv product.csv sales.csv store.csv --cluster_size 2`

The output should be about 70 different JSON files as described below and shown in json_files.zip.

# Data

* Source files sales.csv, calendar.csv, store.csv and product.csv
* Destination files format consumption.json


# Description 

* Sales data contains transactional data with the following columns netSales, salesUnits, dateId, productId and storeId. These fields need to be joined with other fields from other csv’s to get the weekly aggregated value for each combination.

* Calendar data contains dateId, week number and year. (Criteria: sales.dateId should be equal to calendar.dateId to get weekNumber and year) 

* Product data contains productId vs hierarchy. (division, gender, category) (Criteria : sales.productId = product.productId)

* Store data contains store vs channel information. (Criteria:sales.storeId = store.storeId)

# Output
Output should be bunch of json files which is having the weekly aggregated values of net_sales and sales_units. The json files will have unique key. (Refer: consumption.json) 
