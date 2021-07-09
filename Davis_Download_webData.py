##################################################################################################################
# This script is used to automate the download of county parcel data in various formats from different websites.
##################################################################################################################

#Import required modules
import time
import os
import urllib2
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests

#Set Output
output = (r"C:\DataDownloads")

#Get current date
current_date = (time.strftime("%m%d%Y"))


# This script requires a web driver to run, and must be downloaded prior to executing the script
# For instance, chrome webdriver (https://sites.google.com/a/chromium.org/chromedriver/downloads), or webdriver for browser of choice.
# This scripts webdriver is currently set to the chrome browser. 


#                                      **Make sure the webdriver in your PATH or else the script will fail.**
driver = webdriver.Chrome()


##################################################################################################################
# Task A: Download Denver County, CO parcel data in ESRI File Geodatabase format
##################################################################################################################
print ("\nSearching for Denver County, CO parcel geodatabase...")

#Check if the output directory for Colorado State data exists. If not, than create new directory.
Colorado = os.path.join(output, "CO")
if not os.path.exists(Colorado):
    os.makedirs(Colorado)

#Create path for Denver County parcel data export
Complete_Path_Denver = os.path.join(Colorado, "Denver_" + current_date + ".zip")

#Get URL
Denver_Parcels_GDB_service = urllib2.urlopen('https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-parcels')
Denver_Parcels_GDB_HTML = Denver_Parcels_GDB_service.read()
Denver_soup = BeautifulSoup(Denver_Parcels_GDB_HTML, "html.parser")

#Scrape site and find link to parcels gdb link. Write to file output location
with open(Complete_Path_Denver, "wb") as CPD:
    for link in Denver_soup.findAll('a', attrs={'href': re.compile("^https://.+gdb")}):
        Denver_gdb_site = link.get('href')
        print ("Found: " + Denver_gdb_site)
        CO_data = urllib2.urlopen(Denver_gdb_site)
        CO_data_write = CO_data.read()
        print ("Downloading Denver County parcel .gdb")
        CPD.write(CO_data_write)

print ("Task 'a' complete. Denver County parcel data downloaded to: " + Complete_Path_Denver)

print "\n------------------------------------------------------------------------------------------------------------------------------------------------\n"



##################################################################################################################
# Task B: Download Pitkin County, CO parcel data in ESRI File Geodatabase format
##################################################################################################################

print ("Searching for Pitkin County, CO parcel geodatabase...")

#Create path for Pitkin County parcel data export
Complete_Path_Pitkin = os.path.join(Colorado, "Pitkin_" + current_date + ".zip")

#Get URL
Pitkin_Parcels_GDB_service = urllib2.urlopen('http://co-pitkincounty2.civicplus.com/875/Land-Records')
Pitkin_Parcels_GDB_HTML = Pitkin_Parcels_GDB_service.read()
Pitkin_soup = BeautifulSoup(Pitkin_Parcels_GDB_HTML, "html.parser")

#Scrape site and find link to parcels gdb link. Write to file output location
with open(Complete_Path_Pitkin, "wb") as CPP:
    for link in Pitkin_soup.findAll('a', attrs={'href': re.compile("^https://.+ParcelBoundary/gdb")}):
        Pitkin_gdb_site = link.get('href')
        print ("Found: " + Pitkin_gdb_site)
        CO_data = urllib2.urlopen(Pitkin_gdb_site)
        CO_data_write = CO_data.read()
        print ("Downloading Pitkin County parcel gdb")
        CPP.write(CO_data_write)

print ("Task 'b' complete. Pitkin County, CO Parcel data downloaded to: " +  Complete_Path_Pitkin)

print "\n------------------------------------------------------------------------------------------------------------------------------------------------\n"

##################################################################################################################
# Task C: Download Sedgwick County, KS property parcel data
##################################################################################################################
print ("Searching for Sedgwick County, KS property parcel data...")

#Web address for the data site
url = "http://gis.sedgwick.gov/gisdata/default.asp"

#initialize webdriver
driver.get(url)

# wait till the web page is fully loaded
time.sleep(8)

# make the dropdown options available, and select Parcel data
select = Select(driver.find_element_by_name('Property Data'))
select.select_by_value('Property Parcels')

# scrape the page in its current state and close browser
content = driver.page_source.encode('utf-8').strip()

# Use BeaurifulSoup to scrape the page data
soup = BeautifulSoup(content,"html.parser")

# get only things with "li" (list) tags
td_tags = soup.find_all("td")


# get a list of tags that have a zip file path in them
# create empty list
zip_tags = []

for n in td_tags:
    #print(n)
    s = str(n.contents)
    
    if "Parcel.zip" in s:
        zip_tags.append(s)
        continue

# Get the full string, including the link
full_string = zip_tags[3]

# Split full string to get the link
base_link = re.search("\'/(.*)\',", full_string)
link_url = base_link.group(1)
base_path = "http://gis.sedgwick.gov/"
full_path = os.path.join(base_path,link_url)
# Join link to base path
    
#Check if the output directory for Kansas State data exists. If not, than create new directory.
Kansas = os.path.join(output, "KS")
if not os.path.exists(Kansas):
    os.makedirs(Kansas)

#Create path for Sedgwick County parcel data export
Complete_Path_Sedgwick = os.path.join(Kansas, "Sedgwick_" + current_date + ".zip")

# This site requires that you request the URL
r = requests.get(full_path)

#Scrape site and find link to parcels gdb link. Write to file output location
with open(Complete_Path_Sedgwick, "wb") as Sedgwick:
    print ("Downloading Sedgwick County parcel gdb")
    Sedgwick.write(r.content)

print ("Task 'c' complete. Sedgwick County, KS Parcel data downloaded to: " +  Complete_Path_Sedgwick)

print "\n------------------------------------------------------------------------------------------------------------------------------------------------\n"


##################################################################################################################
# Task D: Download Madison County, Idaho property parcel shapefile
##################################################################################################################

print ("Searching for Madison County, Idaho property parcel shapefile...")

#Web address for the data site
url = "https://data-mrgis.opendata.arcgis.com/datasets/madison-county-parcels-live"

#initialize webdriver
driver.get(url)

# wait till the web page is fully loaded
time.sleep(8)

# make the dropdown options available for scraping
element = driver.find_element_by_id('download-button')
element.click()

# scrape the page in its current state and close browser
content = driver.page_source.encode('utf-8').strip()
driver.close()

# Use BeaurifulSoup to scrape the page data
soup = BeautifulSoup(content,"html.parser")

# Find everything with "li" (list) tags
li_tags = soup.find_all("li")

# create empty list
zip_tags = []

# get a list of li tags that have a zip file path in them
for n in li_tags:
    s = str(n.contents[0])
    
    if ".zip" in s:
        zip_tags.append(s)

#Find our download link using regex
for n in zip_tags:
    result = re.search('href="(.*)" id', n)
    dwnld_url = result.group(1)

#Check if the output directory for Idaho State data exists. If not, than create new directory.
Idaho = os.path.join(output, "ID")
if not os.path.exists(Idaho):
    os.makedirs(Idaho)

#Create path for Madison County parcel data export
Complete_Path_Madison = os.path.join(Idaho, "Madison_" + current_date + ".zip")

#Read and Write download to file output location
with open(Complete_Path_Madison, "wb") as Madison:
    ID_data = urllib2.urlopen(dwnld_url)
    ID_data_write = ID_data.read()
    print ("Downloading Madison County, ID parcel shapefile")
    Madison.write(ID_data_write)


print ("Task 'd' complete. Madison County, ID Parcel data shapefile downloaded to: " +  Complete_Path_Madison)

print ("\nScript execution complete")