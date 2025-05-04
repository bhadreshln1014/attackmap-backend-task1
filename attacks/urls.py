from django.urls import path
from .views import AttackListView, RecentAttackView, VisualizationDataView, AttackStatisticsView

urlpatterns = [
    path('api/attacks/', AttackListView.as_view()),
    path('api/attacks/recent/', RecentAttackView.as_view()),
    path('api/attacks/visualization-data/', VisualizationDataView.as_view()),
    path('api/attacks/statistics/', AttackStatisticsView.as_view()),
]
