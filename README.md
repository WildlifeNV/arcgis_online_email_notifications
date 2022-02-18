# Arcgis Online Email Notifications
This repo holds the script to pull data from an arcgis online account, compare the data with the stored data and email the person of interest if there is a change.

Requirements:
  Arcigs Online account
  Email account

How to use this repo:
1. Clone the repo to our local machine

2. Create a new file in the project directory ".env"

3. Copy the following configuration variables names below and add our own data/n
  ARCGIS_ONLINE_USERNAME = /n
  ARCGIS_ONLINE_PASSWORD = /n
  FEATURE_ID = /n

  HOST = /n
  PORT = /n

  EMAIL = /n 
  PASSWORD = /n 
  
 4. Use the requirements.txt to create a virtual environment 
 
 5. Run the code
