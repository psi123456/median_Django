# views.py
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Post, CustomUser, Comment, Medifree
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_POST
import json
import logging

logger = logging.getLogger(__name__)
@method_decorator(csrf_exempt, name='dispatch')
class BoardApiView(View):
    def increase_views(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.views += 1
        post.save(update_fields=['views'])
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        increase_view = request.GET.get('increase_view') == 'true'

        if post_id:
            post = get_object_or_404(Post, id=post_id)
            if increase_view:
                self.increase_views(post_id)
            data = {'id': post.id, 'title': post.title, 'content': post.content,
                    'author': post.author.username,'is_author_superuser': post.author.is_superuser, 'created_at': post.created_at, 'likes': post.likes, 'views': post.views}
        else:
            # 모든 게시글 정보 반환
            posts = Post.objects.all()
            data = {'posts': [{'id': post.id, 'title': post.title, 'content': post.content,
                               'author': post.author.username, 'is_author_superuser': post.author.is_superuser, 'created_at': post.created_at, 'likes': post.likes, 'views': post.views} for
                              post in posts]}

        return JsonResponse(data)

    def patch(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('pk')
            post = get_object_or_404(Post, id=post_id)

            # 'likes' 필드를 업데이트
            post.likes += 1
            post.save(update_fields=['likes'])

            response_data = {'success': True, 'message': '좋아요가 성공적으로 추가되었습니다.'}
            return JsonResponse(response_data)
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data, status=500)

    def post(self, request, *args, **kwargs):
        try:
            # 전송된 JSON 데이터 파싱
            received_data = json.loads(request.body)
            title = received_data.get('title')
            content = received_data.get('content')
            author_username = received_data.get('author')
            # author_username이 'undefined'이거나 비어있는 경우 오류 처리
            if not author_username or author_username == "undefined":
                return JsonResponse({'success': False, 'message': '유효하지 않은 사용자입니다.'}, status=400)
            author = get_object_or_404(CustomUser, username=author_username)

            # 모델에 데이터 저장
            Post.objects.create(title=title, content=content, author=author)

            response_data = {'success': True, 'message': '게시물이 성공적으로 저장되었습니다.'}
            return JsonResponse(response_data)

        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data, status=500)

    def put(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('pk')
            post = get_object_or_404(Post, id=post_id)

            received_data = json.loads(request.body)
            post.title = received_data.get('title', post.title)
            post.content = received_data.get('content', post.content)
            post.author = received_data.get('author', post.author)
            post.save()

            response_data = {'success': True, 'message': '게시물이 성공적으로 수정되었습니다.'}
            return JsonResponse(response_data)

        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('pk')
            post = get_object_or_404(Post, id=post_id)
            post.delete()

            response_data = {'success': True, 'message': '게시물이 성공적으로 삭제되었습니다.'}
            return JsonResponse(response_data)

        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateListView(View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        comments = Comment.objects.filter(post_id=post_id)
        comments_data = [{'id': comment.id, 'author': comment.author.username, 'content': comment.content, 'created_at': comment.created_at, 'is_author_superuser': comment.author.is_superuser}
                     for comment in comments]

        return JsonResponse({'comments': comments_data})
    def post(self, request, *args, **kwargs):
        try:
            received_data = json.loads(request.body)
            post_id = received_data.get('post_id')
            author_username = received_data.get('author')
            content = received_data.get('content')

            post = get_object_or_404(Post, id=post_id)
            author = get_object_or_404(CustomUser, username=author_username)
            Comment.objects.create(post=post, author=author, content=content)

            return JsonResponse({'success': True, 'message': '댓글이 성공적으로 추가되었습니다.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class CommentDetailView(View):
    def patch(self, request, *args, **kwargs):
        try:
            comment_id = kwargs.get('comment_id')
            received_data = json.loads(request.body)
            content = received_data.get('content')

            comment = get_object_or_404(Comment, id=comment_id)
            comment.content = content
            comment.save()

            return JsonResponse({'success': True, 'message': '댓글이 성공적으로 수정되었습니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            comment_id = kwargs.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()

            return JsonResponse({'success': True, 'message': '댓글이 성공적으로 삭제되었습니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(username=username)

            if check_password(password, user.password):
                login(request, user)
                refresh = RefreshToken.for_user(user)

                # 관리자 여부를 클라이언트에게 전달
                is_admin = user.is_superuser

                # 토큰에 is_admin 정보 추가
                refresh['is_admin'] = is_admin
                refresh['username'] = user.username

                return JsonResponse({
                    'success': True,
                    'message': '로그인 성공',
                    'access_token': str(refresh.access_token),
                    'is_admin': is_admin,
                    'username': user.username,
                })
            else:
                return JsonResponse({'success': False, 'message': '아이디 또는 비밀번호가 일치하지 않습니다.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': '아이디 또는 비밀번호가 일치하지 않습니다.'})

    return JsonResponse({'success': False, 'message': 'POST 메소드만 지원합니다.'})

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        # POST 요청인 경우에만 처리
        data = json.loads(request.body)
        new_username = data.get('newUsername')
        new_password = data.get('newPassword')
        address = data.get('address')
        email = data.get('email')

        # 여기서 새로운 사용자를 생성하고 저장
        try:
            new_user = CustomUser.objects.create_user(username=new_username, email=email, password=new_password)
            new_user.address = address  # 주소 필드에 값 할당
            new_user.save()
            return JsonResponse({'success': True, 'message': '회원가입 성공'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'회원가입 실패: {str(e)}'})


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        data = [{'id': user.id, 'username': user.username, 'email': user.email, 'address': user.address} for user in users]
        return JsonResponse(data, safe=False)

@csrf_exempt
def user_delete(request, user_id):
    if request.method == 'DELETE':
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})

@csrf_exempt
@require_POST
def save_data(request):
    data = json.loads(request.body.decode('utf-8'))
    Medifree.objects.create(
        f_title=data['f_title'],
        f_items=data['f_items'],
        f_texts=data['f_texts']
    )
    return JsonResponse({'message': 'Data saved successfully'})

def get_latest_data(request):
    latest_data = Medifree.objects.last()
    if latest_data:
        response_data = {
            'f_title': latest_data.f_title,
            'f_items': latest_data.f_items,
            'f_texts': latest_data.f_texts,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'No data available'})