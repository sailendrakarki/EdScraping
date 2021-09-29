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
    
    accessfilePath = AccessPath+accesdbfile
    accessdbyear = str(accesdbfile)[5:9]
                    
    conn = pyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        r"Dbq={};".format(accessfilePath))
    
    cursor = conn.cursor()
    tablelist =[]

    for tblname in cursor.tables(tableType='TABLE'):
        tablelist.append(tblname.table_name)
    
    for tbl in tablelist:
        if not str(tbl).startswith('MSys'):
            cursor.execute("select * from {}".format(tbl))
            filename = re.sub(r"\d{4}|\d{2}","",tbl) +"_"+accessdbyear+".csv"
            records = cursor.fetchall()
            columnames = [ column[0] for column in cursor.description]
            with open(accesstocsvpath+filename,'w',newline='') as f:
                    writer = csv.writer(f,delimiter=',')
                    writer.writerow(col for col in columnames)
                    writer.writerows(row for row in records)
    
    conn.close()   
        
        
           




