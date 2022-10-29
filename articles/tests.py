from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from articles import serializers
from users.models import User
from faker import Faker
from .models import Article


# Create your tests here.

#이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file




class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email":"test@naver.com", "password":"1234",}
        cls.article_data = {"title":"test title", "content":"test content"}
        cls.user = User.objects.create_user("test@naver.com", "1234")
        
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        
        
    def test_fail_if_not_logged_in(self):
        url = reverse("article_view")
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)
        
    def test_create_article(self):
        response = self.client.post(
            path=reverse("article_view"),
            data = self.article_data,
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        
        
    def test_create_article_with_image(self):
        #임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.article_data["image"] = image_file
        
        #전송
        response = self.client.post(
            path=reverse("article_view"),
            data = encode_multipart(data= self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)
    
    @classmethod
    def tearDownClass(cls):
        pass
        
        
        
class ArticleReadTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.articles.append(Article.objects.create(title=cls.faker.sentence(), content=cls.faker.text(), user=cls.user))
            
    def test_get_article(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = serializers.ArticleSerializer(article).data
            print(response.data)
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
                print(key, value)
            
    @classmethod
    def tearDownClass(cls):
        pass