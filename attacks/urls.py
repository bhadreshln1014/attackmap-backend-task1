from django.urls import path
from .views import AttackListView, RecentAttackView, VisualizationDataView, AttackStatisticsView, NotificationRuleView, NotificationLogView

urlpatterns = [
    path('api/attacks/', AttackListView.as_view()),
    path('api/attacks/recent/', RecentAttackView.as_view()),
    path('api/attacks/visualization-data/', VisualizationDataView.as_view()),
    path('api/attacks/statistics/', AttackStatisticsView.as_view()),
    path('api/notifications/rules/', NotificationRuleView.as_view()),
    path('api/notifications/logs/', NotificationLogView.as_view()),
]
