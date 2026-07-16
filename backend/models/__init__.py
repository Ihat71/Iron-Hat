# backend/models/__init__.py
from models.user import User
from models.exercises import Exercises
from models.exercise_history import ExerciseHistory
from models.personal_records import PersonalRecords
from models.workout_log_exercises import WorkoutLogExercise
from models.program_templates import ProgramTemplates
from models.workout_templates import WorkoutTemplate
from models.workout_logs import WorkoutLog
from models.workout_template_exercises import WorkoutTemplateExercise

__all__ = ["User", "WorkoutLog", "WorkoutLogExercise","Exercises", "ExerciseHistory", "PersonalRecords", "ProgramTemplates", "WorkoutTemplate", "WorkoutTemplateExercise"]