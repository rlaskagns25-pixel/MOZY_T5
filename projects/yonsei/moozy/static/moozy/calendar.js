// calendar.js - 간단한 달력 렌더러 (초기화)
(function(){
  function renderCalendar(year, month){
    const calendar = document.getElementById('calendar');
    if (!calendar) return;
    calendar.innerHTML = '';
    const first = new Date(year, month, 1);
    const last = new Date(year, month+1, 0);
    const table = document.createElement('table');
    const header = document.createElement('tr');
    ['일','월','화','수','목','금','토'].forEach(d=>{
      const th = document.createElement('th'); th.textContent = d; header.appendChild(th);
    });
    table.appendChild(header);
    let row = document.createElement('tr');
    for(let i=0;i<first.getDay();i++){ const td=document.createElement('td'); row.appendChild(td); }
    for(let d=1; d<= last.getDate(); d++){
      if(row.children.length===7){ table.appendChild(row); row=document.createElement('tr'); }
      const td = document.createElement('td');
      td.textContent = d;
      td.className = 'cal-day';
      td.dataset.date = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      td.addEventListener('click', onDateClick);
      // 오늘 강조
      const now = new Date();
      if(now.getFullYear()===year && now.getMonth()===month && now.getDate()===d){
        td.classList.add('today');
      }
      row.appendChild(td);
    }
    if(row.children.length>0) table.appendChild(row);
    calendar.appendChild(table);
  }

  function onDateClick(e){
    const date = e.currentTarget.dataset.date;
    document.getElementById('selected-date').textContent = date;
    // 서버에 저장된 값 불러오기
    fetch(`/api/load-selection/${date}/`).then(r=>r.json()).then(data=>{
      document.getElementById('weather-input').value = data.weather || '';
      document.getElementById('note-input').value = data.note || '';
    });
    window.selectedDate = date;
  }

  document.addEventListener('DOMContentLoaded', function(){
    const now = new Date();
    renderCalendar(now.getFullYear(), now.getMonth());

    document.getElementById('save-btn').addEventListener('click', function(){
      const payload = {
        date: window.selectedDate,
        weather: document.getElementById('weather-input').value,
        note: document.getElementById('note-input').value
      };
      fetch('/api/save-selection/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(payload)
      }).then(r=>r.json()).then(data=>{
        if(data.ok){
          document.getElementById('confirm-msg').textContent = `${formatDate(window.selectedDate)}에 선택한 날씨가 저장되었어요.`;
          document.getElementById('confirm').style.display = 'block';
        } else {
          alert('저장 실패');
        }
      });
    });

    document.getElementById('back-btn').addEventListener('click', function(){
      document.getElementById('confirm').style.display='none';
    });
    document.getElementById('done-btn').addEventListener('click', function(){
      // 완료 후 메인 보기로 이동
      window.location.href = '/';
    });

    // csrftoken helper
    function getCookie(name){
      let v = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
      return v ? v.pop() : '';
    }
    function formatDate(s){
      // 'YYYY-MM-DD' -> 'M월 D일'
      const [y,m,d] = s.split('-'); return `${parseInt(m)}월 ${parseInt(d)}일`;
    }
  });
})();