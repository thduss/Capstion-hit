from bs4 import BeautifulSoup as bs
from pathlib import Path
from typing import Optional,Union,Dict,List
from openpyxl import Workbook
import time
import os
import re
import math
import requests as rq
import json
import sys

# 현재 파일의 위치에서 상위 디렉토리로 이동하여 preprocessing 폴더의 절대 경로 구하기
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'preprocessing')))

# preprocessing 폴더에서 필요한 모듈을 임포트
from text_preprocessing import preprocess
from hanspell import spell_checker

def get_headers(
    key: str,
    default_value: Optional[str] = None
    )-> Dict[str,Dict[str,str]]:
    """ Get Headers """
    JSON_FILE = Path(__file__).resolve().parent / 'json' / 'headers.json'

    with open(JSON_FILE,'r',encoding='UTF-8') as file:
        headers : Dict[str,Dict[str,str]] = json.loads(file.read())

    try :
        return headers[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}')

class Coupang:
    @staticmethod
    def get_product_code(url: str)-> str:
        """ 입력받은 URL 주소의 PRODUCT CODE 추출하는 메소드 """
        prod_code : str = url.split('products/')[-1].split('?')[0]
        return prod_code

    def __init__(self)-> None:
        self.__headers : Dict[str,str] = get_headers(key='headers')

    
    def main(self, prod_name: str, prod_url: str, img_url) -> List[List[Dict[str, Union[str, int]]]]:
        # URL 주소
        URL: str = "https://www.coupang.com" + prod_url

        # URL의 Product Code 추출
        prod_code: str = self.get_product_code(url=URL)

        #최대 리뷰 개수
        max_reviews = 10
        # URL 주소 재가공
        url_template = f'https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={{}}&size=5&sortBy=ORDER_SCORE_ASC&ratings={{}}&q=&viRoleCode=3&ratingSummary=true'

        # __headers에 referer 키 추가
        self.__headers['referer'] = URL

        # 리뷰 비율
        review_url = url_template.format(1, "")
        print(review_url)

        star_rate, total_reviews = Review_ratio.star_rate(review_url)
        print("+++++++++++++++++++++++++++ star ratio +++++++++++++++++++++++++++++++++++++++++")
        print(star_rate)
        print(total_reviews)

        save_data = []
        for star, count in enumerate(reversed(star_rate), start=1):
            if count == 0:
                continue

            page = 1
            collected_reviews = 0
            
            with rq.Session() as session:
                while collected_reviews < count:
                    url = url_template.format(page, star)
                    page_data, rating = self.fetch(url=url, session=session, prod_name=prod_name, remaining_count=count - collected_reviews)
                    if not page_data:
                        break
                    save_data.extend(page_data)
                    collected_reviews += len(page_data)
                    page += 1
                    if collected_reviews >= count:
                        break
            
        
        product_info = self.save_to_json(prod_name, prod_url, img_url, rating, save_data[:max_reviews])
        return save_data[:max_reviews], product_info


    def fetch(self, url:str, session, prod_name, remaining_count)-> List[Dict[str,Union[str,int]]]:
        save_data : List[Dict[str,Union[str,int]]] = list()

        with session.get(url=url,headers=self.__headers) as response :
            html = response.text
            soup = bs(html,'html.parser')

            # Article Boxes
            articles = soup.select('article.sdp-review__article__list')

            # 담아야 하는 리뷰 개수 
            article_length = min(len(articles), remaining_count)

            for idx in range(article_length):
                dict_data : Dict[str,Union[str,int]] = dict()
                articles = soup.select('article.sdp-review__article__list')

                # 평점
                rating = articles[idx].select_one('div.sdp-review__article__list__info__product-info__star-orange')
                if rating == None:
                    rating = 0
                else :
                    rating = int(rating.attrs['data-rating'])

                # 리뷰 내용
                review_content = articles[idx].select_one('div.sdp-review__article__list__review > div')
                if review_content == None :
                    review_content = ''
                else:
                    review_content = preprocess(review_content.text.strip())
                   
                    # 맞춤법 교정
                    # spelled_sent = spell_checker.check(review_content)
                    # checked_review_text = spelled_sent.checked
                    
                if len(review_content) < 50:
                    continue
                
                # dict_data['star-rate'] = rating
                dict_data['prod_name'] = prod_name
                dict_data['review_content'] = review_content

                save_data.append(dict_data)

            time.sleep(1)

            return save_data, rating
        
    @staticmethod
    def clear_console() -> None:
        command: str = 'clear'
        if os.name in ('nt','dos'):
            command = 'cls'
        os.system(command=command)

    def save_to_json(self, product_name: str, product_url: str, img_url, review_score, review_data):
        product_data = {
            "product_name": product_name,
            "product_url": product_url,
            "img_url": img_url, 
            "star": review_score,
            "reviews": review_data
        }
        return product_data

class Review_ratio:
    def star_rate(url):
        __headers = get_headers(key='headers')
        __headers['referer'] = url 

        r = rq.get(url, headers=__headers)
        soup = bs(r.text, 'html.parser')

        # 별점 데이터 추출
        star_counts = [int(element['data-count']) for element in soup.select('.js_reviewArticleHiddenValue')]
        total_reviews = sum(star_counts)
        print(star_counts)

        # 비율 계산
        star_ratios = [count / total_reviews for count in star_counts]

        # 반올림 후 비율을 기반해 총 10개 리뷰 수집
        selected_star_ratio = [round(ratio * 10, 2) for ratio in star_ratios]
        print(selected_star_ratio)

        selected_counts = [round(ratio) for ratio in selected_star_ratio]
        print(selected_counts)

        '''
          총 개수가 10개가 되도록 조정 ex) [0.4, 0.3, 0.1, 0.03, 0.03, 0.04] 
            => 0.5 이하의 리뷰들은 어떻게 처리해서 총 10개의 리뷰를 만들 것인가? 
            => 즉 0.5 이하 중 가장 큰 비율을 차지하는 수를 1로 보자
        '''
        while sum(selected_counts) < 10:
            min_ratios = [r for r in selected_star_ratio if r < 0.5]
            max_min_ratio = max(min_ratios)
            max_min_index = selected_star_ratio.index(max_min_ratio)
            
            selected_counts[max_min_index] += 1
            star_ratios[max_min_index] = 0.1

            print(selected_counts)
        
        return selected_counts, total_reviews
    

if __name__ == "__main__":
    reviews = Coupang().main("코멧 진공 스테인리스 텀블러 + 손잡이 + 빨대뚜껑 + 빨대 + 빨대솔", "https://www.coupang.com/vp/products/2057731929?itemId=3497585861&vendorItemId=71483787293&q=%ED%85%80%EB%B8%94%EB%9F%AC&itemsCount=36&searchId=7bef22be23f34891b7c8f910e7422497&rank=1&isAddedCart=")

    for review in reviews:
        print(review)