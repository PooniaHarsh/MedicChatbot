from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import requests


USER_AGENT = "healthcare-chatbot-mvp/1.0"


def geocode_location(location_text: str) -> Optional[Tuple[float, float]]:
    """Resolve a free-text location into latitude and longitude using Nominatim."""
    if not location_text:
        return None

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_text, "format": "json", "limit": 1}
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, params=params, headers=headers, timeout=12)
    response.raise_for_status()
    data = response.json()

    if not data:
        return None

    return float(data[0]["lat"]), float(data[0]["lon"])


def find_nearby_hospitals(lat: float, lon: float, radius_m: int = 10000, limit: int = 5) -> List[Dict[str, str]]:
    """Find nearby hospitals via Overpass API."""
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius_m},{lat},{lon});
      way["amenity"="hospital"](around:{radius_m},{lat},{lon});
      relation["amenity"="hospital"](around:{radius_m},{lat},{lon});
    );
    out center;
    """

    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data=query.encode("utf-8"), timeout=25)
    response.raise_for_status()
    data = response.json()

    hospitals: List[Dict[str, str]] = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name", "Unnamed Hospital")
        street = tags.get("addr:street", "")
        city = tags.get("addr:city", "")
        address = ", ".join(part for part in [street, city] if part)

        hospitals.append(
            {
                "name": name,
                "address": address if address else "Address not available",
                "lat": str(element.get("lat", element.get("center", {}).get("lat", ""))),
                "lon": str(element.get("lon", element.get("center", {}).get("lon", ""))),
            }
        )

    unique = []
    seen = set()
    for h in hospitals:
        key = (h["name"], h["address"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(h)
        if len(unique) >= limit:
            break

    return unique
