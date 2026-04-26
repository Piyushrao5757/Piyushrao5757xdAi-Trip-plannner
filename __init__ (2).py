"""
Recommendation Engine - Hybrid content + preference-based recommendations
"""


DESTINATION_PROFILES = [
    {
        "name": "Paris, France",
        "tags": ["romance", "art", "history", "food", "culture", "luxury"],
        "climate": "temperate",
        "cost_level": "high",
        "popularity": 0.95,
        "rating": 4.8,
    },
    {
        "name": "Bali, Indonesia",
        "tags": ["beach", "nature", "spiritual", "adventure", "budget", "relaxation"],
        "climate": "tropical",
        "cost_level": "low",
        "popularity": 0.88,
        "rating": 4.7,
    },
    {
        "name": "Tokyo, Japan",
        "tags": ["food", "technology", "culture", "shopping", "anime", "history"],
        "climate": "temperate",
        "cost_level": "medium",
        "popularity": 0.92,
        "rating": 4.9,
    },
    {
        "name": "New York, USA",
        "tags": ["urban", "culture", "food", "shopping", "nightlife", "art"],
        "climate": "continental",
        "cost_level": "high",
        "popularity": 0.90,
        "rating": 4.7,
    },
    {
        "name": "Santorini, Greece",
        "tags": ["romance", "beach", "photography", "luxury", "history", "relaxation"],
        "climate": "mediterranean",
        "cost_level": "high",
        "popularity": 0.85,
        "rating": 4.8,
    },
    {
        "name": "Bangkok, Thailand",
        "tags": ["food", "culture", "budget", "nightlife", "temples", "shopping"],
        "climate": "tropical",
        "cost_level": "low",
        "popularity": 0.86,
        "rating": 4.5,
    },
    {
        "name": "London, UK",
        "tags": ["history", "culture", "art", "food", "theatre", "museums"],
        "climate": "temperate",
        "cost_level": "high",
        "popularity": 0.91,
        "rating": 4.7,
    },
    {
        "name": "Iceland",
        "tags": ["nature", "adventure", "photography", "northern lights", "unique"],
        "climate": "arctic",
        "cost_level": "high",
        "popularity": 0.78,
        "rating": 4.9,
    },
    {
        "name": "Barcelona, Spain",
        "tags": ["beach", "art", "food", "architecture", "nightlife", "culture"],
        "climate": "mediterranean",
        "cost_level": "medium",
        "popularity": 0.87,
        "rating": 4.8,
    },
    {
        "name": "Dubai, UAE",
        "tags": ["luxury", "shopping", "modern", "adventure", "desert", "unique"],
        "climate": "desert",
        "cost_level": "high",
        "popularity": 0.82,
        "rating": 4.6,
    },
]


class RecommendationEngine:
    def hybrid_recommendation(self, user_preferences: dict, destination_data: list, top_n: int = 5) -> list:
        scored = []
        pref_tags = [t.lower() for t in user_preferences.get("interests", [])]
        pref_budget = user_preferences.get("budget_level", "medium").lower()
        pref_climate = user_preferences.get("climate", "").lower()

        all_destinations = DESTINATION_PROFILES + [
            {
                "name": d.get("name", "Unknown"),
                "tags": [],
                "climate": "any",
                "cost_level": "medium",
                "popularity": 0.7,
                "rating": 4.0,
            }
            for d in destination_data
        ]

        for dest in all_destinations:
            score = dest["popularity"] * 0.3 + (dest["rating"] / 5.0) * 0.3

            # Tag match
            if pref_tags:
                matches = sum(1 for t in pref_tags if t in dest["tags"])
                score += (matches / max(len(pref_tags), 1)) * 0.3

            # Budget match
            if pref_budget and dest["cost_level"] == pref_budget:
                score += 0.1

            # Climate match
            if pref_climate and pref_climate in dest["climate"]:
                score += 0.1

            scored.append({
                "destination": dest["name"],
                "score": round(score, 3),
                "tags": dest["tags"],
                "cost_level": dest["cost_level"],
                "rating": dest["rating"],
                "reason": self._explain(dest, pref_tags, pref_budget),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_n]

    def _explain(self, dest: dict, pref_tags: list, pref_budget: str) -> str:
        reasons = []
        matches = [t for t in pref_tags if t in dest["tags"]]
        if matches:
            reasons.append(f"matches your interest in {', '.join(matches)}")
        if dest["rating"] >= 4.8:
            reasons.append("highly rated by travelers")
        if dest["cost_level"] == pref_budget:
            reasons.append(f"fits your {pref_budget} budget")
        return "Recommended because it " + "; ".join(reasons) if reasons else "Popular destination with great reviews"
