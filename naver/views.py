# naver/views.py

import requests
from django.http import JsonResponse

def search_pharmacies(request):
    try:
        query = request.GET.get('query', '약국')
        headers = {
            'X-Naver-Client-Id': 'l190g2vt6v',
            'X-Naver-Client-Secret': 'fMfxM6l3hzEUX2EePtj5AgKuizaB3jYnQUcjCxa8',
             }

        response = requests.get(f'https://openapi.naver.com/v1/search/local.json?query={query}', headers=headers)
        response.raise_for_status()  # 응답 오류 발생 시 예외 발생
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
         # 네트워크 오류 또는 API 응답 오류 처리
        return JsonResponse({'error': str(e)}, status=500)
