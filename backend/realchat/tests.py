"""
Unit tests for the real estate chatbot API endpoints.
"""
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from .views import analyze
import json


class AnalyzeAPITestCase(APITestCase):
    """Test cases for the /api/analyze/ endpoint."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_single_locality_analysis(self):
        """Test single-locality analysis query."""
        query = "Give me analysis of Wakad"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['type'], 'single')
        self.assertIn('summary', response.data)
        self.assertIn('chartData', response.data)
        self.assertIn('tableData', response.data)
        # Verify that Wakad data is present
        self.assertEqual(len(response.data['chartData']['year']), 3)
        self.assertEqual(response.data['chartData']['price'], [4500, 4700, 5200])

    def test_comparison_mode(self):
        """Test comparison between two localities."""
        query = "Compare Ambegaon Budruk and Aundh demand trends"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['type'], 'comparison')
        self.assertIn('summary', response.data)
        self.assertIn('chartData', response.data)
        self.assertIn('tableData', response.data)
        # Verify both localities are in the response
        chart_data = response.data['chartData']
        self.assertTrue(
            ('aundh' in chart_data or 'ambegaon budruk' in chart_data) or
            (len(chart_data) == 2)
        )

    def test_price_growth_mode(self):
        """Test price growth query for a specific period."""
        query = "Show price growth for Akurdi over the last 3 years"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['type'], 'price_growth')
        self.assertIn('summary', response.data)
        self.assertIn('chartData', response.data)
        self.assertIn('tableData', response.data)
        # Verify price data is present
        self.assertEqual(len(response.data['chartData']['year']), 3)
        self.assertEqual(response.data['chartData']['price'], [3000, 3200, 3500])

    def test_invalid_locality(self):
        """Test query with non-existent locality."""
        query = "Analyze NonExistentArea"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.data)

    def test_invalid_query_format(self):
        """Test query that doesn't match any pattern."""
        query = "Tell me a story about real estate"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.data)

    def test_comparison_with_single_locality(self):
        """Test comparison query with only one locality mentioned."""
        query = "Compare Wakad with nothing"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        # Should error because only one locality is detected
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.data)

    def test_alternative_single_analysis_query(self):
        """Test single analysis with different phrasing."""
        query = "Analyze Kalyani Nagar"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['type'], 'single')

    def test_price_growth_with_different_years(self):
        """Test price growth with explicit year specification."""
        query = "Show price growth for Wakad over the last 2 years"
        request = self.factory.post(
            '/api/analyze/',
            {'query': query},
            format='json'
        )
        response = analyze(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['type'], 'price_growth')
        # Should only return 2 years of data
        self.assertEqual(len(response.data['chartData']['year']), 2)
