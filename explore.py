# A script to examine the tag description file.
# Useful insights will be inserted as comments

import csv
import os


def tag_description():
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

def wois_data():
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
        print("Scanning file " + str(count))
        scan_file(directory + "/" + file, tags)

    # Print some info
    print("Finished scanning " + str(count) + " files")
    print("Found " + str(len(tags)) + " unique tags in total")
    print("The unique tags are: " + str(tags))


def rank_engines():

    class Engine:
        def __init__(self, identifier, partial, count):
            self.identifier = identifier
            self.partial = partial
            self.count = count

        def __repr__(self):
            avg = self.partial / float(self.count)
            return "Average FSOC for Engine " + str(self.identifier) + ": " + str(avg)

    # Engine 4 -> column 1
    # Engine 5 -> column 2
    # Engine 6 -> column 3
    engine_index = {4: 1,
                   5: 2,
                   6: 3}

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

if __name__ == "__main__":
    rank_engines()