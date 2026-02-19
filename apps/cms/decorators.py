from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def cms_required(view_func):
    """Require user to be staff to access CMS."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin-login/?next=' + request.path)
        if not request.user.is_staff:
            messages.error(request, 'You need staff access to use the CMS.')
            return redirect('/admin-login/')
        return view_func(request, *args, **kwargs)
    return _wrapped
