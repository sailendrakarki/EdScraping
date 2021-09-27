import os
import glob
import time
import csv
import cx_Oracle as orcCon
from cx_Oracle import DatabaseError
import config as conf

class LoadOracle:
    def __init__(self): 
        self.config()
        if self.countfile()>0:
            self.databaseConnection()  
        else:
            print("No file found ")
        

    def databaseConnection(self):
        try:
            dsn_tns = orcCon.makedsn(conf.HOST,conf.PORT,conf.SERVICE_NAME)
            conn = orcCon.connect(conf.USER, conf.PASSWORD , dsn=dsn_tns)
            if conn:
                cursor =conn.cursor()
                self.schema = 'BI_BUDGET'    
                print("Connecting to Database......")
                success = 0
                for csvfile in os.listdir(os.chdir(self.csvpath)):
                    if csvfile.endswith(".csv") or csvfile.endswith(".CSV"):
                        tablename =csvfile.rsplit('.',1)[0].upper().replace(" ","_")
                        cursor.execute("select table_name from user_tables where table_name='{}'".format(tablename))
                        result =cursor.fetchone()
                        if result:
                           cursor.execute("Truncate table {}.{}".format(self.schema,tablename))
                           with open(csvfile,encoding = 'cp850') as file:
                            reader = csv.reader(file,delimiter=',')
                            L =[]
                            first_row = next(reader)
                            
                            column_string_staging ='"'+'","'.join(first_row)+'"'
                            column_string_mapping = column_string_staging.maketrans('','',"ï»¿´╗┐")
                    
                            column_string = column_string_staging.translate(column_string_mapping)
                            insert_string='insert into ' + self.schema + '.' + tablename + ' (' + column_string + ') values ('
                            val_list=[]
                            for i in range(1,len(first_row)+1):
                                val_list.append(':'+ str(i))
                            value_string=','.join(val_list)
                            insert_string += value_string + ')'
                            
                            for row in reader:
                                for index,col in enumerate(row):
                                    row[index] =col
                                L.append(row)
                          
                            cursor.prepare(insert_string)
                            cursor.executemany(None,L)
                            
                            success = success+1

                        else:
                            print("No table found in oracle")
                if success == 1: 
                    #cursor.callproc("UD_EMAIL_NOTIFICATION")
                    conn.commit()
                    print("Record inserted succesfully!!")
                    #self.filemove()
                
                        
        
        except DatabaseError as e:
            err, = e.args
            print("Oracle Error Code:",err.code)
            print("Oracle Error Message:",err.message)
        finally:
            cursor.close()
            conn.close()
           

    def config(self):
        self.Basepath = r"C:\\Users\\skarki\\Desktop\\Scraping\\"
        self.csvpath =r"C:\\Users\\skarki\\Desktop\\csv\\"
        self.archievepath = r"C:\\Users\\skarki\\Desktop\\Scraping\\"
        self.isdir = os.path.isdir(self.csvpath)
  
    def countfile(self):
            os.chdir(self.csvpath)
            self.list = [f for f in glob.glob("*.csv")]
            self.number_files = len(self.list)
            
            return self.number_files
            
    def filemove(self):
        self.isdir =os.path.isdir(self.csvpath)
        if os.path.isdir(self.csvpath) and os.path.isdir(self.archievepath):
            for f in self.list:
                appendName = os.path.splitext(f)[0] +"_"+ time.strftime("%Y%m%d%H%M")+".csv"
                os.rename(self.csvpath+f,self.archievepath+appendName)
            print("Files move succesfully!!")
        else:
            print("Folder not found")
            
LoadOracle()