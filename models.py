import csv
import os
from datetime import datetime
import pandas as pd
import numpy as np


def subset_month(input_file, month = 7):

    def get_date(line):
        date, time = line.split(' ')
        return date

    def get_time(line):
        date, time = line.split(' ')
        time = time.split("+")[0]
        return time

    def get_month(date):
        return date.split('-')[1]

    df = pd.read_csv(input_file)
    df['date'] = map(get_date, df['time'])
    df['time'] = map(get_time, df['time'])
    df['month'] = map(get_month, df['date'])

    df['timestamp'] = df[['date', 'time']].apply(lambda x: ' '.join(x), axis=1)
    del df['date']
    del df['time']

    subset = df.query('month == "07"')
    #subset.columns = map(lambda x: str.replace(x, "@", "-"), subset.columns)
    subset.to_csv("ambient_out.csv", index=False)

def join_datasets(original, ambient):
    df1 = pd.read_csv(original)
    df2 = pd.read_csv(ambient)
    merged = df1.merge(df2, on="timestamp")
    merged.to_csv("merged6.csv", index=False)

def split_ambient(input_file, engine):
    df = pd.read_csv(input_file)
    for column in df:
        engine_num = column.split('.')[-1]
        if(engine_num.isdigit()):
            if(int(engine_num) != engine):
                del df[column]
    df.to_csv("ambient_" + str(engine), index=False)


def split_df(directory):
    for file in os.listdir(directory):
        print("processing file " + file)
        temp = pd.read_csv(directory + "/" + file).head(2878)
        df4 = temp[['timestamp', 'MT_DG04R_007', 'MT_DG04S_007', 'SFOE4SFOC']].to_csv("July/joined/engine4/" + file, index=False)
        df5 = temp[['timestamp', 'MT_DG05R_007', 'MT_DG05S_007', 'SFOE5SFOC']].to_csv("July/joined/engine5/" + file, index=False)
        df6 = temp[['timestamp', 'MT_DG06R_007', 'MT_DG06S_007', 'SFOE6SFOC']].to_csv("July/joined/engine6/" + file, index=False)

def engine_usage(input_file):
    def helper(sfoc):
        off = (sfoc < 5).sum()
        on = (sfoc > 190).sum()
        transition = len(sfoc) - off - on
        d = {
            "off": off,
            "on": on,
            "transition": transition
        }
        print(d)

    df = pd.read_csv(input_file)
    engine_num = input_file.split('.')[0][-1]
    target_col = "SFOE" + engine_num + "SFOC"
    helper(df.SFOE6SFOC)

def normalize(df, method = 'normal'):
    methods = ('normal', 'max')
    if method not in methods:
        raise ValueError('method can be either normal or max')

    timestamp = df.pop('timestamp')
    df.index = timestamp
    if(method == 'normal'):
        return (df - df.mean()) / df.std()

    return (df - df.min()) / (df.max() - df.min())

def drop_zeros(input_file):
    df = pd.read_csv(input_file)
    df = df[df.SFOE6SFOC > 100] # maybe error coz its a string not float

    del df['timestamp']
    del df['month']
    df.to_csv('nozero_' + input_file,index=False)

if __name__ == "__main__":
    # Call any function here like so:
    #subset_month('data/ambient.csv')
    #join_datasets("July/joined/engine6/all.csv", 'ambient_6.csv')
    #split_df("July/joined/original")
    #split_ambient("ambient_out.csv", 6)
    #drop_zeros('training_sets/merged6.csv')
    engine_usage('July/merged6.csv')

