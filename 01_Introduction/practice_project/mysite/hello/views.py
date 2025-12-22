from django.shortcuts import render
from django.http import HttpResponse
from .models import Message

def index(request):
    """홈페이지 - 모든 메시지 표시"""
    messages = Message.objects.all()
    return render(request, 'hello/index.html', {'messages': messages})

def hello(request):
    """간단한 인사 페이지"""
    return HttpResponse("안녕하세요! Django에 오신 것을 환영합니다.")

def hello_detail(request, id):
    """특정 메시지 상세 조회"""
    try:
        message = Message.objects.get(id=id)
        return render(request, 'hello/detail.html', {'message': message})
    except Message.DoesNotExist:
        return HttpResponse("메시지를 찾을 수 없습니다.", status=404)
