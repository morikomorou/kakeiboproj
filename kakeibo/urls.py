from django.urls import path, re_path
from .views import logoutfunc, month_listfunc, month_choicefunc, KakeiboCreateIn, KakeiboCreateOut, KakeiboUpdate, KakeiboDelete, historyfunc

urlpatterns = [
    path('list/', month_listfunc, name='list'),
    path('logout/', logoutfunc, name='logout'),
    path('month_list/<int:year>/<int:month>', month_listfunc, name='month_list'),
    path('month_choice', month_choicefunc, name="month_choice"),
    path('create_in/', KakeiboCreateIn.as_view(), name='create_in'),
    path('create_out/', KakeiboCreateOut.as_view(), name='create_out'),
    re_path('update/(?P<pk>[0-9]*)/(?P<in_out>(in|out))', KakeiboUpdate.as_view(), name='update'),
    path('delete/<int:pk>', KakeiboDelete.as_view(), name='delete'),
    path('history/', historyfunc, name='history'),
]
