"""Workout domain models and tracking utilities for Iron Oak."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional


class WorkoutCategory(str, Enum):
    """Categorises a workout to drive recommendations."""

    STRENGTH = "strength"
    CARDIO = "cardio"
    MOBILITY = "mobility"


@dataclass(frozen=True)
class WorkoutDefinition:
    """Metadata describing an available workout."""

    name: str
    muscle_group: str
    category: WorkoutCategory
    suggested_sets: int
    suggested_reps: int
    youtube_url: Optional[str] = None

    def label(self) -> str:
        return f"{self.name} ({self.muscle_group})"


@dataclass
class WorkoutSet:
    """A single set performed in a workout session."""

    reps: int
    weight: float
    effort: int

    def intensity(self) -> float:
        """Simple intensity heuristic used for rest recommendations."""

        effort_scale = max(1, min(self.effort, 10))
        return self.reps * self.weight * (effort_scale / 10)


@dataclass
class WorkoutSession:
    """A performed workout consisting of multiple sets."""

    workout: WorkoutDefinition
    sets: List[WorkoutSet]
    notes: Optional[str] = None

    def total_volume(self) -> float:
        return sum(wset.reps * wset.weight for wset in self.sets)

    def average_effort(self) -> float:
        if not self.sets:
            return 0.0
        return sum(wset.effort for wset in self.sets) / len(self.sets)

    def personal_record_candidate(self) -> float:
        return max((wset.weight for wset in self.sets), default=0.0)


@dataclass
class WorkoutTracker:
    """Collects workout sessions and offers analytic summaries."""

    catalog: Dict[str, WorkoutDefinition] = field(default_factory=dict)
    sessions: Dict[str, List[WorkoutSession]] = field(default_factory=lambda: {})

    def register_workout(self, definition: WorkoutDefinition) -> None:
        self.catalog[definition.name.lower()] = definition

    def get_workout(self, name: str) -> WorkoutDefinition:
        key = name.lower()
        if key not in self.catalog:
            raise KeyError(f"Workout '{name}' not found in catalog")
        return self.catalog[key]

    def record_session(self, name: str, sets: Iterable[WorkoutSet], notes: Optional[str] = None) -> WorkoutSession:
        definition = self.get_workout(name)
        set_list = list(sets)
        if not set_list:
            raise ValueError("A workout session must contain at least one set")
        session = WorkoutSession(workout=definition, sets=set_list, notes=notes)
        self.sessions.setdefault(definition.name.lower(), []).append(session)
        return session

    def personal_record(self, name: str) -> Optional[float]:
        key = name.lower()
        if key not in self.sessions:
            return None
        return max(session.personal_record_candidate() for session in self.sessions[key])

    def total_volume(self, name: str) -> float:
        key = name.lower()
        return sum(session.total_volume() for session in self.sessions.get(key, []))

    def average_effort(self, name: str) -> Optional[float]:
        key = name.lower()
        if key not in self.sessions:
            return None
        efforts = [session.average_effort() for session in self.sessions[key]]
        return sum(efforts) / len(efforts)

    def recommend_rest(self, name: str, activity_level: str) -> str:
        """Provide a simplistic rest day recommendation."""

        volume = self.total_volume(name)
        effort = self.average_effort(name) or 0
        activity_level = activity_level.lower()
        if volume == 0:
            return "No sessions logged yet; follow suggested plan."
        if effort >= 8 or volume > 2000:
            return "High intensity recorded. Take a rest day or switch to light cardio."
        if activity_level in {"high", "athlete"}:
            return "Maintain schedule, but consider active recovery."
        if effort <= 4:
            return "Consider increasing effort or volume next session."
        return "Balanced workload. Proceed with next planned session."


def summarize_sessions(sessions: Iterable[WorkoutSession]) -> Dict[str, float]:
    """Aggregate simple stats across sessions for reporting."""

    total_volume = 0.0
    total_effort = 0.0
    count = 0
    for session in sessions:
        total_volume += session.total_volume()
        total_effort += session.average_effort()
        count += 1
    return {
        "sessions": count,
        "total_volume": total_volume,
        "avg_effort": (total_effort / count) if count else 0.0,
    }
