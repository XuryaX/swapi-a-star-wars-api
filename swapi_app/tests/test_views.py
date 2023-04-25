from django.test import TestCase
from rest_framework.exceptions import ValidationError
from unittest.mock import patch, Mock, ANY
from petl.errors import FieldSelectionError
from django.test import RequestFactory
import petl as etl


from swapi_app.models import MetaData
from swapi_app.api.views import get_dataset_data, value_count

class GetDatasetDataTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('swapi_app.api.views.etl.fromcsv')
    @patch('swapi_app.api.views.os.path.exists')
    def test_get_dataset_data(self, mock_exists, mock_fromcsv):
        metadata = MetaData.objects.create(num_files=1)
        mock_exists.return_value = True  # <-- Add this line to mock os.path.exists
        mock_fromcsv.return_value = etl.empty()
        request = RequestFactory().get('/')
        response = get_dataset_data(request, metadata.id, 1)
        self.assertEqual(response.status_code, 200)
        mock_fromcsv.assert_called_once_with(ANY)

    @patch('swapi_app.api.views.etl.fromcsv', side_effect=FileNotFoundError)
    def test_get_dataset_data_file_not_found(self, mock_fromcsv):
        metadata = MetaData.objects.create(num_files=1)
        request = RequestFactory().get('/')
        response = get_dataset_data(request, metadata.id, 1)
        self.assertEqual(response.status_code, 200)

    def test_get_dataset_data_invalid_metadata_id(self):
        request = RequestFactory().get('/')
        response = get_dataset_data(request, 99999, 1)
        self.assertEqual(response.status_code, 404)


class ValueCountTestCase(TestCase):
    @patch('swapi_app.api.views.etl.fromcsv')
    def test_value_count(self, mock_fromcsv):
        metadata = MetaData.objects.create(num_files=1)

        mock_table = etl.fromdicts([
            {'column1': 'value1', 'column2': 'value2'},
            {'column1': 'value3', 'column2': 'value4'},
        ])
        mock_fromcsv.return_value = mock_table

        request = RequestFactory().get('/')
        response = value_count(request, metadata.id, 'column1,column2')
        self.assertEqual(response.status_code, 200)
        mock_fromcsv.assert_called_once()
    
    @patch('swapi_app.api.views.etl.fromcsv', side_effect=FileNotFoundError)
    def test_value_count_file_not_found(self, mock_fromcsv):
        metadata = MetaData.objects.create(num_files=1)

        request = RequestFactory().get('/')
        response = value_count(request, metadata.id, 'column1,column2')
        self.assertEqual(response.status_code, 400)

    @patch('swapi_app.api.views.etl.aggregate', side_effect=FieldSelectionError('invalid column'))
    @patch('swapi_app.api.views.etl.fromcsv')
    def test_value_count_invalid_columns(self, mock_fromcsv, mock_aggregate):
        metadata = MetaData.objects.create(num_files=1)
        mock_fromcsv.return_value = etl.empty()

        request = RequestFactory().get('/')
        response = value_count(request, metadata.id, 'invalid_column')

        self.assertEqual(response.status_code, 400)
