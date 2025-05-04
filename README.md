# Cyberattack Data Map Backend – Internship Task 1

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

---

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
---

## MongoEngine Models – Task 1

### `Location` (EmbeddedDocument)

Represents a geographical location, used as both source and destination in an attack.

| Field       | Type   | Description               |
|-------------|--------|---------------------------|
| `latitude`  | Float  | Latitude of the location  |
| `longitude` | Float  | Longitude of the location |
| `country`   | String | Country name              |

---

### `CyberAttack` (Document)

Represents a cyberattack record in the database.

| Field                  | Type         | Description                                  |
|------------------------|--------------|----------------------------------------------|
| `source_location`      | `Location`   | Origin of the attack                         |
| `destination_location` | `Location`   | Target of the attack                         |
| `attack_type`          | String       | e.g., DDoS, Phishing, Malware                |
| `severity`             | Integer      | Severity rating (1 to 10)                    |
| `timestamp`            | DateTime     | When the attack occurred                     |
| `additional_details`   | Dict         | Extra metadata (e.g., IP addresses, protocol) |

---

## API Endpoints

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

# Notification System - Internship Task 2

This is an extension of the Cyberattack API backend. Task 2 implements a rule-based **notification engine** that scans cyberattack data and triggers alerts when defined conditions are met.

---

## Features

- Define notification rules with flexible conditions:
  - By `attack_type`, `country`, and severity range
- Automatically generate alerts when a cyberattack matches a rule
- Prevents duplicate notifications for the same attack and rule
- REST API endpoints to create/list rules and view triggered notifications
- A management command to run the rule evaluator logic
- Fully tested with clean test DB setup

---

## How It Works

1. You create a rule like:  
   _"Alert me for DDoS attacks in USA with severity > 7"_

2. The system runs a scanner:
   - Compares all rules against existing cyberattacks
   - If a match is found → stores a `Notification`

3. You can then:
   - View all rules
   - View all triggered notifications

---

## MongoEngine Models - Task 2

### `NotificationRule`
Defines an alert condition.

| Field         | Type      | Description                            |
|---------------|-----------|----------------------------------------|
| `name`        | String    | Rule name                              |
| `attack_type` | String    | Optional attack type filter            |
| `country`     | String    | Optional country filter (source or dest) |
| `min_severity`| Integer   | Optional min severity filter           |
| `max_severity`| Integer   | Optional max severity filter           |
| `active`      | Boolean   | Whether the rule is active             |
| `created_at`  | DateTime  | Timestamp of creation                  |

---

### `Notification`
Represents an alert triggered by a rule.

| Field         | Type      | Description                            |
|---------------|-----------|----------------------------------------|
| `rule_name`   | String    | Name of the rule that was triggered    |
| `attack_id`   | String    | The matched CyberAttack ID             |
| `triggered_at`| DateTime  | Timestamp of alert creation            |
| `details`     | Dict      | Snapshot of the matched attack         |

---

## API Endpoints

### `POST /api/notifications/rules/`

Create a new rule.

**Request:**
```json
{
  "name": "High Severity Malware in India",
  "attack_type": "Malware",
  "country": "India",
  "min_severity": 7
}
```

**Response:**

```json
{
  "id": "...",
  "name": "High Severity Malware in India",
  "attack_type": "Malware",
  "country": "India",
  "min_severity": 7,
  "active": true,
  "created_at": "2025-05-04T12:34:56Z"
}
```

---

### `GET /api/notifications/rules/`

List all notification rules.

**Response:**
```json
[
  {
    "id": "...",
    "name": "DDoS in USA",
    "attack_type": "DDoS",
    "country": "USA",
    "min_severity": 8,
    "active": true,
    "created_at": "2025-05-04T12:00:00Z"
  }
]
```

---

### `GET /api/notifications/logs/`

List all triggered notifications.

**Response:**
```json
[
  {
    "rule_name": "DDoS in USA",
    "attack_id": "6817172b70e0f9aa6b9a87f4",
    "triggered_at": "2025-05-04T13:30:00Z",
    "details": {
      "attack_type": "DDoS",
      "severity": 9,
      "country_src": "USA",
      "country_dst": "Germany",
      "timestamp": "2025-05-04T13:29:00Z"
    }
  }
]
```

---
## Evaluate Rules
The core logic to match attack data to rules is run via:
```bash
python manage.py evaluate_rules
```

---

## Tech Stack

- Python 3.11+
- Django 5
- MongoDB
- MongoEngine
- Django REST Framework
- Faker

---

## Author Details

**Name:** Bhadresh

**Role:** Backend Developer Intern Applicant

**Task:** Internship Selection Task 1 - Cyberattack Map API

**Email:** bhadreshln674@gmail.com

**GitHub:** [https://github.com/bhadreshln1014](bhadreshln1014)
