from fastapi import FastAPI
from core.logging import setup_logger
from core.config import config
from api.v1.auth import auth_router
from api.v1.profile import profile_router
from api.v1.programs import program_router
from api.v1.biometrics import biometrics_router
from api.v1.workout_templates import workout_template_exercises_router, workout_templates_router
from api.v1.workout_logs import workout_logs_router, workout_log_exercises_router
from api.v1.personal_records import personal_records_router
""" 
Let's write the requirements here cus why not

tech stack: fastapi, react, bootstrap or tailwind,

requirements:

Mandatory:

User authentication ✅ 
Workout logging ✅  
Exercise database ✅
Workout history ✅ 
PR tracking ✅
Program creation ✅
progress tracking
Progress analytics

----------------------
Good to have:

Notifications
advanced analytics
Challenges
achievements
Exercise recommendations

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
app.include_router(biometrics_router.router)
app.include_router(workout_template_exercises_router.router)
app.include_router(workout_templates_router.router)
app.include_router(workout_logs_router.router)
app.include_router(workout_log_exercises_router.router)
app.include_router(personal_records_router.router)