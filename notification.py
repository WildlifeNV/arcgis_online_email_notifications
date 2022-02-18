import os, arcgis, smtplib
from decouple import config
from zipfile import ZipFile
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

feature_layer_id = config("FEATURE_ID")

gis = arcgis.GIS(None, username=config("ARCGIS_ONLINE_USERNAME"), password=config("ARCGIS_ONLINE_PASSWORD"))
data = gis.content.get(feature_layer_id)

name = data.title
csv = data.export(title=name, export_format="csv", parameters=None, wait=True)
export_path = csv.download(save_path="data")
csv.delete()

folder_path = "data/{}".format(name.replace(" ", "_").lower())
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

zipped_file = ZipFile(export_path)
zipped_file.extractall(folder_path)
zipped_file.close()
os.remove(export_path)

def clear_new_data(path):
    for clean_up in os.listdir(path):
        if not clean_up.endswith("current_data.csv"):    
            os.remove(os.path.join(folder_path, clean_up))

def send_email(path):
    df_attachment = pd.read_csv(path, index_col=0)
    recipients = ["ian.holl@ndow.org"]
    email_list = [elem.strip().split(",") for elem in recipients]
    
    msg = MIMEMultipart()
    msg["Subject"] = "Updates for {}".format(name)
    msg["From"] = "Your Friendly Neighborhood GIS folks"

    html = """\
    <html>
      <head></head>
      <body>
        <p>Here is a list of new records that have been add:</p>
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
    print("email successfully sent")

current_data = os.path.join(folder_path, "current_data.csv")
new_data = os.path.join(folder_path, "Mortality_Reporting_Form_0.csv")

if os.path.exists(current_data):
    current_df = pd.read_csv(current_data)
    new_df = pd.read_csv(new_data)
    compare_df = current_df.equals(new_df)
    
    if compare_df == True:
        print("data is the same, no need to email or update current data")
    else:
        new_records = new_df.loc[~new_df['ObjectID'].isin(current_df['ObjectID'])].copy()
        path = os.path.join(folder_path, "new_records.csv")
        new_records.to_csv(path)
        send_email(path)   
else:
    os.rename(new_data, current_data)
    clear_new_data(folder_path)
    print("this is a new data set, set the new data to the current")