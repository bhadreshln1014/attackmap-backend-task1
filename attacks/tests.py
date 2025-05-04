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

from rest_framework.test import APIClient
from django.test import TestCase
from attacks.models import NotificationRule, Notification, CyberAttack, Location
from datetime import datetime

class NotificationSystemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        NotificationRule.objects.delete()
        Notification.objects.delete()
        CyberAttack.objects.delete()

        loc_usa = Location(latitude=40.0, longitude=-75.0, country="USA")
        loc_de = Location(latitude=52.5, longitude=13.4, country="Germany")

        for i in range(3):
            CyberAttack(
                source_location=loc_usa,
                destination_location=loc_de,
                attack_type="DDoS",
                severity=8 + i,
                timestamp=datetime.utcnow(),
                additional_details={"ip_src": f"10.0.0.{i}", "ip_dst": f"20.0.0.{i}"}
            ).save()

    def test_create_notification_rule(self):
        data = {
            "name": "DDoS in USA",
            "attack_type": "DDoS",
            "country": "USA",
            "min_severity": 8
        }
        response = self.client.post("/api/notifications/rules/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(NotificationRule.objects.count(), 1)

    def test_list_notification_rules(self):
        NotificationRule(
            name="Test Rule",
            attack_type="DDoS",
            country="USA",
            min_severity=7
        ).save()

        response = self.client.get("/api/notifications/rules/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_rule_triggers_notifications(self):
        rule = NotificationRule(
            name="DDoS USA Trigger",
            attack_type="DDoS",
            country="USA",
            min_severity=8
        )
        rule.save()

        # Run evaluator
        from django.core.management import call_command
        call_command("evaluate_rules")

        notifications = Notification.objects()
        self.assertGreaterEqual(len(notifications), 1)
        self.assertEqual(notifications[0].rule_name, "DDoS USA Trigger")

    def test_get_notifications_logs(self):
        # Create a notification manually
        Notification(
            rule_name="Test Rule",
            attack_id="someid123",
            details={"test": "data"}
        ).save()

        response = self.client.get("/api/notifications/logs/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
