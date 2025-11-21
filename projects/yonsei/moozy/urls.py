from django.urls import path
from . import views

app_name = 'moozy'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('diary/<date>/', views.diary_view, name='diary'),
    path('diary/<date>/delete/', views.delete_mood_entry, name='delete_mood'),  # ✅ 추가
    path('mood/select/', views.select_emotion_view, name='select_emotion'),
    path('mood/write/', views.write_note_view, name='write_note'),
    path('mood/confirm/', views.confirm_view, name='confirm'),
    path('mood/success/', views.success_view, name='success'),
    path('api/diary/<date>/', views.diary_api, name='diary_api'),
    path('insight/', views.insight_view, name='insight'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('calendar/get_entry/', views.get_diary_entry, name='get_diary_entry'),

    ]
