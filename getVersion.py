import json
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_secrets():
    with open('environment.json') as secrets_file:
        secrets = json.load(secrets_file)

    return secrets

secrets = get_secrets()

versionNumber = '8.5.6.0'


API_KEY = secrets["API_Key"]
email_user = secrets["email_user"]
email_pass = secrets["email_pass"]
mail_to_user = secrets["mail_to"]
smtp_server = secrets["smtp_server"]
smtp_port = secrets["smtp_port"]

username = email_user
password = email_pass
mail_from = email_user
mail_to = mail_to_user
mail_subject = "UDM controller versions"
mail_body = "Test message"

mail_msg = ''

headers = {'X-API-KEY': '8WeM6kVfGu7G7pVetn4logrw-TEdY6wN'}

response = requests.get('https://api.ui.com/ea/hosts', headers=headers)

data = response.json()
sites = data["data"]
ipaddresses = secrets["controller_IPs"]

for site in sites:
    if site['ipAddress'] in ipaddresses:
        #   controller
        print()
    else:
        #   UDM
        controllers = site["reportedState"]["controllers"]
        try:
            siteName = site["reportedState"]["hostname"]
            print("Site:",siteName)
            # mail_msg = mail_msg + "Site: " + str(siteName) + "\n" 
            versionNum = controllers[0]["uiVersion"]
            print("Version:", versionNum + "\n")
            if versionNum != versionNumber:
                mail_msg = mail_msg + "Site: " + str(siteName) + "\n"
                mail_msg = mail_msg + "Version: " + str(versionNum) + "\n\n"
            
        except:
            siteName = site["reportedState"]["hostname"]
            print("Site:", siteName)
            # mail_msg = mail_msg + "Site: " + str(siteName) + "\n" 
            versionNum = controllers[0]["version"]
            print("Version:", versionNum + "\n")
            if versionNum != versionNumber:
                mail_msg = mail_msg + "Site: " + str(siteName) + "\n" 
                mail_msg = mail_msg + "Version: " + str(versionNum) + "\n\n"
            print("ERROR!!!")

mimemsg = MIMEMultipart()
mimemsg['From'] = mail_from
mimemsg['To'] = mail_to
mimemsg['Subject'] = mail_subject
mimemsg.attach(MIMEText(mail_msg, 'plain'))
connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
connection.starttls()
connection.login(username, password)
connection.send_message(mimemsg)
connection.quit()