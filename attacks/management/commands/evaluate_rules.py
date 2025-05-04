from django.core.management.base import BaseCommand
from attacks.models import CyberAttack, NotificationRule, Notification

class Command(BaseCommand):
    help = "Evaluate notification rules against attack data"

    def handle(self, *args, **kwargs):
        rules = NotificationRule.objects(active=True)
        total_matched = 0

        for rule in rules:
            query = CyberAttack.objects

            if rule.attack_type:
                query = query.filter(attack_type=rule.attack_type)
            if rule.country:
                query = query.filter(
                    __raw__={
                        "$or": [
                            {"source_location.country": rule.country},
                            {"destination_location.country": rule.country}
                        ]
                    }
                )
            if rule.min_severity:
                query = query.filter(severity__gte=rule.min_severity)
            if rule.max_severity:
                query = query.filter(severity__lte=rule.max_severity)

            for attack in query:
                # Check if a notification already exists
                already_triggered = Notification.objects(
                    rule_name=rule.name, attack_id=str(attack.id)
                ).first()

                if not already_triggered:
                    Notification(
                        rule_name=rule.name,
                        attack_id=str(attack.id),
                        details={
                            "attack_type": attack.attack_type,
                            "severity": attack.severity,
                            "country_src": attack.source_location.country,
                            "country_dst": attack.destination_location.country,
                            "timestamp": str(attack.timestamp)
                        }
                    ).save()
                    total_matched += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"Rule '{rule.name}' triggered by attack {attack.id}"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"Done. Total new notifications created: {total_matched}"
        ))

