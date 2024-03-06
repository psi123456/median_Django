from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework import viewsets, status
from quiz.models import Question
from quiz.models import UserAnswer
from quiz.serializers import QuestionSerializer
from quiz.serializers import UserAnswerSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Question, UserAnswer
import json
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets


def check_answers(request):
    # 모든 문제 가져오기
    questions = Question.objects.all()

    # 채점 결과를 저장할 리스트 초기화
    results = []

    # 문제별로 채점 수행
    for question in questions:
        user_answers = UserAnswer.objects.filter(question=question)
        for user_answer in user_answers:
            is_correct = user_answer.user_response == question.answer
            user_answer.is_correct = is_correct  # 정답 여부를 저장
            user_answer.save()  # 변경사항 저장
            results.append({
                'question_text': question.question,  # 질문 텍스트
                'user_answer_text': user_answer.user_response,  # 사용자 답변 텍스트
                'is_correct': is_correct,
                'answer_id': user_answer.id  # 답변의 ID
            })

    # 채점 결과를 JSON 형식으로 전달
    latest_results = sorted(results, key=lambda x: x['answer_id'], reverse=True)[:3]
    return JsonResponse({'latest_results': latest_results})

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

def quiz_page(request):
    # 여기에 퀴즈 페이지 로직 추가
    return HttpResponse("This is the quiz page.")
@method_decorator(csrf_exempt, name='dispatch')
class MyApiView(View):
    def get(self, request, *args, **kwargs):
        data = {'message': 'Hello from Django API!'}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            # 전송된 JSON 데이터 파싱
            received_data = json.loads(request.body)
            message = received_data.get('message')
            response_data = {'success': True, 'message': 'Data saved successfully'}
            return JsonResponse(response_data)

        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data, status=500)

