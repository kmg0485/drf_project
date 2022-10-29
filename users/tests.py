from urllib import response
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserManager, User

class UserRegisterationAPIViewTestCase(APITestCase):
    def test_registeration(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@naver.com",
            "password":"1234",
        }
        response = self.client.post(url, user_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        
    # def test_login(self):
    #     url = reverse("token_obtain_pair")
    #     user_data = {
    #         "username":"testuser",
    #         "fullname":"테스터",
    #         "email":"test@naver.com",
    #         "password":"1234",
    #     }
    #     response = self.client.post(url, user_data)
    #     print(response.data)
    #     self.assertEqual(response.status_code, 201)
    
class LoginUserTest(APITestCase):
    def setUp(self):
        
        self.data = {"email":"test@naver.com", "password":"1234",}
        self.user = User.objects.create_user('test@naver.com', '1234')
        
    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        # print(response.data['access']) #access token값 확인
        self.assertEqual(response.status_code, 200)
        
    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        # print(access_token)
        response = self.client.get(
            path=reverse("profile_view", args = (self.user.id,)),
            HTTP_AUTHORIZAION=f"Bearer {access_token}"
        )
        # print(response.data)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.data['email'])
        
        
        
        