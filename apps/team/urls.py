from django.urls import path, reverse
from django.shortcuts import redirect
from . import views


def team_apply_redirect(request):
    """Redirect /team/apply/ to application center, preserving query string (e.g. ?tab=volunteer)."""
    url = reverse('application_center')
    if request.GET:
        url += '?' + request.GET.urlencode()
    return redirect(url)


urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('apply/', team_apply_redirect, name='team_apply'),
    path('board/filter/', views.team_board_filter, name='team_board_filter'),
    path('volunteers/filter/', views.team_volunteer_filter, name='team_volunteer_filter'),
    path('volunteers/page/', views.team_volunteer_page, name='team_volunteer_page'),
    path('<int:pk>/', views.member_detail, name='team_member_detail'),
    path('member/<int:pk>/', views.member_detail, name='member_detail'),
    path('collaborations/', views.collaboration_list, name='collaboration_list'),
    path('collaborations/<int:pk>/', views.collaboration_detail, name='collaboration_detail'),
    path('collaborations/<int:pk>/mou/', views.collaboration_mou_view, name='collaboration_mou_view'),
]
