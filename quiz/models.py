from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_response = models.TextField()
    is_correct = models.BooleanField(default=False)  # 새로운 필드 추가

    def __str__(self):
        return f"UserAnswer for Question: {self.question}"

