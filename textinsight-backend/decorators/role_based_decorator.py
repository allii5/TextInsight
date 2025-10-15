from functools import wraps
from django.http import JsonResponse

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=403)
            
            if request.user.role != required_role:
                return JsonResponse({'error': f'Access denied for {required_role} role'}, status=403)
            
            return view_func(request, *args, **kwargs)
        _wrapped_view.required_role = required_role
        return _wrapped_view
    return decorator
