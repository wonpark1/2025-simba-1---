from .models import WeatherDB
from django.shortcuts import render, redirect
import requests
import datetime
import re

def weather_view(request):
    url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php"
    params = {
        'tm': '20250512',
        'stn': '108',
        'obs': 'TA, RN, WS',
        'help': '1',
        'mode': '0',
        'authKey': 'JGq0Aa1qTk-qtAGtar5P7A'
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        print("응답 코드:", response.status_code)
        print("응답 내용:", response.text)

        if response.status_code == 200:
            raw_text = response.text
            lines = raw_text.strip().split('\n')

            data_lines = [line for line in lines if not line.startswith("#") and line.strip()] # header, footer를 제외한 실질 데이터만 data_lines로 가져옴옴

            if data_lines:
                for line in data_lines:
                    columns = line.split()
                    try:

                        stn = columns[1] # 지점번호
                        temp_max = columns[11] # 일일 최고기온
                        temp_min = columns[13] # 일일 최저기온
                        wind_max = columns[5] # 일일 최고 풍속
                        rn_day = columns[38] # 일일 강수량 -> -9 == 강우 확률 0%

                        WeatherDB.objects.create(stn = stn, temp_max=temp_max, temp_min=temp_min, wind_max=wind_max, rain=rn_day)

                    except (IndexError, ValueError) as e:
                        print(f"{line} line 파싱 실패패")

            else:
                print("데이터 라인 유효성 X")

        else:
            print(f"API 호출 실패: {response.status_code}")

    except Exception as e:
        print(f"❗ 예외 발생: {e}")
    weather_data = WeatherDB.objects.filter(stn = 108).last() # stn = 108 -> 서울's 지점번호, 단일 쿼리 형식을 위해 .last() 사용용
    context = {
        'weather_data': weather_data,
    }

    return render(request, 'weathers/weathers.html', context)




# from urllib.parse import urlencode, quote_plus, unquote
# from urllib.request import urlopen
# from django.shortcuts import render
# import requests # HTTP 요청을 보내는 모듈
# import datetime # 날짜시간 모듈
# from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈


# def weather_view(request):

#     domain = "https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?"
    
#     params = {
#         'tm':'tm=20250513',
#         'obs':'obs=TA',
#         'help':'help=0',
#         'mode':'mode=0',
#         'authKey':"JGq0Aa1qTk-qtAGtar5P7A",
#     }

#     url = domain + urlencode(params)

#     with urlopen(url) as f:
#         html = f.read()
#         print(html)
    
#     return render(request, 'weathers/weathers.html', {'raw_response':html})

#     # now = datetime.now()
#     # today = datetime.today().strftime("%Y%m%d")
#     # y = date.today() - timedelta(days=1)
#     # yesterday = y.strftime("%Y%m%d")

#     # if now.minute<45: # base_time와 base_date 구하는 함수
#     #     if now.hour==0:
#     #         base_time = "2330"
#     #         base_date = yesterday
#     #     else:
#     #         pre_hour = now.hour-1
#     #         if pre_hour<10:
#     #             base_time = "0" + str(pre_hour) + "30"
#     #         else:
#     #             base_time = str(pre_hour) + "30"
#     #         base_date = today
#     # else:
#     #     if now.hour < 10:
#     #         base_time = "0" + str(now.hour) + "30"
#     #     else:
#     #         base_time = str(now.hour) + "30"
#     #     base_date = today

#     # params = {
#     #     'tm': base_date+base_time,
#     #     'obs':'TA',
#     #     'authKey': serviceKeyDecoded,
#     #     'mode':0,
#     #     'pageNo': 1,
#     #     'numOfRows': 1000,
#     #     'dataType': 'JSON',
#     #     'base_date': base_date,
#     #     'base_time': base_time,
#     #     'stn':0
#     # }
#     # # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 )
#     # res = requests.get(url, params=params, verify=False)
#     # items = res.json().get('response').get('body').get('items')
#     # #print(items)
#     # data = dict()
#     # data['date'] = base_date

#     # weather_data = dict()

#     # for item in items['item']:
#     #     # 기온
#     #     if item['category'] == 'T1H':
#     #         weather_data['tmp'] = item['fcstValue']
#     #     # 습도
#     #     if item['category'] == 'REH':
#     #         weather_data['hum'] = item['fcstValue']
#     #     # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
#     #     if item['category'] == 'SKY':
#     #         weather_data['sky'] = item['fcstValue']
#     #     # 1시간 동안 강수량
#     #     if item['category'] == 'RN1':
#     #         weather_data['rain'] = item['fcstValue']

#     # return render(request, '/weathers/templates/weathers/weathers.html', weather_data)
