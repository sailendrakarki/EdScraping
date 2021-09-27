
import os.path as path
import os
import sys
import zipfile
import pandas as pd
import csv
import openpyxl

def extract():
  inital_loc = r"C:\\Users\\skarki\\Downloads\\"  #initlocation
  final_loc  = r"C:\\Users\skarki\\Desktop\\csv\\" #finallocation
  
  '''
  1. check inital location is valid 
  2. if valid create intermidate folder and zip extract in current location 
  3. extract zip files on zipextract folder location
  4. filter excel files and move them into intermediate folder
  4. then merge them into single file
  5. copy into finallocation
  6. del intermediate folder
  '''
  
  if path.isdir(inital_loc) and path.isdir(final_loc):
    zipextract = "zipextract\\"
    interfiles = "interfolder\\"
    
    interfilespath = path.join(os.getcwd(),interfiles)
    zipextractpath = path.join(os.getcwd(),zipextract)
    
    if not path.isdir(interfilespath):
      os.mkdir(interfilespath,0o777) 
    
    if not path.isdir(zipextractpath):
      os.mkdir(zipextractpath,0o777) 
    
    for file in os.listdir(inital_loc):
        if file.startswith("IPEDS") and file.endswith(".zip"):
          with zipfile.ZipFile(inital_loc+"\\"+file,"r") as zip_ref:
            zip_ref.extractall(zipextract)
           
    for xlsfile in os.listdir(zipextractpath):
        if xlsfile.startswith("IPEDS") and xlsfile.endswith(".xlsx"):
          if os.path.exists(interfilespath+"\\"+xlsfile):
           os.remove(interfilespath+"\\"+xlsfile)
           
          os.rename(zipextractpath+"\\"+xlsfile,interfilespath+"\\"+xlsfile)
    
    df_total = pd.DataFrame()
    for file in os.listdir(interfilespath):                         # loop through Excel files
        print(file)
        if file.endswith('.xlsx'):
            xlspath = path.join(interfilespath,file)
            
            excel_file = pd.ExcelFile(xlspath)
            
            sheets = excel_file.sheet_names
            for sheet in sheets:               # loop through sheets inside an Excel file
                if str(sheet).startswith("vartable"):
                  df = excel_file.parse(sheet_name = sheet,index_col=0)
                  df_total = df_total.append(df)
    df_total.to_excel('combined_file.xlsx')
    excelopen = openpyxl.load_workbook('combined_file.xlsx')
    excelsheet = excelopen.active
    
    col = csv.writer(open("IPEDS_METADATA.csv",'w',newline=""))
    
    for r in excelsheet.rows:
      col.writerow([cell.value for cell in r])
      
    
  else:
    print("location are not avilable")
  

extract()
  