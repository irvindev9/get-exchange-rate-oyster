from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class TestExchangeApi(APITestCase):
  def test_exchanges_token_auth(self):
    response = self.client.get('/api/')
    self.assertEqual(response.status_code, 401)

  def test_authentication_token_auth(self):
    self.user = User.objects.create_user(username='oyster', password='oyster123')
    response = self.client.post('/api/token/', {'username': 'oyster', 'password': 'oyster123'})
    self.assertEqual(response.status_code, 200)

  def test_exchanges_token_auth_refresh(self):
    self.user = User.objects.create_user(username='oyster', password='oyster123')
    response = self.client.post('/api/token/', {'username': 'oyster', 'password': 'oyster123'})
    self.assertEqual(response.status_code, 200)
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    response = self.client.post('/api/token/refresh/', {'refresh': response.data['refresh']})
    self.assertEqual(response.status_code, 200)

  def test_api_exchanges_get(self):
    self.user = User.objects.create_user(username='oyster', password='oyster123')
    response = self.client.post('/api/token/', {'username': 'oyster', 'password': 'oyster123'})
    self.assertEqual(response.status_code, 200)
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    response = self.client.get('/api/')
    self.assertEqual(response.status_code, 200)