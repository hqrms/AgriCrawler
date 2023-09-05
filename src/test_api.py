import unittest
import requests

try:
    from main import app
except Exception as e:
    message = ("Falha no import do app [Erro: {status}]".format(status = e))
    print(message)

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # self.response = app.get('/get_soja')
        self.response = requests.get("http://127.0.0.1:5000/get_soja")

    def test_if_api_is_working(self):
        self.assertEqual(200, self.response.status_code)

    def test_api_return_type(self):
        content_type = self.response.headers['Content-Type']
        self.assertIn('application/json', content_type)

    def test_if_return_is_not_null(self):
        self.assertIsNotNone(self.response.text)