import logging
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.models.exercises import Exercises
from backend.core.database import SessionLocal

PROCESSED_PATH = ROOT / "data" / "processed" / "exercises.json"
LOG_DIR = ROOT / "scripts" / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def parse_parent_index(value) -> int | None:
    """Return the dataset row index for a variation's parent, or None."""
    if value is None or pd.isna(value):
        return None
    return int(value)


def load() -> list[dict]:
    df = pd.read_json(PROCESSED_PATH)
    exercises = df.to_dict(orient="records")

    for exercise in exercises:
        exercise["parent_index"] = parse_parent_index(exercise.pop("parent_id"))

    return exercises


def seed(db: Session, exercises: list[dict]) -> None:
    try:
        logger.info("Loaded %d exercises", len(exercises))

        created: list[Exercises] = []

        for exercise in exercises:
            db_exercise = Exercises(
                name=exercise["name"],
                equipment=exercise["equipment"],
                is_variation=exercise["variation"],
                utility_type=exercise["utility"],
                mechanics_type=exercise["mechanics"],
                force_type=exercise["force"],
                target_muscles=exercise["target_muscles"],
                main_muscle=exercise["main_muscle"],
                secondary_muscles=exercise["secondary_muscles"],
                difficulty=int(exercise["difficulty"]),
                synergist_muscles=exercise["synergist_muscles"],
                stabilizer_muscles=exercise["stabilizer_muscles"],
                antagonist_muscles=exercise["antagonist_muscles"],
                dynamic_stabilizer_muscles=exercise["dynamic_stabilizer_muscles"],
            )
            db.add(db_exercise)
            created.append(db_exercise)

        db.flush()

        for db_exercise, exercise in zip(created, exercises):
            parent_index = exercise["parent_index"]
            if parent_index is not None:
                db_exercise.parent_id = created[parent_index].id

        db.commit()
        logger.info("Successfully seeded exercises")

    except Exception:
        db.rollback()
        logger.exception("Exercise seeding failed")
        raise


def main() -> None:
    db = SessionLocal()
    exercises = load()

    try:
        seed(db, exercises)
    finally:
        db.close()


if __name__ == "__main__":
    main()
