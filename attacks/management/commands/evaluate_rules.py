from django.core.management.base import BaseCommand
from attacks.models import CyberAttack, NotificationRule, Notification

class Command(BaseCommand):
    help = "Evaluate notification rules against attack data"

from django.core.management.base import BaseCommand
from attacks.models import CyberAttack, NotificationRule, Notification
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Evaluate notification rules against attack data"

    def handle(self, *args, **kwargs):
        rules = NotificationRule.objects(active=True)
        total_matched = 0

        for rule in rules:
            # Cooldown check
            if rule.last_triggered_at:
                cooldown_end = rule.last_triggered_at + timedelta(minutes=rule.cooldown_minutes or 10)
                if datetime.utcnow() < cooldown_end:
                    self.stdout.write(f"Skipping '{rule.name}' (cooldown active)")
                    continue

            # Build base query
            query = CyberAttack.objects
            if rule.attack_type:
                query = query.filter(attack_type=rule.attack_type)
            if rule.country:
                query = query.filter(__raw__={
                    "$or": [
                        {"source_location.country": rule.country},
                        {"destination_location.country": rule.country}
                    ]
                })
            if rule.min_severity:
                query = query.filter(severity__gte=rule.min_severity)
            if rule.max_severity:
                query = query.filter(severity__lte=rule.max_severity)
            if rule.time_window_minutes:
                cutoff = datetime.utcnow() - timedelta(minutes=rule.time_window_minutes)
                query = query.filter(timestamp__gte=cutoff)

            matched_attacks = list(query)

            # Volume-based rule
            if rule.threshold_count:
                if len(matched_attacks) >= rule.threshold_count:
                    Notification(
                        rule_name=rule.name,
                        attack_id="(volume_trigger)",
                        triggered_at=datetime.utcnow(),
                        details={
                            "matched_count": len(matched_attacks),
                            "rule": rule.name
                        }
                    ).save()
                    rule.last_triggered_at = datetime.utcnow()
                    rule.save()
                    total_matched += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"Rule '{rule.name}' triggered by volume: {len(matched_attacks)} attacks"
                    ))
            else:
                # Default: trigger per matching attack
                for attack in matched_attacks:
                    already = Notification.objects(rule_name=rule.name, attack_id=str(attack.id)).first()
                    if not already:
                        Notification(
                            rule_name=rule.name,
                            attack_id=str(attack.id),
                            triggered_at=datetime.utcnow(),
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


