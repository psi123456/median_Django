"""
URL configuration for team project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from modelservice.views import upload_image
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static  # static() 함수 임포트
from modelservice.views import get_latest_image
from myapp.views import BoardApiView, CommentCreateListView, CommentDetailView, user_list, user_delete, get_latest_data, save_data
from quiz.views import MyApiView, quiz_page, QuestionViewSet,UserAnswerViewSet
from rest_framework.routers import DefaultRouter
from quiz import views

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'user-answers', UserAnswerViewSet)



urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/upload/', upload_image, name='upload-image'),
    path('api/latest-prediction-result/', get_latest_image, name='latest-prediction-result'),
    path("api/", include("myapp.urls")),  # myapp의 URL 패턴 포함
    path("", include("myapp.urls")),
    path('api/naver/', include('naver.urls')),  # naver 앱의 URL을 'api/naver/' 아래에 포함

    path("api/board/", BoardApiView.as_view(), name='board_api'),
    path("api/board/<int:pk>/", BoardApiView.as_view(), name='board-detail-api'),
    path('api/posts/<int:post_id>/comments/', CommentCreateListView.as_view(), name='post_comments'),
    path('api/comments/<int:comment_id>/', CommentDetailView.as_view(), name='update_delete_comment'),

    path('api/', MyApiView.as_view(), name='my-api'),
    path('quiz/', quiz_page, name='quiz_page'),  # 'quiz_page' 뷰 함수 사용
    path('', include(router.urls)),
    path('check-answers/', views.check_answers, name='check-answers'),

    path('api/users/', user_list, name='users'),
    path('users/<int:user_id>/', user_delete, name='user_delete'),
    path('get_latest_data/', get_latest_data, name='get_latest_data'),
    path('save_data/', save_data, name='save_data'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # 정적 파일 URL 패턴 설정

# 개발환경에서 미디어 파일을 서빙하기 위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)