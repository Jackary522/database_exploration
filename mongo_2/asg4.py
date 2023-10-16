#!/usr/local/bin/python3

from pymongo import MongoClient
import argparse as argp
import pprint

USER = 'root'
PASS = 'mongo'
HOST = 'localhost'
PORT = '27017'


def argparser():
    parser = argp.ArgumentParser()
    parser.add_argument('-l', '--lastname', action='store',
                        type=str, help='Query by last name')

    return parser.parse_args()


def query(collection, last_name: str):
    print()
    for result in collection.find({'last_name': last_name}):
        pprint.pprint(result)
    print()


def main():
    last_name = argparser().lastname

    if not last_name:
        print("Please pass a last name to query. Refer to -h for help!")
        return

    client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/')
    db = client['contacts']
    collection = db['contacts']

    query(collection, last_name)


if __name__ == '__main__':
    main()
