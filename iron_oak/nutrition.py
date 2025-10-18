"""Nutrition planning and logging utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class MacroTarget:
    calories: int
    protein: int
    carbs: int
    fats: int

    def as_ratio(self) -> Dict[str, float]:
        total = self.protein + self.carbs + self.fats
        if total == 0:
            return {"protein": 0.0, "carbs": 0.0, "fats": 0.0}
        return {
            "protein": self.protein / total,
            "carbs": self.carbs / total,
            "fats": self.fats / total,
        }


@dataclass
class NutritionEntry:
    """Represents a daily nutrition log entry."""

    calories_in: int
    calories_out: int
    protein: int
    carbs: int
    fats: int
    notes: Optional[str] = None

    def net_calories(self) -> int:
        return self.calories_in - self.calories_out


@dataclass
class NutritionTracker:
    """Collects nutrition entries and compares against macro targets."""

    target: MacroTarget
    entries: List[NutritionEntry] = field(default_factory=list)

    def log_entry(self, entry: NutritionEntry) -> None:
        self.entries.append(entry)

    def totals(self) -> Dict[str, int]:
        total_calories_in = sum(entry.calories_in for entry in self.entries)
        total_calories_out = sum(entry.calories_out for entry in self.entries)
        total_protein = sum(entry.protein for entry in self.entries)
        total_carbs = sum(entry.carbs for entry in self.entries)
        total_fats = sum(entry.fats for entry in self.entries)
        return {
            "calories_in": total_calories_in,
            "calories_out": total_calories_out,
            "net_calories": total_calories_in - total_calories_out,
            "protein": total_protein,
            "carbs": total_carbs,
            "fats": total_fats,
        }

    def average_day(self) -> Optional[Dict[str, float]]:
        if not self.entries:
            return None
        totals = self.totals()
        days = len(self.entries)
        return {key: value / days for key, value in totals.items()}

    def macro_balance(self) -> Optional[Dict[str, float]]:
        if not self.entries:
            return None
        totals = self.totals()
        total_macros = totals["protein"] + totals["carbs"] + totals["fats"]
        if total_macros == 0:
            return {"protein": 0.0, "carbs": 0.0, "fats": 0.0}
        return {
            "protein": totals["protein"] / total_macros,
            "carbs": totals["carbs"] / total_macros,
            "fats": totals["fats"] / total_macros,
        }

    def optimization_insights(self, bmi: float, resting_hr: int, workout_days: int) -> Dict[str, str]:
        """Provide simple heuristics for macro optimisation."""

        ratio = self.macro_balance() or self.target.as_ratio()
        suggestions: Dict[str, str] = {}
        if bmi > 27:
            suggestions["calories"] = "Slight calorie deficit recommended. Aim for 250-350 kcal below maintenance."
        elif bmi < 19:
            suggestions["calories"] = "Consider a mild surplus to support healthy weight gain."
        else:
            suggestions["calories"] = "Calories on track for maintenance."

        if resting_hr > 80:
            suggestions["cardio"] = "Introduce additional low-intensity cardio to improve heart health."
        elif resting_hr < 55:
            suggestions["cardio"] = "Resting heart rate excellent; maintain current cardio frequency."
        else:
            suggestions["cardio"] = "Cardio volume is adequate."

        protein_ratio = ratio["protein"]
        if workout_days >= 4 and protein_ratio < 0.3:
            suggestions["protein"] = "Increase protein intake to support recovery (target 30-35% of macros)."
        elif workout_days <= 2 and protein_ratio > 0.4:
            suggestions["protein"] = "Current protein high relative to activity; balance with more carbs."
        else:
            suggestions["protein"] = "Protein balance aligned with activity level."
        return suggestions


def combine_trackers(trackers: Iterable[NutritionTracker]) -> Dict[str, float]:
    """Aggregate totals across multiple nutrition trackers (e.g., for analytics)."""

    totals = {"calories_in": 0.0, "calories_out": 0.0, "net_calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}
    for tracker in trackers:
        tracker_totals = tracker.totals()
        for key, value in tracker_totals.items():
            totals[key] += value
    return totals
