"""
Small, explicit builders for model instances that need a lot of required
columns filled in (like Exercises) so individual tests don't have to repeat
that boilerplate. These are plain functions, not a framework -- add more
here as new tests need them, following the same `build_*` / `persist_*`
naming split:

- `build_x(**overrides)` returns an unsaved model instance.
- `persist_x(session, **overrides)` builds it, adds it, commits, and
  returns the refreshed instance -- use this one from tests unless you
  specifically need to control the commit yourself.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.exercises import Exercises


def build_exercise(**overrides) -> Exercises:
    defaults = dict(
        name="Barbell Back Squat",
        equipment="barbell",
        is_variation="false",
        utility_type="basic",
        mechanics_type="compound",
        force_type="push",
        target_muscles="quadriceps",
        main_muscle="quadriceps",
        secondary_muscles="glutes",
        difficulty=3,
        synergist_muscles="hamstrings",
        stabilizer_muscles="core",
        antagonist_muscles="hamstrings",
        dynamic_stabilizer_muscles="none",
    )
    defaults.update(overrides)
    return Exercises(**defaults)


async def persist_exercise(session: AsyncSession, **overrides) -> Exercises:
    exercise = build_exercise(**overrides)
    session.add(exercise)
    await session.commit()
    await session.refresh(exercise)
    return exercise
