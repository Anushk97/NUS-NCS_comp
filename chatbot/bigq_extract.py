import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

class query_db():
    def __init__(self):
        self.client = bigquery.Client(project="nus-competition")
    
    def run_query(self, query):
        query_job = self.client.query(query)
        results = query_job.result()
        rows = [list(row.values()) for row in results]
        columns = [field.name for field in results.schema]
        df = pd.DataFrame(rows, columns=columns)
        return df