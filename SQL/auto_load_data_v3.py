import pymysql
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import getpass
from datetime import datetime
import pandas as pd
import json
import ast

def load_data_into_mysql(table, table_path):
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
    df = pd.read_csv(table_path)
    columns = df.columns.tolist()
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join(columns)
    sql = f"INSERT IGNORE INTO {table} ({columns_str}) VALUES ({placeholders})"

    with conn.cursor() as cursor:
        for index, row in df.iterrows():
            cursor.execute(sql, tuple(None if pd.isna(row[column]) else row[column] for column in columns))
            #cursor.execute(sql, tuple(row[column] for column in columns))

    conn.commit()
    conn.close()
    print(f"Data loaded into {table} table successfully")
        
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, tables):
        super().__init__()
        self.tables = tables

    def on_modified(self, event):
        for table in self.tables:
            try:
                table_path = f"{file_path}{table}/{table}.csv"
                if event.src_path == table_path:
                    print(f"File {table_path} modified. Loading data into {table} table...\n")
                    load_data_into_mysql(table, table_path)
            except:
                print("Error loading data.")
                pass

if __name__ == "__main__":
    with open('./data_upload_config.json') as f:
        config_data = json.load(f)
    file_path = config_data["file_path"]
    tables =  ast.literal_eval(config_data["list_of_tables"])
    
    # MySQL Connection
    MYSQL_PASSWORD = getpass.getpass("Enter MySQL password: ")
    MYSQL_USER = config_data["user"]
    MYSQL_HOST = config_data["host"]
    MYSQL_DB = config_data["db"]

    event_handler = FileChangeHandler(tables)
    observer = Observer()
    for table in tables:
        observer.schedule(event_handler, path=f"{file_path}{table}/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()