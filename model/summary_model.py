#!/usr/bin/env python

# ## 실행 전 설정해야 할 사항
# [첫 번째 코드]
# - openAI API Key 값 설정 : 83

import pandas as pd
from kss import split_sentences # 문장 분리기
from itertools import chain     # 리스트 하나로 합치기
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import json
import os

# 문장 분리기
def sentence_split (text):
    try:
        split_text = split_sentences(text) # 문장 단위로 분리
        result_review = list(chain.from_iterable(split_text)) # 여러 리스트들 하나의 리스트로 합치기
        result_review = [str(sentence) for sentence in result_review]
        return result_review
    
    except Exception as e:
        print(f"Error in sentence_split: {e}")
        return []


# 최적의 k개 찾기
def find_optimal_k (sentence_embeddings):
    try:
        # 실루엣 점수를 통해 최적의 클러스터 수 찾기
        silhouette_scores = []
        n_samples = len(sentence_embeddings)
        k_range = range(2, n_samples) # 클러스터의 수를 2부터 n_samples - 1까지 설정

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(sentence_embeddings)
            silhouette = silhouette_score(sentence_embeddings, kmeans.labels_)
            silhouette_scores.append(silhouette)

        # 실루엣 점수를 사용하여 최적의 클러스터 수 결정
        optimal_k = np.argmax(silhouette_scores) + 2
        
        return optimal_k
    
    except Exception as e:
        print(f"Error in find_optimal_k: {e}")
        return 5 # 기본 클러스터 수 반환


# 클러스터링
def clustering(review_text):
    try:
        #문장 분리와 리스트 하나로 합치기
        split_review = sentence_split(review_text)
        
        model = SentenceTransformer("jhgan/ko-sroberta-multitask")
        
        # 문장 임베딩 생성 
        embeddings = model.encode(split_review)

        # K-means 클러스터링
        num_clusters = find_optimal_k(embeddings)
        clustering_model = KMeans(n_clusters=num_clusters, random_state=31)
        clustering_model.fit(embeddings)
        cluster_assignment = clustering_model.labels_

        # 클러스터 결과 출력   
        clustered_sentences = {}
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            if cluster_id not in clustered_sentences:
                clustered_sentences[cluster_id] = []
            clustered_sentences[cluster_id].append(split_review[sentence_id])

        return clustered_sentences
    
    except Exception as e:
        print(f"Error in clustering: {e}")
        return {}


#GPT API 호출하기
def ask(messages, max_tokens = 256):
    try:
        client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'], 
        )
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo", 
            messages=messages,
            max_tokens=max_tokens,
            seed=1212
        )

        answer = response.choices[0].message.content

        return answer
    
    except Exception as e:
        print(f"Error in ask: {e}")
        return ""


# 클러스터링마다 결과 요약
def summarize_list (review_list):
    try:
        messages = [
            {"role":"system", "content": """Your goal is to generate a summary statement from a given review.
            The requirements are as follows: 

            a. You must summarize the sentences in all numbered categories.
            b. You must synthesize the reviews listed under for each numbered category and summarize them.
            c. You must summarize in Korean.
            d. You must summarize in detail and with specifics.
            e. You must summarize using the exact words used in a given review.
            f. You must summarize them like a human would write a review.
            g. You must write the predicate of the summary in the form "~이다." or "~하다.".
            h. It must be written in the format 'cluster_id n : summarized three sentences' """},
            {"role":"user", "content":f"""The review to summarize is
            Review: {clustering(review_list)} 

            Summarize this review, ensuring all requirements are met.
            """},
        ]

        output_text = ask(messages, 2048)
        
        # 텍스트를 줄 단위로 분할
        lines = output_text.strip().split('\n')

        # 모든 문장을 포함할 리스트 생성
        summary_list = []

        # 각 줄을 처리하여 문장을 리스트에 추가
        for line in lines:
            if ':' in line:
                # ':' 기호를 기준으로 키와 문장 부분을 분리
                _, sentence_part = line.split(':', 1)
                # 문장 부분을 '.' 기호를 기준으로 분할하여 각 문장을 리스트에 추가
                summary_list.extend(sentence_part.strip().split('. '))
            else:
                summary_list.extend(line.strip().split('. '))
        
        return summary_list
    
    except Exception as e:
        print(f"Error in summarize_list: {e}")
        return []


example_review1 = ['계획 없이 온 여행에서 친구들과 2박으로 즐거운 시간 보냈다', '가족들과의 1박2일 여행은 편안하고 행복한 여행이었다', '롯데에서의 첫 여행은 아이와 즐거운 경험이었다.', '호텔 주변 산책과 노랫소리가 기분 좋았다', '객실에서의 휴식과 바다 전망은 훌륭했고 야경은 이국적이었다', '편안한 침대와 맛있는 조식으로 행복한 숙박을 즐겼다.', '아쉬운 부분이 있었지만 호텔 주변 공연과 친절한 직원으로 항상 신뢰하는 호텔이다', '고객 대접 부분에서 조금 아쉬움을 느꼈지만, 직원들의 친절함으로 4박까지 더 머물게 되었다.', '좋은 날씨와 즐거운 기분전환을 경험했고 좋은 추억을 만들었다.', '아직 뜨거운 날씨를 즐긴 후에는 가을을 기대하며 다시 오고 싶다.', '수영장에서의 시간은 차갑지 않은 물과 애들이 좋아하는 시설로 즐거웠다.', '어린이 풀과 미끄럼틀이 있는 수영장으로 6살 아이가 즐거워 했다.', '롯데호텔은 친절하고 깨끗한 시설로 여행을 더욱 편안하게 만들어준다', '직원의 친절함과 깨끗한 객실로 항상 만족스러운 여행이다.', '추운 4월에 안전하고 편안한 휴가를 보낼 수 있는 롯데호텔은 다음 여행 때도 이용하고 싶다.', '해온에서 낮과 밤을 모두 즐길 수 있는 좋은 경치와 수영장을 경험했다.', '다음에는 가족과 함께 호캉스를 즐기고 싶다.', '감사하며 추천하고 있다.', '호텔 정문 직원의 ECI에 대한 대우와 서비스 향상이 필요하다.', '호텔 내의 다양한 레저 시설로 아이들과 함께 즐거운 시간을 보낼 수 있었다', '랍스타 떡볶이와 망고빙수는 특히 기억에 남는 맛있는 음식이었다.']

example_review2 = ['제주도여행을 즐기고 싶은 가족에게 추천하며, 객실이 깔끔하고 가격 대비 좋다.', '위치 또한 이동하기 편리하고 주변에서 많은 사람들이 추천하는 곳으로 나름 괜찮은 선택이다.', '방 청결이 아쉬우며, 재방문 여부는 잘 모르겠다.', '13층에서 숙박했을 때 바다가 시원하게 보이는 전망과 1층에 스타벅스가 위치하여 편리하다.', '가격대 대비 깨끗하고 넓은 객실, 그리고 친절한 직원들의 서비스가 만족스럽다.', '다만 일부 객실은 방음이 잘 되지 않지만, 전체적으로 만족한다.', '바다 전망이 일부 가려져 아쉬웠고 주차 공간이 부족했지만, 공항 근처에 위치하여 접근성이 좋다.', '근처에는 큰 마트와 맛집이 있어 편리하며, 애월이나 협재로 이동하기에도 편리한 위치에 있어서 만족스럽다.', '추가 생수 및 일회용품에 비용이 발생하고, 침구류가 찢어져 있어 교체가 필요하다.', '청결에 조금 더 신경 썼으면 좋겠다.', '전반적으로 청결과 위생에 대한 업그레이드가 필요하다.', '객실의 세면대와 어메니티가 청결하지 못하므로 더 꼼꼼한 청소가 필요하다.', '바닥 청소와 객실 내 청결 상태를 개선해야 한다.']

example_review3 = ['방콕의 코모메트로폴리탄 느낌의 호텔로 자연친화적인 호텔 컨셉이다.', '직원의 친절한 서비스가 인상적이다', '수영장과 사우나, 온탕은 만족스럽지만 수영장의 수심이 얉아 아쉽다.', '호텔 주변 환경은 자연 속의 아름다움을 느낄 수 있고, 전체적으로 만족스럽다.', '중문에 위치하여 접근성이 좋다.', '수영장 외에 추천할 것이 없다.', '객실 상태에 대한 후기는 의견이 갈린다.']

example_review4 = ['호텔 직원의 높은 서비스 수준과 섬세한 응대가 감동을 준다.', '외국인 손님들을 친절하게 대하는 모습이 좋다.', '전체적인 경험이 만족스러운 투숙을 추천한다.', '섬오름 직원들의 친절과 훌륭한 응대로 만족스러운 투숙 이었다.', '객실 상태와 청결도가 양호하다.', '조식의 맛과 품질이 좋다.', '조용한 곳에 위치해 있어 편안하게 쉬기 좋다.', '객실이 깨끗하고, 분위기가 아늑하다.', '호텔 바로 앞의 아름다운 바닷가 뷰로 인해 즐거운 추억을 만들었다.']


# 공통 aspect 추출
def extract_common_aspects (new_review1, new_review2):
    try:
        messages = [
            {"role":"system","content":f"""Your goal is to extract the key common aspects between the two review data provided. 
            The requirements are as follows:
            
            a. You must extract only the key common aspects from the two review datasets provided.
            b. Focus on themes that are commonly mentioned in both review datasets, and exclude any topics that are mentioned only in one. 
            c. Make sure to only specify aspects that are mentioned in both datasets.
            d. You must write in Korean.
            e. The output format must be 'common aspects: extracted common aspects'.
            
            These are the examples of extracting common aspects between two review datas. They are separated by ###. 
            ###
            two reviews : {example_review1}, {example_review2} common aspects : 직원 서비스, 객실 상태, 위치 및 교통, 편의 및 부대시설, 재방문 의사 및 추천, 피드백
            ###
            two reviews : {example_review3}, {example_review4} common aspects : 객실 상태, 직원 서비스, 위치 및 교통, 가격, 시설의 만족도
            """},
            {"role":"user","content":f"""The reviews from which to extract key common aspects are as follows:     
            two reviews : {new_review1}, {new_review2} common aspects : 
            
            Extract the key common aspects between the two review datasets, ensuring all requirements are met."""},
        ]
        
        common_aspects = ask(messages, 512)
        
        return common_aspects
    
    except Exception as e:
        print(f"Error in extract_common_aspects: {e}")
        return ""


# common aspect 하나의 리스트로 묶기
def parse_aspects(input_string):
    try:
        # ':'가 있는 경우, ':' 이후의 문자열을 사용
        if ':' in input_string:
            input_string = input_string.split(': ')[1]
        
        # 쉼표로 구분하여 리스트로 변환
        aspect_list = input_string.split(', ')
        
        return aspect_list
    
    except Exception as e:
        print(f"Error in parse_aspects: {e}")
        return []


# 대망의 비교요약!!!!!
def comparative_summary (new_review1, new_review2, common_aspect_list):
    try:
        messages = [
            {"role":"system","content":f"""Your goal is to compare and summarize the two review datas for a given common aspect list.
            The requirements are as follows:
            
            a. You must summarize the Item A's review data, but also summarize how it compares to the Item B's review data.
            b. You must summarize the Item B's review data, but also summarize how it compares to the Item A's review data.
            c. You must summarize only what is relevant to each aspect for each aspect.
            d. You must summarize with specificity and detail.
            e. You must summarize in Korean.
            f. You must write them like a human would write a review.
            g. You must write the predicate of the summary in the form "~이다." or "~하다.".
            h. You must not write using indirect phrases like '언급되었다' or '평이 있다' and must write your summary as if the reviewer had said it directly. 
            i. The output format must be 'aspect: aspect n, Item A: Summary for Item A's review data, Item B: Summary for Item B's review data\n'.
            
            These are the examples of summarizing the data of two reviews for a given list of common aspects:
            
            Two reviews : {example_review1}, {example_review2} common aspect list : [직원 서비스, 객실 상태, 위치 및 교통, 편의 및 부대시설, 재방문 의사 및 추천, 피드백] <SUMMARY> aspect: 직원 서비스, Item A: 호텔 직원은 친절하고 고객 대접이 좋다. 항상 신뢰할 수 있는 호텔로 인상적이다., Item B: 직원들은 친절하고 서비스가 만족스럽다. 다만 몇몇 직원의 ECI에 대한 대우와 서비스 향상이 필요하다.

    aspect: 객실 상태, Item A: 객실은 깨끗하고 편안하며 바다 전망이 좋다. 침대와 조식이 만족스럽다., Item B: 일부 객실은 방음이 잘 안되고, 세면대와 어메니티의 청결에 문제가 있다. 전체적으로 청결과 위생에 대한 개선이 필요하다.

    aspect: 위치 및 교통, Item A: 호텔 주변에 위치한 롯데호텔은 접근성이 좋고, 주변에 관광 명소가 있어 편리하다., Item B: 호텔은 공항 근처에 위치하여 이동이 편리하고, 주변에는 큰 마트와 맛집이 있어 만족스럽다.

    aspect: 편의 및 부대시설, Item A: 호텔 주변에는 산책로와 다양한 레저 시설이 있어 즐거운 시간을 보낼 수 있고, 레스토랑의 맛있는 음식이 인상적이다., Item B: 호텔 내에 스타벅스가 있어 편리하며, 수영장은 아이들이 좋아할 만큼 좋은 시설이다.

    aspect: 재방문 의사 및 추천, Item A: 만족스러운 여행 후에 다시 이용하고 싶어하며, 가족과 함께 호캉스를 즐기고 싶다는 의사를 표현하고 있다., Item B: 청결과 위생에 대한 업그레이드가 필요하며, 재방문 여부는 미지수이지만 위치와 서비스로는 추천할 만하다.

    aspect: 피드백, Item A: 호텔의 객실과 서비스로 만족스러웠으나, 고객 대접 부분에서 아쉬움을 표현하였다., Item B: 객실의 세면대와 어메니티의 청결 상태를 개선해야 한다는 피드백을 전달하였다.
            
            Two reviews : {example_review3}, {example_review4} common aspect list : [객실 상태, 직원 서비스, 위치 및 교통, 시설의 만족도] <SUMMARY> aspect: 객실 상태, Item A: 호텔의 객실 상태에 대한 후기가 의견이 갈린다., Item B: 객실 상태와 청결도가 양호하며, 객실이 깨끗하고 아늑하다.

    aspect: 직원 서비스, Item A: 호텔 직원의 서비스는 친절하며 인상적이다., Item B: 호텔 직원의 높은 서비스 수준과 섬세한 응대가 감동적이며, 외국인 손님들을 친절하게 대하는 모습이 좋다.

    aspect: 위치 및 교통, Item A: 중문에 위치하여 접근성이 좋다., Item B: 조용한 곳에 위치하여 편안하게 쉬기 좋으며, 호텔 바로 앞의 아름다운 바닷가 뷰로 인해 즐거운 추억을 만들었다.

    aspect: 시설의 만족도, Item A: 수영장과 사우나, 온탕은 만족스럽지만 수영장의 수심이 적어 아쉽다., Item B: 조식의 맛과 품질이 좋으며, 만족스러운 투숙을 추천하며, 호텔의 시설에 대한 전체적인 만족도가 높다.
            """},
            {"role":"user","content":f"""The reviews and list of common aspects to summarize are as follows :     
            two reviews : {new_review1}, {new_review2} common aspects list : {common_aspect_list} <SUMMARY> 
            
            Summarize the two reviews based on the given list of common aspects, ensuring that all requirements are fully met."""},        
        ]
        
        com_summary = ask(messages, 2048)
        
        return com_summary
    
    except Exception as e:
        print(f"Error in comparative_summary: {e}")
        return ""
    

def jsonToDf(json_string):
    try:
        # Convert JSON string to JSON object
        json_object = json.loads(json_string)
        
        # JSON 객체를 DataFrame으로 변환
        df = pd.DataFrame(json_object)
        
        return df
    
    except Exception as e:
        print(f"Error in csvToDf: {e}")
        return pd.DataFrame()

# 아이템별 리뷰리스트 묶기
def split_list(df):
    try:
        items = df['product'].unique()

        ItemLists = {
            item: df[df['product'] == item]['review-text'].tolist()
            for item in items
        }
        
        return ItemLists
    
    except Exception as e:
        print(f"Error in split_list: {e}")
        print(df)
        return {}


# 결과 가공하기 !!!!!!!!!!!!!!!!!!!!!!!!!
def process_reviews(result_text, item_lists):
    try:
        # aspect와 리뷰 데이터를 담을 리스트 초기화
        AorB = ['A', 'B']
        aspect_list = []
        reviewA_list = []
        reviewB_list = []
        data = []

        # 텍스트를 줄 단위로 분리하여 처리
        lines = result_text.strip().split('\n')

        for line in lines:
            # 'aspect: '로 시작하는 경우
            if line.startswith('aspect: '):
                aspect = line.split(',')[0].replace('aspect: ', '').strip()
                aspect_list.append(aspect)
                
                # 'Item A: '와 'Item B: '가 있는지 확인
                if ', Item A: ' in line and ', Item B: ' in line:
                    items = line.split(', Item A: ')[1].split(', Item B: ')
                    reviewA = items[0].strip()
                    reviewB = items[1].strip()
                    
                    reviewA_list.append(reviewA)
                    reviewB_list.append(reviewB)
                elif ', Item A: ' in line:  # 만약 'Item A'만 있는 경우
                    reviewA = line.split(', Item A: ')[1].strip()
                    reviewA_list.append(reviewA)
                    reviewB_list.append('관련 내용이 없습니다.')
                elif ', Item B: ' in line:  # 만약 'Item B'만 있는 경우
                    reviewB = line.split(', Item B: ')[1].strip()
                    reviewA_list.append('관련 내용이 없습니다.')
                    reviewB_list.append(reviewB)      
            
        ##### json 만들기 ##### --> 웹 서비스 전달용
        aspect_dict = {}
        # 아이템 정보 생성
        item_dict = {f"Item {i+1}":item_name for i, item_name in enumerate(item_lists)}
        
        # 각 측면에 대한 정보 생성
        for i, aspect_name in enumerate(aspect_list):
            aspect_info = {"Aspect name": aspect_name, f"Item 1": reviewA_list[i], "Item 2": reviewB_list[i]}
            aspect_dict[f"Aspect {i+1}"] = aspect_info
            
        # 전체 구조 생성
        json_structure = {
            "Items" : item_dict,
            **aspect_dict
        }

        return json_structure
        # # 데이터 디렉토리 경로 설정 (thdus add)
        # data_dir = 'model/data'
        # os.makedirs(data_dir, exist_ok=True) 

        # file_path = os.path.join(data_dir, 'result.json')
                
        # # json 파일 저장
        # with open(file_path,'w', encoding='utf-8') as f:
        #     json.dump(json_structure, f, ensure_ascii = False, indent = 4)
            
    except Exception as e:
        print(f"Error in process_reviews: {e}")


# if __name__ == '__main__':
def main(jsonData):
    df = jsonToDf(jsonData)

    itemList = split_list(df)
    keyList = list(itemList.keys())

    # 두 개의 아이템을 클러스터링후 요약
    itemA = summarize_list(itemList[keyList[0]])
    itemB = summarize_list(itemList[keyList[1]])

    # 공통 측면 추출
    common_aspects = extract_common_aspects(itemA, itemB)

    # 두 아이템의 리뷰데이터를 비교 요약
    summary_result = comparative_summary(itemA, itemB, common_aspects)

    # 요약 결과 전처리 -> 웹 서버로 이동할 데이터로 가공
    item_name = [keyList[0], keyList[1]]
    # data = process_reviews(summary_result, item_name)
    summary_data = process_reviews(summary_result, item_name)

    return summary_data

