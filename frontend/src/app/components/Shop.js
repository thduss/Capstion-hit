'use client';

import { useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import AnimatedTable from '../components/AnimatedTable'
import StarRating from './StarRating';

gsap.registerPlugin(ScrollTrigger);

// 크롤링 후 넘어오는 JSON 형식의 데이터
const data = [
  {
    "product_name": "홈플래닛 베이직 스탠드 선풍기 NDL2211",
    "product_url": "https://www.coupang.com/vp/products/7212367661?itemId=18255669809&vendorItemId=85402293544&pickType=COU_PICK&q=선풍기&itemsCount=36&searchId=2b7e26f0f91345b0a161911d2561a2f7&rank=1&isAddedCart=",
    "img_url": "https://image7.coupangcdn.com/image/retail/images/5231900402857284-4dc3ecaa-0621-4348-a29e-dbf7c0fa8524.jpg",
    "price": "와우 할인가 27,490원",
    "info": "타이머 기능: 타이머기능 있음,리모컨 유무: 미포함,소비전력: 50W,헤드 회전 가능여부: 좌우회전 가능,선풍기 타입: 스탠드",
    "star": 4.5,
    "reviews" : [
      {
        user: "User1",
        comment: "Great product!",
        rating: 5
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User2",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 2
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 1
      }
    ]
  },
  {
    "product_name": "시프이컴 5엽 가정용 선풍기 35cm CIF-FN02B",
    "product_url": "https://www.coupang.com/vp/products/5345925548?itemId=7850940285&vendorItemId=75140630718&q=선풍기&itemsCount=36&searchId=453d45d71be348bd98b9e99bb7a4aee0&rank=6&isAddedCart=",
    "img_url": "https://image6.coupangcdn.com/image/retail/images/298872095664583-16ea20e8-624e-4f67-8b8d-fb352b3383ab.jpg",
    "price": "27,900원 (와우쿠폰할인가)",

    "star": 4.5,
    "reviews" : [
      {
        user: "User3",
        comment: "Great product!",
        rating: 4
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 5
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 5
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 5
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 4
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 3
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 3
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 2
      },
      {
        user: "User4",
        comment: "Good value for money.",
        rating: 1
      }
    ]
  }
]

const Shop = () => {
  useEffect(() => {

    gsap.fromTo('.create-table', 
      { opacity: 0, scale: 0.8, y: 50 },
      { 
        opacity: 1,
        scale: 1,
        y: 0,
        duration: 1,
        scrollTrigger: {
          trigger: '.create-table',
          start: 'top 80%',
          end: 'bottom 20%',
          toggleActions: 'play none none reverse',
        }
      }
    );
     
    gsap.fromTo('.review-list',
      { opacity: 0, scale: 0.8, y: 50 },
      { 
        opacity: 1,
        scale: 1,
        y: 0,
        duration: 1,
        scrollTrigger: {
          trigger: '.review-list',
          start: 'top 80%',
          end: 'bottom 20%',
          toggleActions: 'play none none reverse',
        }
      }
    );
  }, []);
  

  return (
    <div>
      {/* 상품 정보 */}
      <div className="wrapper">
        <div className="screen -left">
          <div className="app-bar">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Coupang_logo.svg"
              className="logo"
              alt="Logo"
            />
          </div>
          <a href={data[0].product_url} target="_blank" rel="noopener noreferrer" className="title link">
            {data[0].product_name}
          </a>
          <div className="shop-items">
            <div className="item-block">
              <div className="image-area">
                <img src={data[0].img_url} className="image" />
              </div>
              <div className="name">{data[0].price}</div>
              <div className='star'>
                <StarRating rating={data[0].star}/>
                <div className="name m-6"> ({data[0].star}점)</div>
              </div>
              <div className="info">
                {data[0].info.split(',').map((info, index) => (
                  <p key={index}>{info}</p>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div id="cartItems" className="screen -right">
          <div className="app-bar">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Coupang_logo.svg"
              className="logo"
              alt="Logo"
            />
          </div>
          <a href={data[1].product_url} target="_blank" rel="noopener noreferrer" className="title link">
            {data[1].product_name}
          </a>
          <div className="shop-items">
            <div className="item-block">
              <div className="image-area">
                <img src={data[1].img_url} className="image" />
              </div>
              <div className="name">{data[1].price}</div>
              <div className='star'>
                <StarRating rating={data[0].star}/>
                <div className="name m-6"> ({data[0].star}점)</div>
              </div>
              <div className="info">
                {data[0].info.split(',').map((info, index) => (
                  <p key={index}>{info}</p>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 리뷰 */}
      <div className="wrapper">
        <h1 className='review_title'>&lt; 요약에 사용된 리뷰 &gt;</h1>
          <div className="review-list -left">
            <div className="title">"{data[0].product_name}" 리뷰 </div>
            <div className="reviews">
              <div className="description">
                    {data[0].reviews.map((review, reviewIndex) => (
                      <div key={reviewIndex} className="review">
                        <p><strong>{review.user}</strong> ({review.rating})</p>
                        <p>: {review.comment}</p>
                        <hr className='m-2'/>
                      </div>
                    ))}
                </div>
            </div>
          </div>
          <div id="cartItems" className="review-list -right">
          <div className="title">"{data[1].product_name}" 리뷰 </div>
          <div className="reviews">
              <div className="description">
                    {data[1].reviews.map((review, reviewIndex) => (
                      <div key={reviewIndex} className="review">
                        <p><strong>{review.user}</strong> ({review.rating})</p>
                        <p>: {review.comment}</p>
                        <hr className='m-2'/>
                      </div>
                    ))}
                </div>
            </div>
          </div>
      </div>

      {/* 테이블 */}
      <div className="wrapper">
        <h1 className='review_title'>1,305개 리뷰 중 20개의 리뷰를 요약한 결과</h1>
        <div className="create-table">
          <AnimatedTable />
        </div>
      </div>
    </div>
  );
};

export default Shop;
