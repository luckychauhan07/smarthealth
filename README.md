SmartHealth
      AI Based Personalized Fitness and Diet Planner

About the Project

      SmartHealth is a web-based health and fitness application developed using Django.
      The main idea behind this project is to help users get a personalized diet and workout plan based on their body details and fitness goals.
      Nowadays, many people want to stay fit but don’t know which diet or exercise plan is suitable for them. So, we built this system which uses Google Gemini AI to generate customized fitness recommendations.
      This project was developed as part of our B.Tech Third Year academic project / EY Training Program.

Objectives:

      To provide personalized fitness and diet plans
      
      To calculate BMI automatically
      
      To use AI for generating smart health suggestions
      
      To create a simple and user-friendly health platform

Technologies Used:
  Frontend

      HTML
      
      Tailwind CSS
      
      JavaScript
      
  Backend
      
      Python
      
      Django Framework
      
  Database
      
      MySQL
      
  External Packages
      
      google-generativeai (for Gemini API)

Features

      User Registration and Login
      
      Email OTP Verification
      
      BMI Calculation on landing page
      
      AI-Based Diet Plan Generation
      
      AI-Based Workout Plan Generation
      
      Personalized Dashboard
      
      Secure Authentication System
      
      Responsive UI

Project Structure
      smarthealth/
      │
      ├── smarthealth/       # Main project settings
      ├── accounts/          # Authentication & OTP
      ├── planner/           # AI diet & workout logic
      ├── dashboard/         # User dashboard
      ├── templates/         # HTML files
      ├── static/            # CSS & JS files
      └── manage.py


How to Run the Project

Step 1: Clone the repository
      git clone https://github.com/luckychauhan07/smarthealth.git
      cd smarthealth

Step 2: Create virtual environment
      python -m venv venv
      venv\Scripts\activate

Step 3: Install dependencies
      pip install -r requirements.txt

Step 4: Apply migrations
      python manage.py makemigrations
      python manage.py migrate

Step 5: Run the server
      python manage.py runserver


Open in browser:

      http://127.0.0.1:8000/


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


How the System Works

      User registers on the platform
      
      Email OTP verification is completed
      
      User enters personal health details
      
      System calculates BMI
      
      Data is sent to Gemini AI
      
      AI generates diet and workout plan
      
      User can view everything on dashboard

Future Improvements

      Progress tracking system
      
      Weekly report generation
      
      Mobile app version
      
      Integration with smart bands
      
      Advanced analytics

Developed By

      Lucky Chauhan(Team leader)
      Arpit chauhan
      Priyanshu garg
      Nalin singh
      Rajan chauhan

(Team Project – EY Training Program)
