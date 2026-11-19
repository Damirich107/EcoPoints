
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Submission


def home(request):
    return render(request, 'index.html')


@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    is_admin = request.user.is_superuser

    if not is_admin:
        try:
            is_admin = request.user.profile.role == 'admin'
        except Exception:
            is_admin = False

    if not is_admin and submission.user.email.lower() != request.user.email.lower():
        raise PermissionDenied

    return render(
        request,
        'submission_detail.html',
        {'submission': submission}
    )
