import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Search_Result_Date :
  def __init__(self, title, date) :
    self.title = title

    if "시간 전" in date :
      self.date = datetime.today()
    else :
      date_list = date.replace(".", " ").split()
      self.date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    
  def __lt__(self, other):
      return self.date > other.date

def get_time_filter(option):
  options = {
      1: "&qdr:n",
      2: "&qdr:h",
      3: "&qdr:d",
      4: "&qdr:w",
      5: "&qdr:m",
      6: "&qdr:y"
  }
  return options.get(option, "")

def get_google_search_titles(query, option, time):
  result = []

  for num in range(time // 10) :
    # make a GET request to the Google search page
    url = f"https://www.google.com/search?q={query}&tbm=vid{option}&start={num * 10}"
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")
    
    # find the searh result one block
    desired_divs = soup.find_all('div', class_='MjjYud')

    for div in desired_divs:
      # 제목 추출
      title = div.find('h3', class_='LC20lb').text.strip()
      
      # 날짜 추출
      date = div.find_all('div', class_='gqF9jc')[0].find_all('span')[-1].text.strip()
      
      # print("제목:", title)
      # print("날짜:", date)

      date = Search_Result_Date(title, date)
      result.append(date)

    # find the search result titles
    # titles = [a.text for a in soup.find_all("h3", class_="LC20lb MBeuO DKV0Md")]
    # result.extend(titles)
  
  return result

print("1. 최근 검색 결과 (최근 몇 분 내)")
print("2. 최근 1시간 내 검색 결과")
print("3. 최근 24시간 내 검색 결과")
print("4. 최근 1주일 내 검색 결과")
print("5. 최근 1개월 내 검색 결과")
print("6. 최근 1년 내 검색 결과")

option = get_time_filter(int(input("기간 옵션을 선택하세요 (1~6): ")))
query = input("검색어를 입력하세요 : ")
time = int(input("원하는 개수를 입력하세요 (10단위) : "))
results = sorted(get_google_search_titles(query, option, time))
for result in results:
  print(f"{result.date.year}-{result.date.month:02d}-{result.date.day:02d}\t{result.title:<70}")
