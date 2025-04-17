from tukin.models import Tukin
from rest_framework import serializers



class TukinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tukin
        fields = '__all__'