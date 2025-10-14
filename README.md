# Events-Planer

# Project Overview and Description:
 The idea of ​​our project is to help people organize their events by managing them and holding them at the time they choose and in the atmosphere they prefer.

## Tech stack
- **Html+Css:** Frontend layout and responsive styling
- **Django framework:** Backend framework handling authentication, CRUD, and routing 
- **Pillow:** Image processing and handling for uploaded event images 
- **Widget:** To improve form layouts and handle date/time pickers
- **Sqlite:** Lightweight database used for local development and testing

## For ERD and more details go to the documentation 
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
**Authentication & Accounts**
As a new user, I want to sign up with my name, email, and password so that I can create and manage my own events.

As a returning user, I want to log in securely so that I can access my previously created events.

As a logged-in user, I want to be automatically redirected to my home/events page instead of seeing the login/signup pages again.

As a user, I want to log out easily so that no one else can access my account from my device.

**Event Management**

As a user, I want to create a new event by filling in details like title, description, location, date, and theme colors so that I can organize my event properly.

As a user, I want to upload theme image for my event so that I can visualize how the setup will look.

As a user, I want to edit my event details before it starts so that I can make necessary changes in time.

As a user, I want to delete an event at least one day before it starts so that I can cancel plans if needed.

As a user, I want to see a list of all my created events sorted by date so that I can keep track of upcoming and past events.

**Event Validations & Rules**

As a user, I want to be prevented from creating an event less than 5 hours in advance so that the planners have enough time to prepare.

As a user, I want to be blocked from editing an event less than one day before it starts so that there are no last-minute changes.

**Admin & Staff Features**

As an admin, I want to view all events created by users so that I can monitor activity on the platform.

As an admin, I want to delete or update inappropriate or invalid events if needed to maintain quality wihtout having 1 day before restriction.

**User Interface & Experience**

As a user, I want to see my events displayed in a modern card-based design showing date, title, and color theme so that it’s easy to find what I need.

As a user, I want the website to be responsive so that I can manage my events from my phone or laptop.

## challenges:
Choosing the suitable assets for the project, the theme colors and some merging conflicts

## solution: 
Installed github desktop and it helped a lot with solving conflicts
