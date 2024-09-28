from django.utils.deprecation import MiddlewareMixin
class IgnoreAuthHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the request is for the login path (adjust as needed)
        if request.path.startswith('/user/login/'):  # Ensure the path matches
            # Remove the Authorization header if present
            if 'HTTP_AUTHORIZATION' in request.META:
                del request.META['HTTP_AUTHORIZATION']
