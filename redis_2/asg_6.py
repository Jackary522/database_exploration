import redis
import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lastname', action='store', type=str)

    return parser.parse_args()

def fetch_data():
    try:
        r = redis.StrictRedis(decode_responses=True)

    except ConnectionError:
        print('Redis Connection Error. Please verify instance is running.')
        exit(1)

    res = parse()
    keys = r.keys('*')

    for key in keys:
        if r.lindex(key, 1) == res.lastname:
            print('\nKey:', key, '--> Value:', r.lrange(key, 0, -1), '\n')

def main():
    fetch_data()

if __name__ == '__main__':
    main()