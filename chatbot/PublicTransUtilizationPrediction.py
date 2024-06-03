import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

class PublicTransUtilizationPrediction:
    def __init__(self, input_df, input_column, arima_order, year):
        self.input_column = input_column
        self.arima_order = arima_order
        self.year = year
        self.df_original = input_df
        self.df = input_df[input_df['year'] < 2020]
        self.model = ARIMA(self.df[self.input_column], order=self.arima_order)
        self.model_fit = self.model.fit()
        self.year_range_predict = [x for x in range(self.df['year'][len(self.df)-1] + 1, self.year + 1)]
        
    def predict(self):
        output_dict = {'year': self.year_range_predict, self.input_column:[]}
        output = self.model_fit.forecast(len(self.year_range_predict))
        output_dict[self.input_column] = output.values.tolist()
        output_df = pd.DataFrame(output_dict)
        final_df = pd.concat([self.df_original, output_df[output_df['year'] > max(self.df_original['year'])]]).reset_index(drop=True)
        return final_df

