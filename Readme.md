# 약속 늦지 않는 새끼

### accounts app
<pre>
- 사용자 계정 관리 app
</pre>

### promise app

- 약속 게시물을 관리하는 app
- Promise model에 현재 담기는 것
  - user : 글쓴이
  - title : 제목
  - content : 내용
  - created_at : 글쓴시간
  - setting_date_time : 약속 날짜, 시간
  - party : 약속한 사람들 목록 (친구들중에서만포함됨)
  - longitud : 약속장소의 경도
  - latitude : 약속장소의 위도
- Friend model로 친구 구현
  - 친구추가버튼 : `<a href="{% url 'change_friend' operation='add' pk=user.pk %}">`
  - 친구해제버튼 : `<a href="{% url 'change_friend' operation='remove' pk=friend.pk %}">`

