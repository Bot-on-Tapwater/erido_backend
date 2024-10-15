from django.test import TestCase, RequestFactory
from unittest.mock import patch
from django.http import JsonResponse
from erido.views import consolidated_data_view, extract_json_data, generate_coupons, validate_coupon
from erido.models import Coupon
import json

class ConsolidatedDataViewTest(TestCase):

    def setUp(self):
        # Create a request factory instance to simulate requests
        self.factory = RequestFactory()

    @patch('erido.views.get_contents_of_shopping_cart_of_user')
    @patch('erido.views.user_status')
    @patch('erido.views.consolidated_data_no_sesssion_or_user_data')
    def test_consolidated_data_view(self, mock_consolidated_data, mock_user_status, mock_cart):
        # Mocking responses to return JsonResponse objects
        mock_consolidated_data.return_value = JsonResponse({
            'discounted_products': [],
            'best_selling_products': [],
            'brands': [],
            'categories': [],
            'subcategories': []
        })

        mock_user_status.return_value = JsonResponse({'is_logged_in': True})
        mock_cart.return_value = JsonResponse({'cart_items': []})

        # Simulate a GET request to the view
        request = self.factory.get('/consolidated-data/')
        
        # Call the view function
        response = consolidated_data_view(request)
        
        # Verify that the response is a JsonResponse
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        
        # Convert the response content to a dictionary
        response_data = extract_json_data(response)
        
        # Check that the consolidated data includes the correct keys
        self.assertIn('user_status', response_data)
        self.assertIn('cart', response_data)
        self.assertIn('discounted_products', response_data)
        self.assertIn('best_selling_products', response_data)
        self.assertIn('brands', response_data)
        self.assertIn('categories', response_data)
        self.assertIn('subcategories', response_data)
        
        # Verify the content of the returned data
        self.assertEqual(response_data['user_status'], {'is_logged_in': True})
        self.assertEqual(response_data['cart'], {'cart_items': []})
        self.assertEqual(response_data['discounted_products'], [])
        self.assertEqual(response_data['best_selling_products'], [])
        self.assertEqual(response_data['brands'], [])
        self.assertEqual(response_data['categories'], [])
        self.assertEqual(response_data['subcategories'], [])

class GenerateCouponsViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('erido.views.generate_and_save_coupons')
    def test_generate_coupons(self, mock_generate_and_save_coupons):
        # Simulate a GET request to the view
        request = self.factory.get('/coupons/generate/')
        
        # Call the view function
        response = generate_coupons(request)
        
        # Verify that the response is a JsonResponse
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        
        # Verify that the generate_and_save_coupons was called
        mock_generate_and_save_coupons.assert_called_once()
        
        # Now, let's add some coupons to the database and check the response
        Coupon.objects.create(code='CODE1234', discount=10.00, active=True)
        Coupon.objects.create(code='CODE5678', discount=15.00, active=True)

        # Simulate another request to the view
        response = generate_coupons(request)

        # Convert the response content to a dictionary
        response_data = json.loads(response.content)
        
        # Check that the correct coupons are returned in the response
        self.assertEqual(len(response_data), 2)  # Expecting 2 coupons
        self.assertEqual(response_data[0]['code'], 'CODE1234')
        self.assertEqual(response_data[0]['discount'], 10.00)
        self.assertEqual(response_data[1]['code'], 'CODE5678')
        self.assertEqual(response_data[1]['discount'], 15.00)

class ValidateCouponViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.valid_coupon = Coupon.objects.create(code='VALIDCODE', discount=10.00, active=True)
        self.invalid_coupon = Coupon.objects.create(code='INVALIDCODE', discount=5.00, active=False)

    def test_no_coupon_code(self):
        request = self.factory.post('/coupons/validate/', {})
        response = validate_coupon(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No coupon code provided.'})

    def test_valid_active_coupon(self):
        request = self.factory.post('/coupons/validate/', {'coupon': 'VALIDCODE'})
        response = validate_coupon(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'discount': 10.00})

    def test_valid_inactive_coupon(self):
        request = self.factory.post('/coupons/validate/', {'coupon': 'INVALIDCODE'})
        response = validate_coupon(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Coupon is not active.'})

    def test_invalid_coupon_code(self):
        request = self.factory.post('/coupons/validate/', {'coupon': 'NONEXISTENTCODE'})
        response = validate_coupon(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid coupon code.'})

    def test_invalid_request_method(self):
        request = self.factory.get('/coupons/validate/')  # Simulating a GET request
        response = validate_coupon(request)
        
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'error': 'Invalid request method.'})
