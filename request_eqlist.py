import requests

URL = 'https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&xls=0&startTm=2016-09-12&endTm=2021-09-21&startSize=&endSize=&startLat=&endLat=&startLon=&endLon=&lat=35.746305&lon=129.205945&dist=20&keyword=&dpType=a'
response = requests.get(URL)
response.status_code
response.text
