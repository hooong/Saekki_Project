# 약속 늦지 않는 새끼

> 음음...



### TODO

- 프론트 전반적으로!!^^
- 현재위치 받아오기 ~> map 띄울때 현재위치 주변으로
- 시간에 맞춰 약속이 종료되었는지 만들기
- 회원 정보 구체화 ~> 마이페이지
- 엽사를 올릴만한 구조 만들기
- 박지원 머리털 뽑기
- +++++이 이상 더 생각나는대로!!



### installed app (pip)

- django
- django-tempus-dominus
- psycopg2
- 일단 생각나는거 여기까지 만약에 뭔가가 no module뜨면 찾아보고 채워넣기
- DB는 PostgresQL 사용!!



### accounts app

- 사용자 계정 관리 app

- `signup.html`관리, auth 폼 꾸미기
- `login.html`은 `saekki_pro/templates/registration`에 있음



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