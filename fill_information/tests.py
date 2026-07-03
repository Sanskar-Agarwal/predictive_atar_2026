from django.test import TestCase
from django.urls import reverse
import json
# Create your tests here.
class MyapiTest(TestCase):
    def test_my_calculation(self):
        url = reverse('/fill_information/get_atar/')
        response = self.client.post(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
