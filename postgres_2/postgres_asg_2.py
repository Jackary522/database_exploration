'''
Assignment #2 - PostgreSQL
--------------------------
The python file should be uploaded.

Write a Python Script to allow command line searches of the University database by the following criteria:
- By student id [-s | --stuid]
- By last name  [-l | --lastname]
- By major      [-m | --major]
- By rank (freshman, sophomore, junior, and senior) [-r | --rank]

The data returned should be the student's:
- stuid
- lastname
- firstname
- majordesc
- credits

The data output is written to two separate files and should be in the following formats:
- CSV (tilde delimited)
- JSON

Written by Jack Hatton
'''

from typing import Any
import psycopg2 as psql
import argparse as argp
import json

# Update these global constants to connect to your PostgreSQL instance
USER = 'postgres'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = '5432'
DATABASE = 'university'


def get_args() -> argp.Namespace:
    '''
    Builds a help menu and parses for command line arguments.
    Returns a namespace containing parsed arguments.
    '''

    parser: argp.ArgumentParser = argp.ArgumentParser()
    group: argp._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()

    group.add_argument('-s', '--stuid', action='store',
                       type=str, help='Query by Student ID')
    group.add_argument('-l', '--lastname', action='store',
                       type=str, help='Query by Lastname')
    group.add_argument('-m', '--major', action='store',
                       type=str, help='Query by Major')
    group.add_argument('-r', '--rank', action='store', type=str,
                       help='Query by Rank [freshman | sophomore | junior | senior]')

    return parser.parse_args()


def parse_args(args: argp.Namespace) -> str:
    '''
    Parses an Args Namespace for a valid flag.
    Returns a WHERE clause to be appended to the PostgreSQL query.
    '''

    if args.stuid:
        return f'where stuid = \'{args.stuid}\''
    elif args.lastname:
        return f'where lastname = \'{args.lastname.capitalize()}\''
    elif args.major:
        return f'where majordesc = \'{args.major}\''
    elif args.rank:
        match args.rank.lower():
            case 'freshman':
                return f'where credits < 30'
            case 'sophomore':
                return f'where credits between 30 and 61'
            case 'junior':
                return f'where credits between 61 and 90'
            case 'senior':
                return f'where credits >= 90'
    else:
        return ''


def query(conn, where: str) -> list[tuple[Any, ...]]:
    '''
    Initializes a PostgreSQL cursor.
    Generates a SELECT statement with the appropriate WHERE clause.
    Returns the queried tuples in as a list.
    '''

    curr: psql._Cursor = conn.cursor()

    query_string: str = f'''
        select stuid, lastname, firstname, majordesc, credits
        from students s
        join majors m on s.majorid = m.majorid
        {where}
        '''

    curr.execute(query_string)
    records: list[tuple[Any, ...]] = curr.fetchall()
    curr.close()

    return records


def data_output(data: list[tuple[Any, ...]], csv_filename: str, json_filename: str) -> None:
    '''
    Opens a ~ delimited .csv file and writes passed data to the .csv file.
    Opens a .json file and writes passed data to the .json file.
    '''

    with open(csv_filename, 'w') as tsv_data:
        for tup in data:
            tsv_data.write('~'.join(map(str, tup)) + '\n')

    with open(json_filename, 'w') as json_data:
        json.dump([
            dict(zip(('stuid', 'firstname', 'lastname', 'majordesc', 'credits'), tup))
            for tup in data
        ], json_data, indent=4)


def main() -> None:
    '''
    Calls the command line argument parser.
    Connects to the PostgreSQL database with global connection options.
    Calls the WHERE parser.
    Calls the query cursor.
    Outputs the data to files and closes the connection.    
    '''

    args: argp.Namespace = get_args()

    try:
        conn = psql.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE
        )
    except Exception:
        print('Couldn\'t connect to database')
        return

    where: str = parse_args(args)
    data: list[tuple[Any, ...]] = query(conn, where)

    if not data:
        print('Select query returned 0 students. Please try another query.')
        return

    print(f'Select query returned {len(data)} students')

    data_output(data, './student_report.csv', './student_report.json')

    conn.close()


if __name__ == '__main__':
    main()
