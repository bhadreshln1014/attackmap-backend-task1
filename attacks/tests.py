from django.test import TestCase
from rest_framework.test import APIClient
from attacks.models import CyberAttack, Location
from datetime import datetime

class AttackAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample attacks
        location1 = Location(latitude=40.7128, longitude=-74.0060, country="USA")
        location2 = Location(latitude=48.8566, longitude=2.3522, country="France")

        for i in range(5):
            CyberAttack(
                source_location=location1,
                destination_location=location2,
                attack_type="DDoS",
                severity=5 + i,
                timestamp=datetime.utcnow(),
                additional_details={"ip_src": f"192.0.2.{i}", "ip_dst": f"198.51.100.{i}"}
            ).save()

    def test_list_attacks(self):
        response = self.client.get("/api/attacks/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("results" in response.json())

    def test_filter_by_attack_type(self):
        response = self.client.get("/api/attacks/?attack_type=DDoS")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(a["attack_type"] == "DDoS" for a in response.json()["results"]))

    def test_recent_attacks(self):
        response = self.client.get("/api/attacks/recent/?limit=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)

    def test_statistics(self):
        response = self.client.get("/api/attacks/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("by_country", response.json())
