#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:20:43 2018

@author: griggles
"""
import pandas as pd    

class Masseuse:
    def __init__(self, csv_dir='csv/'):
        self.csv_dir = csv_dir
        self.dfs = {}
        
    # create an individual dataframe for a given csv and add it to 
    # list of dataframes - separating concerns for cleaning individual datasets
    # and eventually aggregating the data into a single table
    def build_df(self, name):
        df=pd.read_csv('{}{}.csv'.format(self.csv_dir, name))
        self.dfs[name] = df
        return df
        
    # WorldBankData contains individual country data and larger regions
    # here we separate these categories to avoid recounting
    def filter_countries(self):
        fertility = self.build_df('fertility')
        countries = self.build_df('country')
        codes = countries['alpha-3']        
        mf = fertility[fertility['Country Code'].isin(codes)]
        mf = mf.set_index(mf['Country Code'])
        mf = mf.drop(columns=['Indicator Name', 'Indicator Code', 'Country Name', 'Country Code'])
        mf.columns.name='Years'
        mf = mf.stack()
        mf = mf.to_frame()
        mf = mf.rename(columns={0: "Fertility Rate"})
        self.dfs['mf'] = mf
        
        
    def merge_wb_csv_into_mf(self, name):
        mf = self.dfs['mf']
        df = self.build_df(name)
        df = df.set_index(df['Country Code'])
        df = df.drop(columns=['Indicator Name', 'Indicator Code', 'Country Name', 'Country Code'])
        df.columns.name='Years'
        df = df.stack()
        df = df.to_frame()
        df = df.rename(columns={0: "Population Density"})
        self.dfs['mf'] = mf.merge(df, how = 'inner', on = ['Country Code', 'Years'])
        
    def build_data(self):
        self.filter_countries()
        #self.merge_population_densities()
        self.merge_wb_csv_into_mf('density')
        return self.dfs['mf']


m = Masseuse()
data = m.build_data()
print(data)
        

        
            
        
    
        