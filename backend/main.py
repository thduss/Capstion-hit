from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Union
import uuid
import traceback
import os
import time
from openpyxl import Workbook
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.summary_model import main as summarize_main
from crawler.agoda_crawling import Agoda
from crawler.coupang_crawling import Coupang

app = FastAPI()

# CORS 설정 추가
origins = [
    "chrome-extension://nblcjhgbpieholjcokgdkobednndbphn",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    prod_index: int
    prod_site: str
    prod_name: str
    prod_url: str
    imageUrL: str

class Review(BaseModel):
    prod_name: str
    review_content: str

# 파일 저장
class CVS:
    @staticmethod
    def save_file(resultA, resultB) -> str:
        # 크롤링 결과
        results = resultA + resultB

        if not results:
            print("리뷰가 없습니다.")
            return ""

        # JSON 형식으로 저장
        json_data = []
        for review_data in results:
            for review in review_data:
                if isinstance(review, dict):
                    json_data.append({
                        "product": review.get('prod_name', 'unknown'),
                        "review-text": review.get('review_content', 'no content')
                    })
                else:
                    print("Unexpected data format:", review)

        return json.dumps(json_data)

# 크롤링 & 모델 
def process_products(products: List[Product], queueId: str):
    start_time = time.time() 

    resultA = []
    resultB = []
    A_info_json = None
    B_info_json = None

    for product in products:
        print(product)
        if product.prod_site == 'coupang':
            if product.prod_index == 1:
                review_data, A_info_json = Coupang().main(product.prod_name, product.prod_url, product.imageUrL)
                resultA.append(review_data)
            else:
                review_data, B_info_json = Coupang().main(product.prod_name, product.prod_url, product.imageUrL)
                resultB.append(review_data)
        else:
            if product.prod_index == 1:
                A_info_json, review_data = Agoda().main(product.prod_name, product.prod_url)
                resultA.append(review_data)
            else:
                B_info_json, review_data = Agoda().main(product.prod_name, product.prod_url)
                resultB.append(review_data)

    review_data_json = CVS.save_file(resultA, resultB)

    combined_info_json = {
        "A": A_info_json,
        "B": B_info_json
    }
    # 크롤링 총 소요시간 
    end_time = time.time() 
    elapsed_time = end_time - start_time 
    print(f'크롤링 소요 시간: {elapsed_time:.2f}초')

    # 모델 호출 
    start_time = time.time() 
    
    summary_result = summarize_main(review_data_json)
    
    end_time = time.time() 
    elapsed_time = end_time - start_time 
    print(f'리뷰 요약 총 소요 시간: {elapsed_time:.2f}초')

    task_results[queueId] = {
        "combined_info": combined_info_json,
        "result": summary_result
    }
    return combined_info_json, review_data_json



task_results: Dict[str, Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]] = {}
start_times: Dict[str, float] = {}

# queueId 생성 & 크롤링 요청 엔드포인트
@app.post("/api/compare")
async def search_prod(products: List[Product], background_tasks: BackgroundTasks):
    try:
        queueId = str(uuid.uuid4())
        print(queueId)

        start_times[queueId] = time.time()  # Store the start time

        background_tasks.add_task(process_products, products, queueId)

        return JSONResponse(content={"queueId": queueId})
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 작업 결과 프론트로 반환하는 엔드포인트
@app.get("/api/results/{queue_id}")
async def get_results(queue_id: str):
    try:
        if queue_id in task_results:
            elapsed_time = time.time() - start_times[queue_id]  # Calculate elapsed time
            print(f'총 소요 시간: {elapsed_time:.2f}초')

            return JSONResponse(content=task_results[queue_id])
        else:
            raise HTTPException(status_code=202)
    
    except Exception as e:
        print("****************************************")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
