from rest_framework import serializers
from .models import PredictionResult

class PredictionResultSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PredictionResult
        fields = '__all__'  # 'image_url' 필드 추가

    def get_image_url(self, obj):
        return obj.image.get_image_url() if obj.image else None
