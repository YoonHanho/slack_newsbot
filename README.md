# 네이버 뉴스 크롤링 후 팀 슬랙 채널에 자동 발송

- 네이버 뉴스 피드에서 특정 단어(예:금융빅데이터)로 검색 후 관련도 순으로 10개 정렬
- 관련도 상위 순으로 슬랙 채널에 발송. 단, 이전에 발송된 이력이 있으면 제외하고 다음 뉴스 발송
- 발송 이력은 SQLite로 관리
- 파이썬 코드는 라즈베리파이의 크론탭에 걸어놓고, 자동으로 돌아가게 하자~! 
