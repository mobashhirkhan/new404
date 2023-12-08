from rest_framework import serializers


from .models import Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['type', 'id', 'origin','author', 'summary', 'object_on', 'object_type', 'published']
        
    def create(self, validated_data):
        """
        Create and return new Part instance given validated data
        """
        new_part_instance = Like.objects.create(**validated_data)
         
        return new_part_instance

    