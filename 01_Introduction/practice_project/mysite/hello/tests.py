from django.test import TestCase
from django.urls import reverse
from .models import Message


class MessageModelTests(TestCase):
    """메시지 모델 테스트"""
    
    def setUp(self):
        """테스트용 데이터 생성"""
        self.message = Message.objects.create(
            title="테스트 제목",
            content="테스트 내용"
        )
    
    def test_message_str(self):
        """메시지의 __str__ 메서드 테스트"""
        self.assertEqual(str(self.message), "테스트 제목")
    
    def test_message_creation(self):
        """메시지 생성 테스트"""
        self.assertIsNotNone(self.message.id)
        self.assertEqual(self.message.title, "테스트 제목")


class HelloViewTests(TestCase):
    """뷰 함수 테스트"""
    
    def setUp(self):
        """테스트용 메시지 생성"""
        self.message = Message.objects.create(
            title="테스트",
            content="테스트 내용"
        )
    
    def test_hello_view(self):
        """hello 뷰 테스트"""
        response = self.client.get(reverse('hello:hello'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view(self):
        """인덱스 뷰 테스트"""
        response = self.client.get(reverse('hello:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.message, response.context['messages'])
