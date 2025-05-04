# Cyberattack Map Backend – Internship Task 1

This is a Django-based backend service designed to provide real-time cyberattack data for visualizations on a map or globe. It connects to MongoDB and exposes RESTful API endpoints for attack data, statistics, and Mapbox-compatible formats.

## Features

- Stores attack data in MongoDB using `mongoengine`
- Generates realistic fake attack entries using `faker`
- Provides REST API endpoints for:
  - Listing and filtering attacks
  - Fetching recent attacks
  - Generating attack statistics
  - Returning GeoJSON data for visualizations
- Includes basic unit tests using Django’s test framework

## Tech Stack

- Python 3.11+
- Django 5
- MongoDB
- MongoEngine
- Django REST Framework
- Faker

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/bhadreshln1014/attackmap-backend-task1.git
cd attackmap-backend
```
2. Create and activate the Virtual Environment:
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On Mac/Linux
```
3. Install Requirements:
```bash
pip install -r requirements.txt
```
4. Start MongoDB:
```bash
net start MongoDB   # Windows
# OR
brew services start mongodb-community  # macOS
```
5. Generate Attacks:
```bash
python manage.py generate_attacks
```
6. Run the Server:
```bash
python manage.py runserver
```


## 📡 API Endpoints

### `GET /api/attacks/`

Returns a paginated list of all attack records.

**Query Parameters (optional):**

- `attack_type` – filter by type (e.g., DDoS)
- `country` – filter by source or destination country
- `min_severity`, `max_severity` – filter by severity range
- `start`, `end` – filter by timestamp (ISO date)
- `page`, `page_size` – pagination controls

**Example:**

`/api/attacks/?attack_type=DDoS&country=USA&min_severity=7&page=1&page_size=10`

**Curl Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/attacks/?attack_type=Phishing&min_severity=5"
```

---

### `GET /api/attacks/recent/`

Returns the most recent N attacks.

**Query Parameters:**

- `limit` – number of records to return (default: 10)

**Example:**

`GET /api/attacks/recent/?limit=5`

**Curl Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/attacks/recent/?limit=5"
```

---

### `GET /api/attacks/statistics/`

Returns attack count summaries grouped by:

- Country (source and destination)
- Attack type
- Severity level

**Example Response:**
```json
{
  "by_country": {
    "USA": 12,
    "India": 10
  },
  "by_attack_type": {
    "DDoS": 25,
    "Phishing": 15
  },
  "by_severity": {
    "5": 8,
    "9": 6
  }
}
```
**Curl Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/attacks/statistics/"
```

---

### `GET /api/attacks/visualization-data/`

Returns attack points in GeoJSON format for Mapbox or globe visualizations.

**Query Parameters:**

- `limit` - number of attack records to include (default: 500)
- `view_type` - optional, for future map/ globe optimizations

**Example:**

```bash
/api/attacks/visualization-data/?limit=100
```

**Curl Example:**

```bash
curl -X GET "http://127.0.0.1:8000/api/attacks/visualization-data/?limit=100"
```

**Example Response (GeoJSON):**

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-74.0060, 40.7128]
      },
      "properties": {
        "direction": "source",
        "country": "USA",
        "attack_type": "DDoS",
        "severity": 8,
        "timestamp": "2025-05-04T12:00:00Z"
      }
    }
  ]
}
```

## Run Tests

```bash
python manage.py test attacks
```


## Project Structure

```bash
attackmap-backend/
├── attackmap_backend/
├── attacks/
├── manage.py
├── README.md
├── requirements.txt
```

## Author Details

**Name:** Bhadresh

**Role:** Backend Developer Intern Applicant

**Task:** Internship Selection Task 1 - Cyberattack Map API

**Email:** bhadreshln674@gmail.com

**GitHub:** [https://github.com/bhadreshln1014](bhadreshln1014)







