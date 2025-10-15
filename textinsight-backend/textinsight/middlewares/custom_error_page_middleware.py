from django.http import JsonResponse
from textinsight.middlewares.base_middleware import BaseMiddleware

class CustomErrorPageMiddleware(BaseMiddleware):
    def __call__(self, request):
        # Process the request first and get the response
        response = self.get_response(request)

        # Handle the error codes in the response
        if response.status_code == 404:
            return JsonResponse({'error': 'Page not found'}, status=404)
        elif response.status_code == 403:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        
        return response
