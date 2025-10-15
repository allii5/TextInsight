from django.http import JsonResponse
from textinsight.middlewares.base_middleware import BaseMiddleware

class ErrorHandlingMiddleware(BaseMiddleware):
    def process_exception(self, request, exception):
        try:
            return JsonResponse({
                'error': str(exception),
                'message': 'Something went wrong, please try again later.'
            }, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Internal server error'}, status=500)
