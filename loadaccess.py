import pyodbc
import re
import os
import csv


pyodbc.lowercase = False
accessPath = r'C:\\Users\\skarki\\Downloads\\IPEDS200405.accdb'
accesstocsvpath = r'C:\\Users\\skarki\\Desktop\\Scraping\\AccesstoCsv\\'
filename1 = os.path.splitext(os.path.basename(accessPath))[0][5:9]
#filename2 = filename1[5:9]

excludelist = ['MSysAccessStorage','MSysACEs','MSysComplexColumns','MSysNameMap',
               'MSysNavPaneGroupCategories','MSysNavPaneGroups','MSysNavPaneGroupToObjects',
               'MSysNavPaneObjectIDs','MSysObjects','MSysQueries','MSysRelationships',
               'MSysResources']
               
conn = pyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\\Users\\skarki\\Downloads\\IPEDS200405.accdb;")
cursor = conn.cursor()
tablecol =[]

for row in cursor.tables():
    tablecol.append(row.table_name)

for tab in tablecol:
    if not str(tab).startswith('MSys'):
        cursor.execute("select * from {}".format(tab))
        filename = re.sub(r"\d{4}|\d{2}","",tab) +"_"+filename1+".csv"
        m_dict = cursor.fetchall()
        columnames = [ column[0] for column in cursor.description]
        with open(accesstocsvpath+filename,'w',newline='') as f:
                writer = csv.writer(f,delimiter=',')
                writer.writerow(i for i in columnames)
                writer.writerows(j for j in m_dict)
       
    
        
        
           




