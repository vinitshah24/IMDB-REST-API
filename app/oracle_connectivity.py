import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_9")

try:
    con = cx_Oracle.connect('system/admin@localhost:1521/orcl')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM SYSTEM.GENRE")
    rows = cursor.fetchall()
    print(rows)
except Exception as e:
    print(f"Exception caught while quering database: {e}")
finally:
    if cursor:
        cursor.close()
    if con:
        con.close()
