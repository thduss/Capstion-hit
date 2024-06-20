import React from 'react';
import Image from 'next/image';

const Info = () => {
    const data = {
        "product1" : {
            "product_name": "롯데 호텔 부산 (Lotte Hotel Busan)",
            "product_url": "https://www.agoda.com/ko-kr/lotte-hotel-busan/hotel/busan-kr.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1922887&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-06-8&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=KRW&isFreeOccSearch=false&tag=eeeb2a37-a3e0-4932-8325-55d6a8ba95a4&tspTypes=8&los=1&searchrequestid=1df6d383-a03b-47d7-af09-9b938a8b5d0e",
            "img_url": "//pix8.agoda.net/hotelImages/42958/-1/4591e6c1349743676fb0fe79cff45771.jpg?ce=0&s=1024x768",
            "star": "8.9",
            "reviews": [
                {
                    "prod_name": "롯데 호텔 부산 (Lotte Hotel Busan)",
                    "review_content": "위치도 서면 중심이라 먹거리도 많고 지하에 백화점이 있어서 좋음. 야외수영장 새단장 후 벌써 세번째 방문인데 갈때마다 만족스러움. 다만 실내수영장의 경우 진정 수영인을 위한 레인을 분리해주면 좋겠음. 너무 유아동반 가족위주임. 사우나와 피트니스 시설도 굿. 직원분들은 항상 친절함. 라운지 애프터눈티는 이전보다 좋아진것 같은데 디너타임은 갈수록 음식퀄이 떨어지는듯함ㅠㅠ 특히 이번엔 같은 재료를 조리법만 바꿔서 낸 요리가 두가지였는데 맛비교하라는것도 아니고..일반적입맛으로는 아쉬웠음. 그럼에도 가성비 최고의 호텔임은 분명함. 계속 이용할것임."
                },
                {
                    "prod_name": "롯데 호텔 부산 (Lotte Hotel Busan)",
                    "review_content": "객실은 사실 오래되어 최신식 해운대 호텔들에 비해서 아쉬운 점은 있습니다. 하지만 롯데 직원들의 서비스가 정말 친절하고 투숙객들을 배려하는 점이 느껴집니다. 서면에 위치하고 있어 교통이 매우 편리하며 짐캐리 서비스를 이용하였는데 짐이 가벼워지니 여행의 퀄리티가 한단계 올라가는 편리한 서비스 였습니다. 조식이 정말 최고인데 종류도 많고 맛도 좋습니다. 아침의 서면 시티뷰도 좋구요. 일찍 일어나셔서 꼭 드시길 바랍니다. 휘트니스 센터도 널찍하고 리뉴얼을 한 지 얼마 안된 듯 쾌적합니다. 사우나도 괜찮았습니다. 다만 아쉬운 점이 한가지 있다면 객실 내 카드키가 전자식이 아닌 마그네틱 식이라서 그 점이 아쉬웠습니다."
                },
                {
                    "prod_name": "롯데 호텔 부산 (Lotte Hotel Busan)",
                    "review_content": "부산 시내 한가운데 이런 호텔에서 묵을 수 있어서 좋았습니다 성수기가 아닌 시점이라 가격도 나름 합리적으로 예매했네요 ㅎㅎ 친구의 브라이덜샤워를 몰래 준비하기 위해서 미리 이것저것 연락드리고 부탁드렸는데도 항상 친절하게 응답해주시고 얼리체크인을 했음에도 요청하신 사항을 잊지않고 모두 준비해주셔서 너무 좋았어요 리모델링 한 수영장도 따뜻한 물에 놀기 좋아서 다음에 또 방문하고싶네요 ㅎㅎ"
                }
            ]
        }
    }

    return(
        <div className="flex justify-center items-center p-10 ">
            <div className="flex items-center space-x-4">
                <div className="w-32 h-32 rounded-full overflow-hidden bg-gray-300">
                    <Image src={data.product1.img_url} alt="Product 1" width={128} height={128} className="w-full h-full object-cover" />
                </div>
                <div>
                    <div className="font-bold">{data.product1.product_name}</div>
                    <div className="text-yellow-500">⭐⭐⭐⭐⭐</div>
                </div>
            </div>
            <div className="flex items-center space-x-4">
                <div>
                    <div className="font-bold">{data.product1.product_name}</div>
                    <div className="text-yellow-500">⭐⭐⭐⭐⭐</div>
                </div>
                <div className="w-32 h-32 rounded-full overflow-hidden bg-gray-300">
                    <Image src={data.product1.img_url} alt="Product 2" width={128} height={128} className="w-full h-full object-cover" />
                </div>
            </div>
        </div>
    );
}

export default Info;
