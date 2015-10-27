"""
Resets the sqlite3 database in case of changes to migrations and optionally
reruns all of the migrations to repopulate the database if specified
"""

from sqlite3 import connect
from fabric.api import local
from argparse import ArgumentParser  # optparse is deprecated

DATABASE = "db.sqlite3"
APP = "gridApp"


def resetDB():
    with connect(DATABASE) as conn:
        print "Deleting {} tables...".format(APP)
        tablesToDelete = conn.execute(
            "SELECT name FROM sqlite_master " +
            "WHERE instr(name, '{}') > 0".format(APP)).fetchall()

        for table in tablesToDelete:
            tableName = table[0]  # table = (tableName,)
            conn.execute("DROP TABLE {}".format(tableName))

        print "{} table deletion complete!".format(APP)
        print "\nDeleting {} migrations in history...".format(APP)
        conn.execute(
            "DELETE FROM django_migrations WHERE app='{}'".format(APP)
        )

        print "{} migrations deletion complete!\n".format(APP)


def rerunMigrations():
    print "Rerunning {} migrations...\n".format(APP)
    local("python manage.py migrate")
    print "\n{} migrations execution complete!\n".format(APP)

if __name__ == "__main__":
    parser = ArgumentParser(description="Reset {} database".format(APP))
    parser.add_argument("-r", "--rerun",
                        dest="rerun",
                        default=False,
                        action="store_true",
                        help="rerun {} migrations".format(APP))

    resetDB()
    args = parser.parse_args()

    if args.rerun:
        rerunMigrations()
