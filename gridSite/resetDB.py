"""
Resets the sqlite3 database in case of changes to migrations and optionally
reruns all of the migrations to repopulate the database if specified
"""

from __future__ import print_function

from sqlite3 import connect
from fabric.api import local
from argparse import ArgumentParser  # optparse is deprecated

DATABASE = "db.sqlite3"
APP = "gridApp"


def resetDB():
    with connect(DATABASE) as conn:
        print("Deleting {0} tables...".format(APP))
        tablesToDelete = conn.execute(
                "SELECT name FROM sqlite_master " +
                "WHERE name LIKE '{0}'".format(APP)).fetchall()

        for table in tablesToDelete:
            tableName = table[0]  # table = (tableName,)
            conn.execute("DROP TABLE {0}".format(tableName))

        print("{0} table deletion complete!".format(APP))


def rerunMigrations():
    print("Rerunning {0} migrations...\n".format(APP))
    local("python manage.py migrate")
    print("\n{0} migrations execution complete!\n".format(APP))

if __name__ == "__main__":
    parser = ArgumentParser(description="Reset {0} database".format(APP))
    parser.add_argument("-r", "--rerun",
                        dest="rerun",
                        default=False,
                        action="store_true",
                        help="rerun {0} migrations".format(APP))

    resetDB()
    args = parser.parse_args()

    if args.rerun:
        rerunMigrations()
