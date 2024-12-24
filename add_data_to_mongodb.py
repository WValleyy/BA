import os
import csv
import sys
from pymongo import MongoClient

# Tăng giới hạn kích thước trường
csv.field_size_limit(1000000)  # 1 MB

client = MongoClient("mongodb://localhost:27017")
db = client["BA_Database"]

def csv_to_mongo(file_path):
    collection_name = os.path.splitext(os.path.basename(file_path))[0]
    collection = db[collection_name]
    
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data_list = [row for row in reader]
    
    if data_list:
        collection.insert_many(data_list)
        print(f"Inserted {len(data_list)} documents into collection '{collection_name}'")
    else:
        print(f"File '{file_path}' contains no data!")

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            csv_to_mongo(file_path)

csv_folder_path = "data_BA"

process_folder(csv_folder_path)
