from django.urls import path
from .api.views import dataset_metadata_list, fetch_and_process_data, get_dataset_data, value_count

urlpatterns = [
    path('api/metadata/', dataset_metadata_list, name='dataset_metadata_list'),
    path('api/fetch_and_process/', fetch_and_process_data, name='fetch_and_process_data'),
    path("data/<int:metadata_id>/<int:page>/", get_dataset_data, name="get_dataset_data"),
    path("data/value_count/<int:metadata_id>/<str:columns>/", value_count, name="value_count"),
]