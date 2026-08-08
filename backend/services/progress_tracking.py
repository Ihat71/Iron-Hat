from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.crud.user_biometrics import get_weight_and_bf_history, get_bio_history, get_weights_last_month
from backend.crud.personal_records import get_pr_history, get_pr_count
from backend.crud.exercise_history import get_exercise_history_by_exercise
from backend.crud.workout_logs import get_workouts_done, get_workout_logs_count
from backend.crud.workout_log_exercises import get_user_workout_log_exercise_by_workout
from backend.crud.workout_templates import get_workout_template_target_consistency_per_week
from backend.crud.workout_template_exercises import get_user_workout_template_exercises_by_workout_value
from collections import Counter


def get_weight_and_bf_history_service(db: Session, current_user: User):
    return get_weight_and_bf_history(db, current_user)

def get_pr_tracking_service(exercises: list[int], db: Session, current_user: User):
    return get_pr_history(exercises, db, current_user)

def get_exercise_history_service(exercise_id: int, db: Session, current_user: User):
    return get_exercise_history_by_exercise(exercise_id, db, current_user)

def get_extra_biometrics_service(db: Session, current_user: User):
    bio_history = get_bio_history(db, current_user)

    return bio_history

def get_workout_history_service(db: Session, current_user: User):
    """this func should return a count of workout logs for this month, how many were done properly according to the template, and how many were done and skipped in general."""
    res = []
    workouts_done = get_workouts_done(30, db, current_user)
    if not workouts_done:
        return []
    workouts_done_count = len(workouts_done)

    for workout in workouts_done:
        # this part is supposed to check if each logged workout is identical or close to its template counterpart (done properly)
        workout_template = db.execute(select(WorkoutTemplate).where(WorkoutTemplate.program_id == workout.program_id, WorkoutTemplate.day_number == workout.day_number)).scalars().one_or_none()
        template_exercises = get_user_workout_template_exercises_by_workout_value(db, current_user.id, workout_template.id)
        log_exercises = get_user_workout_log_exercise_by_workout(db, current_user.id, workout.id)
        is_subset = Counter(template_exercises) <= Counter(log_exercises)
        diff = Counter(log_exercises) - Counter(template_exercises)
        workout_info = workout.model_dump()
        workout_info.is_subset = is_subset
        workout_info.diff = diff
        if len(template_exercises) >= len(log_exercises):
            workout_info.did_more = False
        else:
            workout_info.did_more = True

        res.append(workout_info)

    return {'workouts' : res, 'count' : workouts_done_count}



def get_tracking_summary(program_id:int, db: Session, current_user: User):
    """This func should return data for a simple weekly and monthly summary card that also features how consistent the user and
    how many PRs he accomplished in various exercises and other stuff.
    """ 
    res = {}
    res['pr_count'] = get_pr_count(30, db, current_user)
    res['workouts_done'] = get_workout_logs_count(program_id, 30, db, current_user)
    weight_per_month = get_weights_last_month(db, current_user) # returns (weight, date), make sure it has the most recent one as last
    target_consistency = get_workout_template_target_consistency_per_week(program_id, db, current_user)
    res['latest_weight'] = weight_per_month[-1][1]
    res['weight_last_month'] = weight_per_month[0][1]
    res['lowest_weight'] = min(weight_per_month, key=lambda x: x[1])
    res['heighest_weight'] = max(weight_per_month, key=lambda x: x[1])
    res['weight_diff'] = weight_per_month[-1][1] - weight_per_month[0][1]
    res['consistency'] = res['workouts_done'] / target_consistency if target_consistency != 0 else None

    return res
    #now i just gotta figure out the consistency logic

