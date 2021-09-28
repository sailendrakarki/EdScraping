import pyodbc
import re


pyodbc.lowercase = False
accessPath = r'C:\\Users\skarki\\Downloads\\IPEDS200405.accdb'
excludelist = ['MSysAccessStorage','MSysACEs','MSysComplexColumns','MSysNameMap',
               'MSysNavPaneGroupCategories','MSysNavPaneGroups','MSysNavPaneGroupToObjects',
               'MSysNavPaneObjectIDs','MSysObjects','MSysQueries','MSysRelationships',
               'MSysResources']
conn = pyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\\Users\skarki\\Downloads\\IPEDS200405.accdb;")
cursor = conn.cursor()

try:
    for row in cursor.tables():
        if row.table_name not in excludelist:  
            print(row.table_name + "  ::  " + re.sub(r"\d{4}|\d{2}","",row.table_name)+"::")
            
   
except pyodbc.DatabaseError as error:
    print(error)


