import requests
from datetime import datetime
import smtplib
import numpy as np
import time
import os

MY_LAT = 53.482790
MY_LONG = -2.337310

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
#iss_latitude = 52.482790
#iss_longitude =-2.337310
iss_longitude = float(data["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour
print(time_now.hour)
print (sunrise)
print(sunset)

my_latitude = float(MY_LAT)
my_longitude =float(MY_LONG)

def send_email():
    my_email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]

    connection = smtplib.SMTP("smtp.gmail.com")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
        to_addrs="client",
        msg=f"Subject:The ISS is here!\n\n Look up!")

def check_hour():
    if current_hour >= sunset or current_hour <= sunrise:
        return True

def check_location():
    if iss_latitude in np.arange(my_latitude, (my_latitude + 5)) or iss_latitude in np.arange((my_latitude - 5),
                                                                                              my_latitude):
        if iss_longitude in np.arange(my_longitude, (my_longitude + 5)) or iss_longitude in np.arange(
                (my_longitude - 5), my_longitude):
            return True

while True:
    if check_hour() is True:
        if check_location() is True:
            send_email()
    time.sleep(60)




