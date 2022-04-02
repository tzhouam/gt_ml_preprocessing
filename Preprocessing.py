import pandas as pd
import sklearn as sk
import numpy as np
from scipy.stats import zscore
from scipy import stats
import matplotlib.pyplot as plt

class Preprocessing:
    def __init__(self,file_path='winequalityN.csv',save_path='Preprocessed_winequalityN.csv'):
        self.file_path=file_path
        self.data=pd.read_csv(self.file_path)
        self.processed=None
        self.save_path=save_path
        print('Data types:')
        print(self.data.dtypes)
        print()


    def fill_blanks_with_0(self):
        self.data=self.data.replace(r'^\s*',0,regex=True)
        self.data=self.data.fillna(0)
        return self.data

    def drop_NaN(self):
        print()
        print('Counted NaN as missing values in original dataset:')
        print(self.data.isna().sum())
        print('Total:\t\t\t',self.data.isna().sum().sum())
        print('Total number of lines:\t',self.data.shape[0])
        before=self.data.shape[0]
        self.data=self.data.dropna()
        self.data = self.data.reset_index(drop=True)
        print('After droping NaN:\t', self.data.shape[0])
        print('Droping ratio:\t\t',round(1-p.data.shape[0]/before,5))
        return self.data

    def change_first_column(self):
        """type: white -> 0, red->1"""
        self.data['type']=pd.factorize(self.data['type'])[0]
        print('After changing the first column into number:')
        print(self.data.dtypes)
        print()

        return self.data

    def Z_score_normalization(self):
        self.data=self.data.apply(zscore)
        return self.data

    def remove_outlier_IQR(self):
        for col_name in self.data.columns:
            if col_name=='type':
                continue
            q1 = self.data[col_name].quantile(0.25)
            q3 = self.data[col_name].quantile(0.75)
            iqr = q3 - q1  # Interquartile range
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_low=(self.data[col_name]<lower_bound)
            outlier_high = (self.data[col_name] > upper_bound)
            self.data=self.data[~(outlier_low|outlier_high)]

    def remove_outlier_Z(self):
        print()
        print('Total number of lines before remove_outlier_Z:\t', self.data.shape[0])
        before = self.data.shape[0]
        for col_name in self.data.columns:
            if col_name=='type':
                continue
            m=self.data.apply(zscore)
            outlier_low=(m[col_name]<-3)
            outlier_high = (m[col_name] > 3)
            self.data=self.data[~(outlier_low|outlier_high)]
            self.data=self.data.reset_index(drop=True)
        print('After droping outliers:\t', self.data.shape[0])
        print('Droping ratio:\t\t', round(1 - p.data.shape[0] / before, 5))

    def save(self):
        self.data.to_csv(self.save_path)






if __name__=="__main__":
    p=Preprocessing()
    # print('Data types:')
    # print(p.data.dtypes)
    # print()
    # print('After changing the first column into number:')
    p.change_first_column()
    # print(p.data.dtypes)
    # print('\n\n')
    # print(p.data)
    p.drop_NaN()
    p.remove_outlier_Z()

    print('Since the data is not sorted, smoothing cannot be applied to the data.')


    p.save()