import pyodbc
import re
import os
import csv


pyodbc.lowercase = False

accesstocsvpath = r'C:\\Users\\skarki\\Desktop\\Scraping\\AccesstoCsv\\'
AccessPath = r'C:\\Users\\skarki\\Desktop\\Scraping\\Access\\'
excludelist = ['MSysAccessStorage','MSysACEs','MSysComplexColumns','MSysNameMap',
               'MSysNavPaneGroupCategories','MSysNavPaneGroups','MSysNavPaneGroupToObjects',
               'MSysNavPaneObjectIDs','MSysObjects','MSysQueries','MSysRelationships',
               'MSysResources']

for accesdbfile in os.listdir(AccessPath):
    #print(accesdbfile)
    accessfilePath = r'C:\\Users\\skarki\\Downloads\\{}'.format(accesdbfile)
    accessdbyear = str(accesdbfile)[5:9]
    #print(accessfilePath)                
    conn = pyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        r"Dbq={};".format(accessfilePath))
    
    cursor = conn.cursor()
    tablelist =[]

    for tblname in cursor.tables():
        tablelist.append(tblname.table_name)

    for tbl in tablelist:
        if not str(tbl).startswith('MSys'):
            cursor.execute("select * from {}".format(tbl))
            filename = re.sub(r"\d{4}|\d{2}","",tbl) +"_"+accessdbyear+".csv"
            m_dict = cursor.fetchall()
            columnames = [ column[0] for column in cursor.description]
            with open(accesstocsvpath+filename,'w',newline='') as f:
                    writer = csv.writer(f,delimiter=',')
                    writer.writerow(i for i in columnames)
                    writer.writerows(j for j in m_dict)
    
    conn.close()   
        
        
           




