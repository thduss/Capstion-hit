from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Union, Dict, List
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import sys
import json

from langdetect import detect
from openpyxl import Workbook

# 현재 파일의 위치에서 상위 디렉토리로 이동하여 preprocessing 폴더의 절대 경로 구하기
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'preprocessing')))

# preprocessing 폴더에서 필요한 모듈을 임포트
from text_preprocessing import preprocess

class Agoda:
    def main(self, hotel_name: str, hotel_url: str):
        # 크롬 드라이버 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = os.path.join(current_dir, 'chromedriver')

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

        url = hotel_url
        driver.get(url)
        time.sleep(5)
        
        # 리뷰 점수, 이미지 url 크롤링
        hotel_info = self.get_hotel_info(driver)

        # 리뷰 비율 
        review_counts = self.review_ratio(driver)

        # 리뷰 데이터 크롤링
        review_data = self.get_reviews(driver, review_counts, hotel_name)

        driver.quit()
        
        # JSON 형식으로 저장
        hotel_info_json = self.save_to_json(hotel_name, hotel_url, hotel_info, review_data)

        return hotel_info_json, review_data
    
    def get_hotel_info(self, driver: webdriver.Chrome) -> List[str]:
        # 페이지 소스 파싱
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # # 편의 시설/서비스 크롤링
        # amenities = []
        # amenity_elements = soup.select('div[data-element-name="atf-top-amenities-item"] p')
        # for element in amenity_elements:
        #     amenities.append(element.get_text())

        # # 위치 크롤링
        # location_element = soup.select_one('div.HeaderCerebrum__Location span[data-selenium="hotel-address-map"]')
        # location = location_element.get_text() if location_element else '위치 정보 없음'
        
        # # 금액 크롤링
        # price_element = soup.select_one('div.StickyNavPrice__priceDetail')
        # price = price_element.get_text(separator=' ').strip() if price_element else '가격 정보 없음'


        # 리뷰 점수 크롤링
        review_score_element = soup.select_one('span.sc-jrAGrp.sc-kEjbxe.fzPhrN.ehWyCi')
        review_score = review_score_element.get_text() if review_score_element else '리뷰 점수 없음'

        # # 체크인/체크아웃 시간 크롤링
        # checkin_time_element = soup.select_one('div[data-element-index="8"] span.kite-js-Span:nth-child(2)')
        # checkin_time = checkin_time_element.get_text() if checkin_time_element else '체크인 시간 정보 없음'

        # checkout_time_element = soup.select_one('div[data-element-index="9"] span.kite-js-Span:nth-child(2)')
        # checkout_time = checkout_time_element.get_text() if checkout_time_element else '체크아웃 시간 정보 없음'

        # 이미지 URL 크롤링
        img_url_element = soup.select_one('div[data-element-name="hotel-mosaic-tile"] img')
        img_url = img_url_element['src'] if img_url_element else '이미지 URL 없음'


        return review_score, img_url
    

    
    def review_ratio(self, driver: webdriver.Chrome) -> List[int]:
        # 별점 데이터 추출 
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        review_count = []
        items = soup.find_all('div', class_='ReviewSideFilter__Item')

        for item in items:
            text = item.find('span', class_='ReviewSideFilter__ItemText').text
            number = text.split('(')[-1].strip(')')
            review_count.append(int(number.replace(',', '')))

        # 비율 계산
        total_review = sum(review_count)
        star_ratios = [count / total_review for count in review_count]

        # 반올림 후 비율을 기반해 총 20개 리뷰 수집
        selected_star_ratio = [round(ratio * 10, 2) for ratio in star_ratios]
        print(selected_star_ratio)

        selected_counts = [round(ratio) for ratio in selected_star_ratio]
        print(selected_counts)
        
        while sum(selected_counts) < 10:
            min_ratios = [r for r in selected_star_ratio if r < 0.5]
            max_min_ratio = max(min_ratios)
            max_min_index = selected_star_ratio.index(max_min_ratio)
            
            selected_counts[max_min_index] += 1
            star_ratios[max_min_index] = 0.1

            print(selected_counts)

        return selected_counts
    
    def get_reviews(self, driver: webdriver.Chrome, review_counts: List[int], hotel_name: str) -> List[Dict[str, Union[str, int]]]:
        review_data = []
        for i, count in enumerate(review_counts):
            if count > 0:
                filter_selector = f'div.ReviewSideFilter__Item:nth-child({i+1}) .ReviewSideFilter__ItemCheckBox input[type="checkbox"]'
                checkbox = driver.find_element(By.CSS_SELECTOR, filter_selector)
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(3)

                reviews_counter = 0
                page_counter = 1

                while reviews_counter < count:
                    if page_counter > 1:
                        page_button_selector = f'span.Review-paginator-number[aria-label="이용후기 페이지 {page_counter}"]'
                        page_button = driver.find_element(By.CSS_SELECTOR, page_button_selector)
                        page_button.click()
                        time.sleep(5)

                    # 페이지 소스 파싱
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # 리뷰 추출
                    reviews = soup.find_all('div', class_='Review-comment')

                    for review in reviews:
                        # 리뷰 텍스트 추출
                        review_star = review.find('div', class_='Review-comment-leftScore').get_text()
                        review_text_element = review.find('p', class_='Review-comment-bodyText')
                        
                        if review_text_element is None:
                            continue
                        
                        review_text = review_text_element.get_text()
                        
                        # 언어 감지
                        if detect(review_text) == 'ko':
                            # 50자 이하 거르기
                            if len(review_text) < 50:
                                continue
                            
                            reviews_counter += 1

                            dict_data: Dict[str, Union[str, int]] = dict()

                            # 리스트에 데이터 담기
                            dict_data['prod_name'] = hotel_name
                            dict_data['review_content'] = preprocess(review_text)
                            review_data.append(dict_data)

                            if reviews_counter == count:
                                break

                    if reviews_counter >= count:
                        break

                    # 페이지 인덱스 업데이트
                    page_counter += 1

                # 체크박스 선택 해제
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(3)
        
        return review_data

    def save_to_json(self, hotel_name: str, hotel_url: str, hotel_info, review_data):
        review_score, img_url = hotel_info
        hotel_data = {
            "product_name": hotel_name,
            "product_url": hotel_url,
            "img_url": img_url, 
            "star": review_score,
            "reviews": review_data
        }

         # 상위 디렉토리의 data 폴더에 저장
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # data_dir = os.path.join(base_dir, 'data')

        # if not os.path.exists(data_dir):
        #     os.makedirs(data_dir)

        # file_path = os.path.join(data_dir, f'{hotel_name}_data.json')
        # with open(file_path, 'w', encoding='utf-8') as f:
        #     json.dump(hotel_data, f, ensure_ascii=False, indent=4)


        
        return hotel_data

if __name__ == "__main__":
    hotel_info, reviews = Agoda().main("다이와 로이넷 호텔 도쿄 쿄바시 프리미어 (Daiwa Roynet Hotel Tokyo Kyobashi Premier)", "https://www.agoda.com/ko-kr/st-john-s-hotel/hotel/gangneung-si-kr.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1922887&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-06-8&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=KRW&isFreeOccSearch=false&tag=eeeb2a37-a3e0-4932-8325-55d6a8ba95a4&tspTypes=7%2C8&los=1&searchrequestid=b83721de-be97-4734-b861-fd2344755d05&ds=JDAYvw1hldoylnpT")
    hotel_info, reviews = Agoda().main("롯데 호텔 부산 (Lotte Hotel Busan)", "https://www.agoda.com/ko-kr/lotte-hotel-busan/hotel/busan-kr.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1922887&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-06-8&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=KRW&isFreeOccSearch=false&tag=eeeb2a37-a3e0-4932-8325-55d6a8ba95a4&tspTypes=8&los=1&searchrequestid=1df6d383-a03b-47d7-af09-9b938a8b5d0e&ds=JDAYvw1hldoylnpT")
    
    # amenities, location, price, review_score, checkin_time, checkout_time, img_url = hotel_info

    # print("Amenities:")
    # for amenity in amenities:
    #     print(amenity)
    
    # print("\nLocation:")
    # print(location)

    # print("\nPrice:")
    # print(price)

    # print("\nReview Score:")
    # print(review_score)

    # print("\nCheck-in Time:")
    # print(checkin_time)

    # print("\nCheck-out Time:")
    # print(checkout_time)

    # print("\nReviews:")
    # for review in reviews:
    #     print(review)
