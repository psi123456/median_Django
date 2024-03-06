from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import ImageModel
import requests
import concurrent.futures  # 비동기 처리를 위한 모듈
from rest_framework.response import Response
from .models import PredictionResult
from .serializers import PredictionResultSerializer
from django.core.exceptions import ObjectDoesNotExist
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import base64
import json

logger = logging.getLogger(__name__)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            image_path = save_image(image)

            # Flask 서버의 엔드포인트 URL
            flask_endpoint = 'http://127.0.0.1:5000/predict'

            # 비동기 작업을 위한 함수 정의
            def process_image():
                try:
                    # 이미지 파일을 Flask 서버로 전송
                    with open(image_path, 'rb') as img:
                        response = requests.post(flask_endpoint, files={'image': img})
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return {"error": "Error processing image"}
                except requests.RequestException as e:
                    return {"error": str(e)}

            # 비동기 처리를 위한 실행자 생성
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 비동기 작업 실행
                processed_image_data = executor.submit(process_image).result()

            # 필요한 추가 작업 수행
            return JsonResponse(processed_image_data)
        else:
            return HttpResponse("No image file provided", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_image(request):
    try:
        latest_image = PredictionResult.objects.latest('id')
        image_url = latest_image.get_image_url()  # 이미지 URL 가져오기
        class_label = latest_image.class_label  # 예시로 'class_label' 필드 사용

        data = {
            'image_url': image_url,
            'class_label': class_label  # class_label도 응답에 포함
        }

        return Response(data)
    except ObjectDoesNotExist:
        logger.error('No images found')
        return Response({'error': 'No images found'}, status=404)
    except Exception as e:
        logger.error(f'Error fetching latest image: {e}')
        return Response({'error': str(e)}, status=500)


def save_image(image):
    # 이미지를 저장할 경로를 지정합니다.
    image_path = 'C:/team/team/images/' + image.name

    # 이미지 저장 경로의 디렉터리가 존재하는지 확인하고, 없으면 생성합니다.
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # 이미지를 저장합니다.
    with open(image_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)

    return image_path
