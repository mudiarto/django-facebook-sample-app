================================
Sample Django Canvas Application
================================

This application is based loosely from "Run With Friends" sample app from facebook (http://apps.facebook.com/runwithfriends/)

I want to have & experiment with some additional features that are not available there:

  - accessible inside and outside facebook apps
  - work as personal app, and also app in a pages
  - using 3rd party login - django-social-auth 

Instruction:

  1. copy local_settings.py.template to local_settings.py
     - fill out the necessary information
     - you may need to register your app with facebook first
  2. pip -r requirements
  3. python manage.py syncdb
  4. 
