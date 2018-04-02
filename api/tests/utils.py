from django.test import TestCase

class CustomTestCase(TestCase):
    def assertGoodResponse(self, response):
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json['message'], 'OK')


