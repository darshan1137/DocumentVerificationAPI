from rest_framework import serializers

class SSCMarksheetSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    roll_no = serializers.CharField(required=True)
    result = serializers.CharField(required=True)
    document_file = serializers.FileField(required=True)
