from yaml import loader
from database import Database
import yaml

class test:
  
  def __init__(self):
    
    self.config()
    with Database(self.data) as self.db:
      self.result=self.db.query('''SELECT "Email Address" , "First Name" FROM BI_BUDGET.STG_USERS''')
     ##print(self.result)
    
  def config(self):
    with open('config.yml','r') as f:
      self.data  =yaml.safe_load(f)
  
  def __lis(self):
     self.__pp= "size of photo" 
     return self.__pp

a=test()
print(a._test__lis())