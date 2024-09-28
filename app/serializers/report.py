from rest_framework import serializers
from ..models.report import Report


class ReportSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()  # Customize file logic
    image = serializers.ImageField()  # Directly map the image field
    category = serializers.CharField()  # Category in English
    industry = serializers.CharField()  # Industry in English
    report_type = serializers.CharField()  # Report Type in English

    class Meta:
        model = Report
        fields = ['id', 'title', 'description', 'category', 'industry', 'report_type', 'publish_date', 'page_count', 'file', 'image']

    def get_title(self, obj):
        language = self.context.get('language', 'en')  # Default to English
        return getattr(obj, f'title_{language}', obj.title_en)

    def get_description(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'description_{language}', obj.description_en)

    def get_file(self, obj):
        # Check if the user is authenticated
        request = self.context.get('request')
        if request.user.is_authenticated:
            # Provide the file URL if the user is authenticated
            language = self.context.get('language', 'en')
            file_field = getattr(obj, f'file_{language}', obj.file_en)
            if file_field:
                return request.build_absolute_uri(file_field.url)
            return None
        else:
            # Return a message that authentication is required
            return "Authentication required to download this file."
