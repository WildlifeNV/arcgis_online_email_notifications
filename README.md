# Arcgis Online Email Notifications
This repo holds the script to pull data from an arcgis online account, compare the data with the stored data and email the person of interest if there is a change.

#### Requirements:  
  Anaconda  
  Arcgis Online account  
  Email account  

### How to use this repo:  
1. Clone the repo to our local machine  
  git clone https://github.com/WildlifeNV/arcgis_online_email_notifications.git  

2. Create a new file in the project directory called ".env"  
  cd arcgis_online_email_notifications && touch .env  

3. Copy the below variables to the new .env file and assign values:  
  ARCGIS_ONLINE_USERNAME =  
  ARCGIS_ONLINE_PASSWORD =  
  FEATURE_ID =  
  LAYER_NAME =  
  LAYER_ID =  
  HOST =  
  PORT =  
  EMAIL =  
  PASSWORD = 
  
 4. Use the requirements.txt to create a virtual environment and activate it:  
     conda env create -n notifications_env -f requirements.yml && conda activate notifications_env
   
 5. Run the code with the new evironment 
