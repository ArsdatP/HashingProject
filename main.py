# Demonstrate DIY hashing implmenentation

import json
import statistics
from collections import namedtuple
import time
import sys

# TABLE_SIZE should be a prime number, see:
# https://medium.com/swlh/why-should-the-length-of-your-hash-table-be-a-prime-number-760ec65a75d1
# for a list of prime numbers, please see:
# https://en.wikipedia.org/wiki/List_of_prime_numbers#The_first_1000_prime_numbers
TABLE_SIZE = 5003




# One bucket in a hash table
class Bucket():

    def __init__(self, key_str, val_str):
        self.key = key_str
        self.val = val_str

    def print_me( self):
        print("key=" + self.key + "," + "val=" + self.val)


# holds all the buckets
class Hash_table():

    def __init__(self, n_items):
        self.name = "My Hash Table"
        self.n_buckets = n_items
        self.bucket_list = [Bucket("", "") for i in range(self.n_buckets)]
        self.collisions = 0 

    # Convenience dump for debugging
    def print_hash_table( self, start, limit ):

        for i in range( start, start+limit):
            self.bucket_list[i].print_me( )
            
    # This is the actual hashing function   
    # Fill this in with the function of your choice,  See zyBook
    def compute_hash_bucket(self, key_str):
        sum = 0
        for x in range(len(key_str)):
            sum += sum + int(x)

        return sum % self.n_buckets


    # Based on ZyBook, 4.3.4
    # code your own insert method here
    # insert resolving collisions by linear probin
    def insert(self, key_str, val_str):
        bucket = self.compute_hash_bucket(key_str)
        buckets_probed = 0

        while buckets_probed < self.n_buckets:
            if self.bucket_list[bucket].key == "":
                self.bucket_list[bucket].key = key_str
                self.bucket_list[bucket].val = val_str
                if buckets_probed > 0:
                    self.collisions += 1
                return True

            bucket + (bucket + 1) % self.n_buckets
            buckets_probed += 1

        return False

    # Based on ZyBook, 4.3.8
    # search a hash table for a value, using linear probing
    # Code your own search method here -- remember 
    # that if you are probing you search method must be able 
    # to probe using the same algorith as your insert()
    def search_linear (self, key_str):
        bucket = self.compute_hash_bucket(key_str)

        while self.bucket_list[bucket].key != "":
            if self.bucket_list[bucket].key == key_str:
                return self.bucket_list[bucket].val
            bucket + (bucket + 1) % self.n_buckets

        return None


# 
# Utility functions
#
        
# Convert json dictionary into a a list of objects
# based on: https://pynative.com/python-convert-json-data-into-custom-python-object/
#
# These are the same and in the earlier list project
def custom_json_decoder(c_name, inDict):
    createdClass = namedtuple(c_name, inDict.keys())(*inDict.values())
    return createdClass


# Load and parse the JSON files
# create a list of objects from the specified JSON file
def load_lynx_json(c_name, f_name):
    with open(f_name, 'r') as fp:
        #Load the JSON
        json_dict = json.load(fp)
        object_list = []
        for i in range(len(json_dict)):
            tmp = custom_json_decoder(c_name, json_dict[i])
            object_list.append(tmp)
        return object_list



# 
# main starts here
#
def main():


    def test_python(master_stops_list):
        times = []
        for x in range(5):
            t0 = time.perf_counter_ns()
            test_dict = {}
            {}
            for this_stop in master_stops_list:
                test_dict[this_stop.code] = this_stop.name

            t1 = time.perf_counter_ns() - t0
            times.append(t1)

        avg_time = statistics.mean(times)
        print("Python Dict average time (ns) " + str(avg_time))
        print("Attempts: ", times)

    # Load the stops from json
    # assuming you are using Lynx stops
    master_stops_list = load_lynx_json('Stops', "stops.json")

    # create the (initial) hash table
    the_hash_table = Hash_table(TABLE_SIZE)

    # hash the stops using stop_code as key and stop__name as the stored value
    sucessful_inserts = 0
    stops_processed = 0

    # get time in nanoseconds -- maybe OS-specific?
    # See https://docs.python.org/3/library/time.html
    t0 = time.perf_counter_ns()


    
    for this_stop in master_stops_list:
        stops_processed = stops_processed + 1
        if the_hash_table.insert(this_stop.code, this_stop.name) == True:
            sucessful_inserts = sucessful_inserts + 1
    t1 = time.perf_counter_ns() - t0
    print( "elapsed ns = " + str(t1 ))

    print("stops_processed = " + str(stops_processed))
    print("sucessful_inserts = " + str(sucessful_inserts))
    print( "collisions = " + str(the_hash_table.collisions ))

    # Your test and debug code here...
    the_hash_table.print_hash_table(20, 25)
    test_stop = the_hash_table.search_linear("10036")
    print("test_stop = " + test_stop)
    test_python(master_stops_list)

if __name__ == "__main__":
    main()
