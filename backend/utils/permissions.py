from django.contrib.auth.decorators import login_required, permission_required
from functools import wraps
from django.http import JsonResponse

# Decorador para vistas basadas en clase (CBV)
def class_login_required(view_class):
    orig_dispatch = view_class.dispatch
    @wraps(view_class.dispatch)
    def new_dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required.'}, status=401)
        return orig_dispatch(self, request, *args, **kwargs)
    view_class.dispatch = new_dispatch
    return view_class

# Decorador para permisos específicos en CBV
def class_permission_required(perm):
    def decorator(view_class):
        orig_dispatch = view_class.dispatch
        @wraps(view_class.dispatch)
        def new_dispatch(self, request, *args, **kwargs):
            if not request.user.has_perm(perm):
                return JsonResponse({'detail': 'Permission denied.'}, status=403)
            return orig_dispatch(self, request, *args, **kwargs)
        view_class.dispatch = new_dispatch
        return view_class
    return decorator
