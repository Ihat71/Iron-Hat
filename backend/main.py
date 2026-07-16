from fastapi import FastAPI
from core.logging import setup_logger
from core.config import config
from api.v1.auth import auth_router
from api.v1.profile import profile_router
from api.v1.programs import program_router
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

app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(program_router.router)



