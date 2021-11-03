'''
 * @author Sahil 
 * @email skarki@unr.edu
 * @create date 2021-09-17 14:28:24
 * @modify date 2021-09-21 10:52:36
 * @desc [download zip files]
 */
'''
from selenium import webdriver
from pathlib import Path
import os
import sys


# Provide path for download and chromedriver executable
downloadfolder = str(os.path.join(Path.home(), "Downloads"))
webdriverpath = str(os.path.join(os.getcwd(), "chromedriver.exe"))

# check if file and folder exist
if not os.path.isdir(downloadfolder) or not os.path.isfile(webdriverpath):
    print('folder or executable is missing')
    sys.exit()

# Configuration settings
URL = "https://nces.ed.gov/ipeds/use-the-data/download-access-database"
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": downloadfolder,
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "safebrowsing_for_trusted_sources_enabled": False,
         "safebrowsing.enabled": False,
         "excludeSwitches":["enable-logging"]}
options.add_experimental_option('prefs', prefs)

# driver set up
driver = webdriver.Chrome(executable_path=webdriverpath, chrome_options=options)
driver.get(URL)
linkslist = driver.find_elements_by_xpath(
    '/html/body/div[1]/div[4]/div/table/tbody/tr/td/a')

# download from link

for links in linkslist:
    if str(links.get_attribute('href')).endswith(".zip"):
        print(links.get_attribute('href'))
        link = links.get_attribute('href')
        fileName = (link.split('/')[-1]).split('.')[0]
        if not os.path.isfile(downloadfolder+"\\"+fileName+".zip"):
            print("Downloading File {}".format(fileName))
            links.click()
            print("{} Downloaded!\n".format(fileName))
    links = ''
#os.times.sleep(10) 
#driver.quit()
print("All Download are completed")

