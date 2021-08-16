# 동남권 PT 센서 모니터링(압력, 온도)

## 모니터링 현황

### 파일 처리

1. csv file from DAQ -> 100도 , 20 MPa  초과 시 가져오지 않음 -> A~~all.csv
2. Datetime64로 형식 변경하고 인덱스화, column 명 통일
3. hampel 필터 적용 -> 필터링된 아웃라이어 개수 카운팅할 것 -> A~~all_filtered.csv
4. csv 연 단위 통계 내고 전체 개요 그래프 4개
5. 

