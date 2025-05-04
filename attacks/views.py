from rest_framework.views import APIView
from rest_framework.response import Response
from attacks.models import CyberAttack
from attacks.serializers import CyberAttackSerializer
from datetime import datetime

class AttackListView(APIView):
    def get(self, request):
        query = CyberAttack.objects

        # Filter by attack_type
        attack_type = request.GET.get('attack_type')
        if attack_type:
            query = query.filter(attack_type=attack_type)

        # Filter by country (source or destination)
        country = request.GET.get('country')
        if country:
            query = query.filter(
                __raw__={
                    "$or": [
                        {"source_location.country": country},
                        {"destination_location.country": country}
                    ]
                }
            )

        # Severity range
        min_severity = request.GET.get('min_severity')
        max_severity = request.GET.get('max_severity')
        if min_severity:
            query = query.filter(severity__gte=int(min_severity))
        if max_severity:
            query = query.filter(severity__lte=int(max_severity))

        # Date range
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start:
            start_date = datetime.fromisoformat(start)
            query = query.filter(timestamp__gte=start_date)
        if end:
            end_date = datetime.fromisoformat(end)
            query = query.filter(timestamp__lte=end_date)

        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        total = query.count()
        results = query.order_by('-timestamp')[start_index:end_index]
        serialized = CyberAttackSerializer(results, many=True)

        return Response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": serialized.data
        })

from rest_framework import status
from rest_framework.exceptions import ValidationError

class RecentAttackView(APIView):
    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 10))  # default: 10
        except ValueError:
            raise ValidationError("Limit must be an integer.")

        if limit < 1 or limit > 1000:
            return Response(
                {"error": "Limit must be between 1 and 1000"},
                status=status.HTTP_400_BAD_REQUEST
            )

        attacks = CyberAttack.objects.order_by('-timestamp')[:limit]
        serialized = CyberAttackSerializer(attacks, many=True)
        return Response({
            "count": len(serialized.data),
            "results": serialized.data
        })

class VisualizationDataView(APIView):
    def get(self, request):
        view_type = request.GET.get("view_type", "map")  # map or globe
        limit = int(request.GET.get("limit", 500))  # to limit the response size

        attacks = CyberAttack.objects.order_by('-timestamp')[:limit]

        features = []

        for attack in attacks:
            # Source point
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        attack.source_location.longitude,
                        attack.source_location.latitude
                    ]
                },
                "properties": {
                    "direction": "source",
                    "country": attack.source_location.country,
                    "attack_type": attack.attack_type,
                    "severity": attack.severity,
                    "timestamp": attack.timestamp.isoformat()
                }
            })

            # Destination point
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        attack.destination_location.longitude,
                        attack.destination_location.latitude
                    ]
                },
                "properties": {
                    "direction": "destination",
                    "country": attack.destination_location.country,
                    "attack_type": attack.attack_type,
                    "severity": attack.severity,
                    "timestamp": attack.timestamp.isoformat()
                }
            })

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return Response(geojson)

from collections import Counter

class AttackStatisticsView(APIView):
    def get(self, request):
        attacks = CyberAttack.objects()

        country_counts = Counter()
        type_counts = Counter()
        severity_counts = Counter()

        for attack in attacks:
            # Count both source and destination countries
            country_counts[attack.source_location.country] += 1
            country_counts[attack.destination_location.country] += 1

            type_counts[attack.attack_type] += 1
            severity_counts[attack.severity] += 1

        return Response({
            "by_country": dict(country_counts),
            "by_attack_type": dict(type_counts),
            "by_severity": dict(severity_counts)
        })
