# A script to examine the tag description file.
# Useful insights will be inserted as comments

import csv
import os
from datetime import datetime
import pandas as pd
import numpy as np



def tag_description():
    """ Find out how many tags exist, in what categories etc. """
    input = "data/tag_description.csv"
    with open(input, 'r') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            tag_name = row[1]
            if(tag_name) == "Group name":
                count += 1
                print(row[2])
        print("Count is: " + str(count))

def wois_data(debug = False):
    """ Explore sensor data and print some statistics """
    def scan_file(input_file, existing_tags):
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                existing_tags.add(row[2])

    directory = "data/sensors"
    tags = set()
    count = 0
    for file in os.listdir(directory):
        count += 1
        if(debug):
            print("Scanning file " + str(count))
        scan_file(directory + "/" + file, tags)

    # Print some info
    print("Finished scanning " + str(count) + " files")
    print("Found " + str(len(tags)) + " unique tags in total")
    print("The unique tags are: " + str(tags))


def rank_engines():
    """ Rank every available engine based on its average SFOC value over every file"""
    class Engine:
        def __init__(self, identifier, partial, count):
            self.identifier = identifier
            self.partial = partial
            self.count = count

        def __repr__(self):
            avg = self.partial / float(self.count)
            return "Average FSOC for Engine " + str(self.identifier) + ": " + str(avg) +\
                   " using " + str(self.count) + " measurements"

    # Engine 4 -> column 1
    # Engine 5 -> column 2
    # Engine 6 -> column 3
    engine_index = {4: 1,
                    5: 2,
                    6: 3}

    # Will this change if I fill missing values?
    def measure_engine(engine_num):
        def scan_file(input_file, engine):
            threshold = 1
            with open(input_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    fsoc = row[engine_index[engine_num]]
                    if fsoc:
                        try:
                            partial = float(fsoc)
                            if(partial > threshold):
                                engine.partial += float(fsoc)
                                engine.count += 1
                        except ValueError:
                            pass

        directory = "data/sfoc"
        engine = Engine(identifier=engine_num, partial=0, count=0)
        file_count = 0
        for file in os.listdir(directory):
            file_count += 1
            scan_file(directory + "/" + file, engine)

        print(engine)

    engines = {4, 5, 6}
    for eng in engines:
        measure_engine(eng)

def fill_missing(directory):
    """
    Fill untransmitted values using their last valid measurement
    Computation takes place in chunks. This script needs 10min to run!
    """
    def process_file(input_file):
        print("Processing file " + input_file)
        def delete_sparse_cols(df, threshold):
            df.replace(r'\s+', np.nan, regex=True, inplace = True)
            for column in df:
                null_percent = df[column].isnull().sum() / float(len(df[column]))
                if null_percent > threshold:
                    del df[column]

        df = pd.read_csv(directory + "/" + input_file)
        delete_sparse_cols(df, threshold = 0.9)
        df.fillna(method = 'bfill', inplace = True)
        output_file = "out_" + input_file
        df.to_csv(output_file)

    for file in os.listdir(directory):
        process_file(file)


def transform_dttm():
    """
    Transform date from raw format: 2016-02-02T01:53:12.500000
    to proper python date time object.
    """
    def del_columns():
        del df['sensor_description']
        del df['unit']
        del df['engine_id']
        del df['engine_type']
        del df['engine_subtype']
        del df['installation_id']

    def get_date(line):
        date, time = line.split('T')
        return date

    def get_time(line):
        date, time = line.split('T')
        time = time.split(".")[0]
        return time

    file = 'data/sensors/all.csv'
    df = pd.read_csv(file)
    date = map(get_date, df['ts'])
    time = map(get_time, df['ts'])
    df['date'] = date
    df['time'] = time
    df['v'] = df['v'].apply(lambda x: round(x, 1))
    df = df.drop_duplicates(subset=['tag', 'date', 'time'], keep='first')
    del df['ts']
    df.to_csv('out.csv', index = False)

def reshape(input_file):
    """
    Long to wide format
    :param input_file: String
    :return: void
    """
    long_df = pd.read_csv(input_file)
    wide_df = long_df.pivot_table(index = ['date', 'time'], columns = 'tag', values = 'v')
    wide_df.to_csv('wide.csv')


if __name__ == "__main__":
    # Call any function here like so:
    #tag_description()
    #rank_engines()
    #wois_data(debug = True)
    #transform_dttm()
    #reshape('sample.csv')
    fill_missing('data/sensors/wide/parts')
