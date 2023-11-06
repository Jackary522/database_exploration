
from cassandra.cluster import Cluster, Session
from argparse import ArgumentParser, Namespace

def parse() -> Namespace:
    parser = ArgumentParser(
        prog='cassandra_lastname',
        description='Queries a Cassandra DB by Last Name'
    )

    parser.add_argument('-l', '--lastname',
                        action='store',
                        type=str,
                        help='Last name to be queried',
                        required=True)

    return parser.parse_args()


def connect() -> Session:
    cluster = Cluster(
        ['127.0.0.1'],
        port=9042
    )

    return cluster.connect()


def run_query(session: Session, lastname: str) -> None:
    session.set_keyspace('contacts')

    rows = session.execute(
        f'SELECT * FROM contacts.contacts_names WHERE lastname = \'{lastname}\';'
    ).all()

    if len(rows) == 0:
        print(
            f'\nThis query returned 0 results')
        exit(0)
    else:
        for row in rows:
            print(f'''{row.contactid} - {row.firstname} {row.lastname} - {row.email} - ({row.areacode}) {row.phone}''')


def main():
    session = connect()
    lastname = parse().lastname
    run_query(session, lastname)


if __name__ == '__main__':
    main()
