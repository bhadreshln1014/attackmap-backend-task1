from django.core.management.base import BaseCommand
from attacks.models import CyberAttack, Location
from faker import Faker
import random
from datetime import datetime

fake = Faker()

class Command(BaseCommand):
    help = 'Generate realistic cyber attack data using Faker'

    def handle(self, *args, **kwargs):
        attack_types = ['DDoS', 'Malware', 'Phishing', 'Ransomware', 'Zero-Day', 'SQL Injection']

        for _ in range(100):
            src_coords = fake.location_on_land(coords_only=True)
            dst_coords = fake.location_on_land(coords_only=True)

            src = Location(
                latitude=float(src_coords[0]),
                longitude=float(src_coords[1]),
                country=fake.country()
            )
            dst = Location(
                latitude=float(dst_coords[0]),
                longitude=float(dst_coords[1]),
                country=fake.country()
            )

            attack = CyberAttack(
                source_location=src,
                destination_location=dst,
                attack_type=random.choice(attack_types),
                severity=random.randint(1, 10),
                timestamp=fake.date_time_this_year(),
                additional_details={
                    "ip_src": fake.ipv4_public(),
                    "ip_dst": fake.ipv4_public(),
                    "description": fake.sentence()
                }
            )

            attack.save()

        self.stdout.write(self.style.SUCCESS("100 realistic attack records generated."))
