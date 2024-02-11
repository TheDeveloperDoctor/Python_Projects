# TODO : To Run this code automatically go check the "https://www.pythonanywhere.com/"


from datetime import datetime
import pandas
import random
import smtplib

# TODO : Change MY_EMAIL/MY_PASSWORD to your own details and also go to your email provider and make it allow less secure apps.

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

# TODO : This will fetch the current day and month

today = datetime.now()
today_tuple = (today.month, today.day)

# TODO : This will fetch the data that you have stored in Birthday.csv file if you dont update the csv file

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

# TODO : this will compare today's Date with the birthday day&Month from the dictionary

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    # TODO : open the random txt message file and replace the name tag with actual name

    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    # TODO : This will create a connection so that the message can be sent

    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )