import pyodbc


pyodbc.lowercase = False
accessPath = r'C:\\Users\skarki\\Downloads\\IPEDS2000405.accdb'

conn = pyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\\Users\skarki\\Downloads\\IPEDS200405.accdb;")
cursor = conn.cursor()

try:
    cursor.execute('''GRANT SELECT ON MSysObjects TO Admin;''')
   
except pyodbc.DatabaseError as error:
    print(error)
else:
    result = cursor.fetchone()
    print(result)

