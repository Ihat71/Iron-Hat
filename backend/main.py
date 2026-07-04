from fastapi import FastAPI
from backend.core.logging import setup_logger
from backend.core.config import config

""" 
Let's write the requirements here cus why not

tech stack: fastapi, react, bootstrap or tailwind,

requirements:

Mandatory:

User authentication
Workout logging
Exercise database
Workout history
PR tracking 
Program creation
Progress analytics
Challenges
achievements
----------------------
Good to have:

Notifications
advanced analytics

----------------------

superflous but should still do:

Friend system
groups and communities
social poking features
"""
setup_logger() #in other files write 'logger = get_logger(__name__)'

app = FastAPI(title="Iron-Hat's API")

@app.get("/")
def root():
    return {"message": "welcome to Iron Hat"}

#this function allows users to log their workouts day-to-day and check history of each lift if needed
@app.get("/logging")
def logging():
    return {"message": "sup nerd"}

#this function allows users to create their own programs
@app.get("/program")
def program():
    return ...

#this function allows users to login to their accounts or create an account
@app.get("/login")
def login():
    return ...

