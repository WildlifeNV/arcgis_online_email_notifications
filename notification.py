import os, arcgis, smtplib
from decouple import config
from zipfile import ZipFile
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# log into arcigs online account and export the required feature layer to a csv in the users arcgis online content
feature_layer_id = config("FEATURE_ID")
gis = arcgis.GIS(None, username=config("ARCGIS_ONLINE_USERNAME"), password=config("ARCGIS_ONLINE_PASSWORD"))
data = gis.content.get(feature_layer_id)
name = data.title
csv = data.export(title=name, export_format="csv", parameters=None, wait=True)

# check for the data directory if not create one, download the csv, and remove it
if not os.path.exists("data"):
    os.mkdir("data")
export_path = csv.download(save_path="data")
csv.delete()

# check if there is a folder based on the feature title to store the data and create one if not
folder_path = "data/{}".format(name.replace(" ", "_").lower())
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

# extract the csv files from the downloaded zipfile and delete the zipped file
zipped_file = ZipFile(export_path)
zipped_file.extractall(folder_path)
zipped_file.close()
os.remove(export_path)

# remove all the files in a folder except for the current data (param: path to folder to remove files from)
def clear_new_data(path):
    for clean_up in os.listdir(path):
        if not clean_up.endswith("current_data.csv"):    
            os.remove(os.path.join(folder_path, clean_up))

# create an email, add the new records dataframe to the body of the email and send email
def send_email(path):
    df = pd.read_csv(path, index_col=0)
    df_attachment = df[["ObjectID", "First Name:", "Last Name:", "Email:", "Date:", "Location Specifics:", "Location Description:", "x", "y"]]
    recipients = ["ian.holl@ndow.org"]
    email_list = [elem.strip().split(",") for elem in recipients]
    
    msg = MIMEMultipart()
    msg["Subject"] = "Updates for {}".format(name)
    msg["From"] = "Your Friendly Neighborhood GIS folks"

    html = """
    <html>
      <head></head>
      <body>
        <p>You are receiving this email becuase there are new submissions to the Wildlife Mortality Tracking Form./n
        If you wish to unsubcribe from this list please notify the Nevada Department of Wildlife GIS staff.</p>
        <p>Here is a list of new records that have been added in the past 24 hours:</p>
        {0}
      </body>
    </html>
    """.format(df_attachment.to_html())

    part1 = MIMEText(html, "html")
    msg.attach(part1)

    server = smtplib.SMTP(host=config("HOST"), port=config("PORT"))
    server.starttls()
    server.login(config("EMAIL"), config("PASSWORD"))
    server.sendmail(msg["From"], email_list, msg.as_string())

# set the new and current data csvs
current_data = os.path.join(folder_path, "current_data.csv")
feature = "{}_{}.csv".format(config("FEATURE_NAME"), config("FEATURE_NUMBER")).replace(" ", "_")
new_data = os.path.join(folder_path, feature)

# if current data is not avaliable, create current data and remove files 
if os.path.exists(current_data):
    current_df = pd.read_csv(current_data)
    new_df = pd.read_csv(new_data)
    compare_df = current_df.equals(new_df)
    
    # if true remove files, else create csv, send email, update current data and remove files
    if compare_df == True:
        clear_new_data(folder_path)
        print("Data is the same, no need to update, and remove the new files")
    else:
        new_records = new_df.loc[~new_df["ObjectID"].isin(current_df["ObjectID"])].copy()
        output_path = os.path.join(folder_path, "new_records.csv")
        new_records.to_csv(output_path)
        send_email(output_path)
        os.rename(new_data, current_data)
        clear_new_data(folder_path)
        print("Email sent successfully and current data updated")   
else:
    os.rename(new_data, current_data)
    clear_new_data(folder_path)
    print("New dataset, creating current data for future comparisons")