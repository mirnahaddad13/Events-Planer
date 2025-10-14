# Events-Planer

# Project Overview and Description:
 The idea of ​​our project is to help people organize their events by managing them and holding them at the time they choose and in the atmosphere they prefer.

## Tech stack
- **Html+Css:** Frontend layout and responsive styling
- **Django framework:** Backend framework handling authentication, CRUD, and routing 
- **Pillow:** Image processing and handling for uploaded event images 
- **Widget:** To improve form layouts and handle date/time pickers
- **Sqlite:** Lightweight database used for local development and testing

## for ERD and more details go to the documentation 
* https://docs.google.com/document/d/1FlKjheZPNa6BRKFPlfH2y7pYXh5wJe1bT3QVDVCSGqk/edit?usp=sharing

## Key Features
- **User Authentication:** Sign up, log in, and log out securely  
- **Event Management:** Create, update, and delete personal events  
- **Image Uploads:** Add one image per event  
- **Validation Rules:** Prevents scheduling past events or updates too close to event start  
- **User-Specific Data:** Each user can only see their own events  
- **Events List:** Sorted by creation date with easy navigation and admins can see all client events 

## setup:
git clone https://github.com/{{username}}/Events-Planer.git
cd Events-Planer
**MaxOs/Linux**
python3 -m venv venv
source venv/bin/activate

**Windows**
py -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make and apply migrations
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver

# Create a superuser for admin access:
python manage.py createsuperuser

## user stories:

## challenges:
Choosing the suitable assets for the project, the theme colors and some merging conflicts

## solution: 
Installed github desktop and it helped a lot with solving conflicts
