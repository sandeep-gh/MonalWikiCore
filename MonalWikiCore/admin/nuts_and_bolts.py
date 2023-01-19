import sqlite3
import sqlalchemy as sqa
from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, ADMIN_DB_SQLALCHEMY_URL, BACKEND_DATADIR_BASE


def init_db():
    dbEngine=sqa.create_engine(ADMIN_DB_SQLALCHEMY_URL)
    #https://stackoverflow.com/a/71685414
    with dbEngine.connect()  as conn:
        pass

    #con = sqlite3.connect(ADMIN_DB_SQLALCHEMY_URL)
    #con.commit()

#print(ADMIN_DB_SQLALCHEMY_URL)
#init_db()
tdir =  "/home/kabira/var/data/monalwiki/freshwiki"
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# subprocess.run(["sed", f"'s/sqlalchemy.url.*/sqlalchemy.url={ADMIN_DB_SQLALCHEMY_URL}/'" , tdir + "/alembic.ini"]
#                )

#print (quote(ADMIN_DB_SQLALCHEMY_URL))
# import subprocess
# subprocess.run(["sed", "-i", f"s_sqlalchemy.url.*_sqlalchemy.url = {ADMIN_DB_SQLALCHEMY_URL}_" , tdir + "/alembic.ini"]
#                )


print (BACKEND_DATADIR_BASE)
from pathlib import Path
version_dir = Path(os.path.join(tdir, "alembic/versions"))
baseline_file= next(version_dir.glob("*_baseline.py"))
print (baseline_file.stem.split("_")[0])

