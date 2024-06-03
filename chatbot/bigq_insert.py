from google.cloud import bigquery
import pandas as pd

class BQDataInserter:
    def __init__(self, project_id="nus-competition", dataset_id="Chatbot", table_id="chat_history"):
        self.project_id = project_id
        self.client = bigquery.Client(project=self.project_id)
        self.dataset_id = dataset_id
        self.table_id = table_id

    def create_table(self):
        schema = [
            bigquery.SchemaField("file_name", "STRING"),
            bigquery.SchemaField("query", "STRING"),
            bigquery.SchemaField("answer", "STRING"),
            bigquery.SchemaField("timestamp", "TIMESTAMP")
        ]
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        try:
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)
            print(f"Table {table.table_id} created.")
        except Exception as e:
            print("Error creating table:", e)

    def insert_dataframe(self, dataframe):
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        
        table = self.client.get_table(table_ref)
        if not table:
            print(f"Table {self.table_id} does not exist.")
            return
        
        schema = [field for field in table.schema]
        existing_records = self.client.list_rows(table_ref)
        existing_data = [tuple(row.values()) for row in existing_records]
        new_data = [tuple(row) for row in dataframe.values]
    
        unique_data = [data for data in new_data if data not in existing_data]
    
        if not unique_data:
            print("No unique records to insert.")
            return
        else:
            print("Successfully inserted record(s).")
    
        unique_dataframe = pd.DataFrame(unique_data, columns=dataframe.columns)
        self.client.insert_rows_from_dataframe(table_ref, unique_dataframe, selected_fields=schema)
