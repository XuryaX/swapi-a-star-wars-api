import io
import os
import petl as etl
from swapi_app.cache import InMemoryCache
from swapi_app.models import MetaData
from swapi_app import tasks
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, Mock, call



class TasksTestCase(TestCase):

    @patch('requests.get')
    def test_fetch_characters(self, mock_requests_get):
        # Setup
        mock_requests_get.return_value.json.return_value = {
            "results": [
                {"name": "Luke Skywalker", "url": "http://swapi.dev/api/people/1/"},
                {"name": "Darth Vader", "url": "http://swapi.dev/api/people/4/"},
                {"name": "Han Solo", "url": "http://swapi.dev/api/people/14/"}
            ],
            "next": None
        }

        # Execute
        characters = tasks.fetch_characters()

        # Verify
        expected = [
            {"name": "Luke Skywalker", "url": "http://swapi.dev/api/people/1/"},
            {"name": "Darth Vader", "url": "http://swapi.dev/api/people/4/"},
            {"name": "Han Solo", "url": "http://swapi.dev/api/people/14/"}
        ]
        self.assertListEqual(characters, expected)

    @patch('requests.get')
    def test_fetch_homeworld_name_with_cache(self, mock_requests_get):
        # Setup
        url = "http://swapi.dev/api/planets/1/"
        cache = InMemoryCache()
        expected = "Tatooine"
        cache.set(url, expected)

        # Execute
        actual = tasks.fetch_homeworld_name(url)

        # Verify
        self.assertEqual(actual, expected)
        mock_requests_get.assert_not_called()

    @patch('swapi_app.tasks.fetch_characters')
    @patch('swapi_app.tasks.process_characters')
    @patch('swapi_app.tasks.save_data_to_csv')
    def test_fetch_data_calls_dependencies(self, save_data_mock, process_characters_mock, fetch_characters_mock):
        fetch_characters_mock.return_value = []
        process_characters_mock.return_value = Mock(), 0

        tasks.fetch_data()

        fetch_characters_mock.assert_called_once()
        process_characters_mock.assert_called_once()
        save_data_mock.assert_called_once()

    @patch('swapi_app.tasks.requests')
    def test_fetch_characters_with_successful_request(self, requests_mock):
        mock_response = Mock()
        mock_response.json.return_value = {
            "next": None,
            "results": [
                {"name": "Luke Skywalker", "height": "172", "mass": "77", "hair_color": "blond",
                 "skin_color": "fair", "eye_color": "blue", "birth_year": "19BBY", "gender": "male",
                 "homeworld": "http://swapi.dev/api/planets/1/", "created": "2014-12-09T13:50:51.644000Z",
                 "edited": "2014-12-20T21:17:56.891000Z", "url": "http://swapi.dev/api/people/1/"},
            ]
        }
        requests_mock.get.return_value = mock_response

        expected_result = [
            {"name": "Luke Skywalker", "height": "172", "mass": "77", "hair_color": "blond",
             "skin_color": "fair", "eye_color": "blue", "birth_year": "19BBY", "gender": "male",
             "homeworld": "http://swapi.dev/api/planets/1/", "created": "2014-12-09T13:50:51.644000Z",
             "edited": "2014-12-20T21:17:56.891000Z", "url": "http://swapi.dev/api/people/1/"},
        ]

        result = tasks.fetch_characters()

        requests_mock.get.assert_called_once_with('https://swapi.dev/api/people/')
        self.assertEqual(result, expected_result)

    def test_fetch_homeworld_name_with_cache_hit(self):
        cache_mock = Mock()
        cache_mock.has.return_value = True
        cache_mock.get.return_value = 'Tatooine'

        with patch('swapi_app.tasks.cache', cache_mock):
            result = tasks.fetch_homeworld_name('http://swapi.dev/api/planets/1/')

        self.assertEqual(result, 'Tatooine')
        cache_mock.has.assert_called_once_with('http://swapi.dev/api/planets/1/')
        cache_mock.get.assert_called_once_with('http://swapi.dev/api/planets/1/')

    def test_fetch_homeworld_name_with_cache_miss(self):
        url = 'http://swapi.dev/api/planets/1/'
        cache_mock = Mock()
        cache_mock.has.return_value = False
        response_mock = Mock()
        response_mock.json.return_value = {'name': 'Tatooine'}
        requests_mock = Mock()
        requests_mock.get.return_value = response_mock

        with patch('swapi_app.tasks.cache', cache_mock), \
             patch('swapi_app.tasks.requests', requests_mock):
            result = tasks.fetch_homeworld_name(url)

        self.assertEqual(result, 'Tatooine')
        cache_mock.set.assert_called_once_with(url, 'Tatooine')
        requests_mock.get.assert_called_once_with(url)
        response_mock.json.assert_called_once()
