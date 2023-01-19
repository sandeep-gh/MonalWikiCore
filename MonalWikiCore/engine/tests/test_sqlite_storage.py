from sqlite3 import connect, Row

db_filepath = "/home/kabira/var/data/monalwiki//wiki2//.meta.db"

conn = connect(db_filepath)
conn.row_factory = Row
tblname = "store"
rows = list(conn.execute(f"select value from {tblname}"))
print(rows)
key = "kuchi"
value = "bhalo"
conn.execute(f"""insert into  {tblname} values ("{key}", "{value}")""")

rows = list(conn.execute(f"select value from {tblname}"))
print(rows)

conn.commit()
