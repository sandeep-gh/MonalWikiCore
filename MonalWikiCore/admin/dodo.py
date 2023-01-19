from pathlib import Path
import doit
import os
from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, ADMIN_DB_SQLALCHEMY_URL, WIKI_DATADIR
import subprocess
from pathlib import Path
        
initial_workdir = doit.get_initial_workdir()

print (initial_workdir)
def task_init_alembic():
    def init_alembic(dependencies, targets):
        # os.system(""". ~/Development/webdevenv.sh;
        # alembic init alembic;
        # sed -i 's/sqlalchemy.url.*/{print(ADMIN_DB_SQLALCHEMY_URL)}' alembic.ini
        # """)

        os.system(""". ~/Development/webdevenv.sh;
        alembic init alembic;
        """)
        
        tdir =  "/home/kabira/var/data/monalwiki/freshwiki"
        subprocess.run(["sed",
                        "-i",
                        f"s_sqlalchemy.url.*_sqlalchemy.url = {ADMIN_DB_SQLALCHEMY_URL}_" ,
                        tdir + "/alembic.ini"]
               )

        
        
        # print ("targets = ", targets)
        # with Path(targets[0]).open("w") as fh:
        #     fh.write("testscript")

    return {
        'actions': [init_alembic],
        'targets': ['alembic.ini'],
        'file_dep': [os.path.join(initial_workdir, '.env')]
        }

        
module_path = os.path.dirname(os.path.realpath(__file__))
def task_build_admindb():
    def build_admindb():
        os.system("""alembic revision -m "baseline""")

        # get the version number

        version_dir = Path(os.path.join(WIKI_DATADIR, "alembic/versions"))
        baseline_file= next(version_dir.glob("*_baseline.py"))
        baseline_revision = baseline_file.stem.split("_")[0]

        baseline_revision_py = os.path.join(module_path, "baseline_revision.py")
        


        # place revision id 
        subprocess.run(["sed",
                        f"s/__revid__/{baseline_revision}",
                        baseline_revision_py,
                        ">",
                        baseline_file
                        ]
                       )
        
        
s
        
