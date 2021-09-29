import pyodbc
import re
import os
import csv


pyodbc.lowercase = False
accessPath = r'C:\\Users\\skarki\\Downloads\\IPEDS200405.accdb'
accesstocsvpath = r'C:\\Users\\skarki\\Desktop\\Scraping\\AccesstoCsv\\'
filename1 = os.path.splitext(os.path.basename(accessPath))[0][5:9]
print(filename1)
#filename2 = filename1[5:9]

excludelist = ['MSysAccessStorage','MSysACEs','MSysComplexColumns','MSysNameMap',
               'MSysNavPaneGroupCategories','MSysNavPaneGroups','MSysNavPaneGroupToObjects',
               'MSysNavPaneObjectIDs','MSysObjects','MSysQueries','MSysRelationships',
               'MSysResources']
               
conn = pyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\\Users\\skarki\\Downloads\\IPEDS200405.accdb;")
cursor = conn.cursor()

try:
    for row in cursor.tables():
        if row.table_name not in excludelist:
            cursor.execute("select * from {}".format(row.table_name))
            filename = re.sub(r"\d{4}|\d{2}","",row.table_name) +"_"+filename1+".csv"
            print(filename)
            #print(row.table_name + "  ::  " + re.sub(r"\d{4}|\d{2}","",row.table_name))
            
            with open(accesstocsvpath+filename,'w',newline='') as f:
                writer = csv.writer(f)
                for row in cursor.fetchall():
                    writer.writerow(row)

except pyodbc.DatabaseError as error:
    print(error)


