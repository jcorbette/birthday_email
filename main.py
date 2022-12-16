#import all required modules
import pandas as pd
import datetime as dt
import random
import os
import ssl
import smtplib
from bs4 import BeautifulSoup
import re
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#set today's date
today = dt.datetime.now()
date = today.day
month = today.month
year = today.year
week_day = today.strftime('%A')
month_name = today.strftime("%B")
day_tuple = (month, date) #tuple with today's month and day



#function to create email from html template
def create_Email(name, relation, w_day, month, b_day, b_year, age, sender):
        
        
        #select random background colour for email
        r = random.randint(130,255)
        g = random.randint(0,130)
        b = random.randint(0,255)
        birthday_email_background_colour = (r,g,b)       
    
        
        #open files containing list of birthday greetings and email html template       
        with open('birthday_greetings.txt', 'r', encoding="UTF-8") as greetings_file, open("email_template.html", 'r', encoding="UTF-8") as email_template_file:
              
            #select random birthday greeting quote       
            all_greetings = greetings_file.readlines()
            greeting = random.choice(all_greetings)       

            
            email_content = email_template_file.read()
            
            
            #use BeautifulSoup to parse through html template and replace placeholder text
            soup = BeautifulSoup(email_content, 'html.parser')            
            
            name_target = soup.find_all(text=re.compile(r'[NAME]'))    
            for n in name_target:
                n.replace_with(n.replace('[NAME]', name))
                
            relation_target = soup.find_all(text=re.compile(r'[RELATION]'))    
            for rl in relation_target:
                rl.replace_with(rl.replace('[RELATION]', relation))
                
            weekday_target = soup.find_all(text=re.compile(r'[WEEKDAY]'))    
            for w in weekday_target:
                w.replace_with(w.replace('[WEEKDAY]', w_day))
                
            month_target = soup.find_all(text=re.compile(r'[MONTH]'))    
            for m in month_target:
                m.replace_with(m.replace('[MONTH]', month))
            
            date_target = soup.find_all(text=re.compile(r'[DATE]'))    
            for d in date_target:
                d.replace_with(d.replace('[DATE]', str(b_day)))
                
            year_target = soup.find_all(text=re.compile(r'[YEAR]'))    
            for y in year_target:
                y.replace_with(y.replace('[YEAR]', str(b_year)))
                
            age_target = soup.find_all(text=re.compile(r'[AGE]'))    
            for a in age_target:
                a.replace_with(a.replace('[AGE]', str(age)))
                
            greeting_target = soup.find_all(text=re.compile(r'[GREETING]'))    
            for gr in greeting_target:
                gr.replace_with(gr.replace('[GREETING]', greeting))
                
            sender_target = soup.find_all(text=re.compile(r'[SENDER]'))    
            for s in sender_target:
                s.replace_with(s.replace('[SENDER]', sender))
                
            for tag in soup.findAll(attrs={"class": "background"}):
                tag["style"] = f"background-color: rgb{birthday_email_background_colour};"
        
        
        #save updated html as new file        
        with open(f'{person_name}_birthday_email.html', 'w+', encoding="UTF-8") as personal_html:
            personal_html.write(str(soup))        
           
        with open(f'{person_name}_birthday_email.html', 'r', encoding="UTF-8") as personal_html_file:
            personal_html_content = personal_html_file.read()
        
        #return content of personalized html file
        return personal_html_content
        



#function to send email to person
def send_Email():
    
    #set email login/sender info 
    sender_email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    sender_name = "Your Name"
    
    #start new message object 
    em = MIMEMultipart()
    del em["To"]
    em["To"] = person_email
    em["From"] = sender_email
    email_subject = f"IT'S YOUR BIRTHDAY! YOU'RE NOW {person_age}"
    em["Subject"] = email_subject
    

    #set result of create_Email function as written email content
    written_email = create_Email(person_name, person_relation, week_day, month_name, date, year, person_age, sender_name)
    em.attach(MIMEText(written_email, "html")) 
    
    #open and set image content ID 
    with open("balloons.png", 'rb') as image:
        background_image = MIMEImage(image.read())
    background_image.add_header("Content-ID", "<b-img>")#image id to reference in html div    
    em.attach(background_image)#attach image to message
        
    
    #set port for SMTP over TLS
    port = 465
            
    context = ssl.create_default_context()        
    
    #start SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        
        server.login(sender_email, password)
        print("\nLogged in successfully\n")    

        server.send_message(em)
        print(f"Your message was sent to {person_email}\n")
    
    #delete the personalized html file   
    os.remove(f'{person_name}_birthday_email.html')




#open file with data on individuals using pandas and convert from dataframe to dictionaries  
birthday_data = pd.read_csv("birthday_list.csv")
birthday_data_dict = birthday_data.to_dict(orient='records')


#iterate through list of dictionaries
for dic in birthday_data_dict:   
    
    #iterate through each key value representing person's info and assign it to variable
    for key in dic:        
        person_name = dic["Name"]
        person_relation = dic["Relation"]
        person_birthday = (dic["Birth_Month"], dic["Birth_Day"])
        person_birth_year = dic["Birth_Year"]
        person_email = dic["Email"]
        person_age = year - person_birth_year    
        
    #send email if person's birthday matches the tuple with current date   
    if person_birthday == day_tuple:
        send_Email()
