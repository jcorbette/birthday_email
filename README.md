# BIRTHDAY EMAIL PYTHON SCRIPT

## About the Project

This is a python script that runs once a day. It pulls data from a csv file with info about persons (names, ralation, birthday, email) and then checks to see if the person's date of birth matches the current date. If it does, an email with a personalized birthday greeting is sent. 

**Languages used:** Python, HTML, CSS

#### Required Python Modules:
- pandas
- datetime
- random
- os (if you use environment variables to get user and password)
- ssl
- smtplib
- BeautifulSoup from bs4
- re
- MIMEMultipart, MIMEImage and MIMEText from email

#### Other Required Files:
- html email template file
- csv file with person data
- text file with birthday greetings
- png image

#### Decsription of how the script works:
- checks current date
- opens csv to get person data using pandas
- converts data to dictionaries
- loops through dictionaries and each dictionary key value to get info for each person
- if person birthday matches current date then function to create email is called
- create email function selects random background colour for email, opens text file with birthday greetings and opens html file with styled email template
- random birthday quote is chosen from text file
- html is parsed and placeholder text replaced with person info and other details
- edited html file is saved and is then read to return that content for create email function
- send email function then creates a new email object and attaches the email content and a png image
- secure SMTP server is started and email is sent using sender login info
- the personalized html file that was created is then deleted
- loop starts over for each person whose birthday it is

#### Project Images
![Sample Image of Email on PC](/screenshots/Screenshot_1.jpeg?raw=true "Sample Image of Email on PC")
![Sample Image of Email on Mobile 1](/screenshots/Screenshot_2.jpg?raw=true "Sample Image of Email on Mobile 1")
![Sample Image of Email on Mobile 2](/screenshots/Screenshot_3.jpg?raw=true "Sample Image of Email on Mobile 2")
![Sample Image of Email on Mobile 3](/screenshots/Screenshot_4.jpg?raw=true "Sample Image of Email on Mobile 3")

#### Resources:
Link for website with birthday greetings/quotes used in project - https://www.shutterfly.com/ideas/happy-birthday-quotes/
