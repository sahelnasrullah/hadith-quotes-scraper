
#Install these modules if you haven't already (pip install bs4, pip install requests etc...)
from bs4 import BeautifulSoup
import requests
from time import time
import random 
import smtplib
from email.mime.text import MIMEText

server_email = "email_to_send_from@example.com"
server_password = "password_to_the_email_you're_sending_from"

#The URL you want to scrape
url = "https://sunnah.com/riyadussalihin/introduction"

# Scraping for hadiths
def scrape(url):
    response = requests.get(url)
    # The tag name
    tag = "div"
    # The class name of the tag
    class_details = "text_details"
    if response.status_code == 200:
        lst_of_hadiths = []
        soup = BeautifulSoup(response.text, "html.parser")

        hadiths = soup.find_all(tag, class_=class_details)
        for hadith in hadiths:
            lst_of_hadiths.append(hadith.text)
    else:
        return None
    return lst_of_hadiths

# Scraping multiple pages
def scrape_pages():
    for times in range(0,20):
        url_ = url.split("introduction")[0]
        url_ = url_+ str(times)
        if times == 0:
            scrape(url)
        else:
            scrape(url_)
            time.sleep(3)

def get_random_hadith():
    return random.choice(scrape(url))

def users():
    # Add as many users as needed
    users_info = [
        {'email': 'usertosendto@example.com'},
        {'email': 'usertosendto2@example.com'},
        {'email': 'usertosendto3@example.com'}
    ]
    return users_info

# Sending the hadith
def send_email(sender_email, sender_password, recipient_email, subject, message):
    smtp_server =  'smtp.office365.com' #If you're not using outlook change this
    smtp_port = 587
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    sender_password = server_password

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(server_email, sender_password)
        server.send_message(msg)

# Main program
def main():
    hadith = get_random_hadith()
    users_info = users()

    # Sending to every user added in users
    for user in users_info:
        email = (user["email"])
        subject = "A hadith a day"
        send_email(server_email,server_password,email,subject,hadith)
        print("Hadith sent!")

if __name__ == "__main__":
    main()
