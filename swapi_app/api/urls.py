from django.urls import path
from .views import dataset_metadata_list, fetch_and_process_data, get_dataset_data, value_count

urlpatterns = [
    path('data/list', dataset_metadata_list, name='dataset_metadata_list'),
    path('data/fetch_and_process/', fetch_and_process_data, name='fetch_and_process_data'),
    path("explore/<str:metadata_id>/<int:page>/", get_dataset_data, name="get_dataset_data"),
    path("explore/value_count/<str:metadata_id>/<str:columns>/", value_count, name="value_count"),
]