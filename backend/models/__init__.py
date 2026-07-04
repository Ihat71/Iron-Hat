# backend/models/__init__.py
from backend.models.user import User
from backend.models.workouts import Workouts
from backend.models.exercises import Exercises
from backend.models.exercise_history import ExerciseHistory
from backend.models.personal_records import PersonalRecords
from backend.models.workout_exercises import WorkoutExercises

__all__ = ["User", "Workouts", "WorkoutExercises","Exercises", "ExerciseHistory", "PersonalRecords"]