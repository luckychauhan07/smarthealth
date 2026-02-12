SmartHealth
AI Based Personalized Fitness and Diet Planner

About the Project

SmartHealth is a web-based health and fitness application developed using Django.
The main idea behind this project is to help users get a personalized diet and workout plan based on their body details and fitness goals.

Objectives:

To provide personalized fitness and diet plans

How to Run the Project

Step 1:
git clone https://github.com/luckychauhan07/smarthealth.git
cd smarthealth

Step 2:
python -m venv venv
venv\Scripts\activate

Step 3: 
pip install -r requirements.txt

Step 4: 
python manage.py makemigrations
python manage.py migrate

Step 5: 
python manage.py runserver

Email OTP Setup

In .evn file add:

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

Gemini API Setup:

Add your Gemini API key in .env:


Developed By

Lucky Chauhan(Team leader)
Arpit chauhan
Priyanshu garg
Nalin singh
Rajan chauhan

(Team Project – EY Training Program)
