from django.utils.dateparse import parse_date
from django.http import HttpResponse
from datetime import datetime, date
import calendar
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MoodEntry
from datetime import datetime


@login_required
def diary_api(request, date):
    selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    entry = MoodEntry.objects.filter(user=request.user, date=selected_date).first()

    if entry:
        return JsonResponse({
            'exists': True,
            'date': selected_date.strftime("%Y년 %m월 %d일"),
            'emotion': entry.emotion,
            'note': entry.note,
        })
    else:
        return JsonResponse({
            'exists': False,
            'date': selected_date.strftime("%Y년 %m월 %d일"),
        })



from .models import MoodEntry

# 🏠 홈 화면
def home_view(request):
    return render(request, 'moozy/home.html')

# 📅 달력 화면
def calendar_view(request):
    today = date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    calendar_data = []
    for week in month_days:
        calendar_data.append({
            'week_number': week[0].isocalendar()[1],
            'days': [d if d.month == month else None for d in week]
        })

    return render(request, 'moozy/calendar.html', {
        'calendar_data': calendar_data,
        'current_month': month,
        'user': request.user
    })

# 📖 감정 기록 보기
def diary_view(request, date):
    parsed_date = parse_date(date)
    user = request.user if request.user.is_authenticated else None

    mood_entry = MoodEntry.objects.filter(user=user, date=parsed_date).first()

    return render(request, 'moozy/diary.html', {
        'date': parsed_date,
        'mood': mood_entry
    })

# 😊 감정 선택 화면
def select_emotion_view(request):
    if request.method == 'POST':
        emotion = request.POST.get('emotion')
        request.session['emotion'] = emotion
        return redirect('moozy:write_note')

    selected_date = request.GET.get('date')
    if selected_date:
        request.session['selected_date'] = selected_date

    return render(request, 'moozy/select_emotion.html')

from django.contrib import messages
# ✍️ 기분 입력 화면
def write_note_view(request):
    emotion = request.session.get('emotion')
    if not emotion:
        return redirect('moozy:select_emotion')

    if request.method == 'POST':
        note = request.POST.get('note', '').strip()

        if not note:
            messages.error(request, "일기를 작성해주세요!")
            return render(request, 'moozy/write_note.html', {'emotion': emotion})

        request.session['note'] = note
        return redirect('moozy:confirm')

    return render(request, 'moozy/write_note.html', {'emotion': emotion})

# ✅ 확인 및 저장 화면
def confirm_view(request):
    emotion = request.session.get('emotion')
    note = request.session.get('note')
    selected_date_str = request.session.get('selected_date')

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    if not emotion or not note:
        return HttpResponse("세션 정보가 없습니다. 다시 시작해주세요.")

    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        MoodEntry.objects.create(
            user=user,
            emotion=emotion,
            note=note,
            date=selected_date
        )
        request.session.pop('emotion', None)
        request.session.pop('note', None)
        request.session.pop('selected_date', None)
        return redirect('moozy:success')

    return render(request, 'moozy/confirm.html', {
        'emotion': emotion,
        'note': note,
        'date': selected_date
    })

def diary_api(request, date):
    parsed_date = parse_date(date)
    user = request.user if request.user.is_authenticated else None
    entry = MoodEntry.objects.filter(user=user, date=parsed_date).first()

    if entry:
        data = {
            'exists': True,
            'date': parsed_date.strftime('%Y년 %m월 %d일'),
            'weather': entry.emotion,
            'note': entry.note,
            'csrf_token': get_token(request),
        }
    else:
        data = {
            'exists': False,
            'date': parsed_date.strftime('%Y년 %m월 %d일'),
        }

    return JsonResponse(data)

def delete_mood_entry(request, date):
    user = request.user if request.user.is_authenticated else None
    parsed_date = parse_date(date)

    entry = get_object_or_404(MoodEntry, user=user, date=parsed_date)

    if request.method == 'POST':
        entry.delete()
        return redirect('moozy:calendar')

    return render(request, 'moozy/delete_confirm.html', {
        'date': parsed_date,
        'entry': entry
    })

@login_required
def write_diary(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        note = request.POST.get('note')
        emotion = request.POST.get('emotion')
        weather = request.POST.get('weather')

        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        Diary.objects.update_or_create(
            user=request.user,
            date=date,
            defaults={'note': note, 'emotion': emotion, 'weather': weather}
        )
        return redirect('calendar')  # 작성 후 캘린더로 이동
    return render(request, 'moozy/write_diary.html')



# 🎉 저장 완료 화면
def success_view(request):
    emotion = request.session.get('emotion')
    note = request.session.get('note')

    return render(request, 'moozy/success.html', {
        'emotion': emotion,
        'note': note,
    })
def insight_view(request):
    return render(request, 'moozy/insight.html')

def insight(request):
    return render(request, 'moozy/insight.html')  # user는 자동 포함됨

def mypage_view(request):
    return render(request, 'moozy/mypage.html')

def mypage(request):
    return render(request, 'moozy/mypage.html')  # user는 자동 포함됨