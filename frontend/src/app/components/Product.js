'use client';
import Image from 'next/image';

import { useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import StarRating from './StarRating';
import Table from './Table';

gsap.registerPlugin(ScrollTrigger);


export default function Product({ ProductA, ProductB, Result }) {


  useEffect(() => {
    gsap.to('.fade-in', {
      opacity: 1,
      duration: 1,
      scrollTrigger: {
        trigger: '.fade-in',
        start: 'top 50%',
        toggleActions: 'play none none none'
      }
    });

    gsap.fromTo('#review-summary', 
      { y: 0 },
      { y: 100, opacity: 0, duration: 1, scrollTrigger: {
        trigger: '#review-summary',
        start: 'top top',
        toggleActions: 'play none none none'
      }}
    );

    gsap.fromTo('.table-container', 
      { y: 100, opacity: 0, scale: 0.8 },
      { y: 0, opacity: 1, scale: 1, duration: 1, scrollTrigger: {
        trigger: '.table-container',
        start: 'top 80%',
        toggleActions: 'play none none none'
      }}
    );

    let lastScrollTop = 0;
    const handleScroll = () => {
      const reviewSummary = document.getElementById('review-summary');
      const productSummary = document.getElementById('product-summary');
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const windowHeight = window.innerHeight;
      const bodyHeight = document.body.scrollHeight - windowHeight;

      if (scrollTop > lastScrollTop && scrollTop + windowHeight >= bodyHeight) {
        // Scrolling down and reached the bottom
        gsap.to(reviewSummary, { opacity: 0, duration: 0.5 });
        gsap.to(productSummary, { opacity: 1, duration: 0.5 });
      } else if (scrollTop < lastScrollTop) {
        // Scrolling up
        gsap.to(reviewSummary, { opacity: 1, duration: 0.5 });
        gsap.to(productSummary, { opacity: 0, duration: 0.5 });
      }

      lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);
  console.log(Result);
  
  const productA_url = ProductA ? `https://www.coupang.com/${ProductA.product_url}` : 'ProductA URL not available';
  const productB_url = ProductB ? `https://www.coupang.com/${ProductB.product_url}` : 'ProductB URL not available';

  return (
    <div className=''>
      <div className="wrapper">
        {/* 1번째 상품 */}
        {ProductA && (
        <div className="screen -left" onClick={() => window.open(productA_url, "_blank")}>
          <div className="app-bar">
            <Image
              src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Coupang_logo.svg"
              className="logo"
              width={100}
              height={50} 
              alt="Logo"
            />
          </div>
          <a href={productA_url} target="_blank" rel="noopener noreferrer" className="title link text-3xl">
            {ProductA.product_name}
          </a>
          <div className="shop-items">
            <div className="item-block">
              <div className="image-area">
                <Image src={`https:${ProductA.img_url}`} width={360} height={360} className="image" />
              </div>
              <div className='star mt-2 flex items-center justify-center'>
                <StarRating rating={ProductA.star}/>
                <div className="name m-3"> ({ProductA.star}점)</div>
              </div>
            </div>
          </div>
        </div>
        )}
         {/* 2번째 상품 */}
         {ProductB && (
        <div id="cartItems" className="screen -right" onClick={() => window.open(productB_url, "_blank")}>
          <div className="app-bar">
            <Image
              src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Coupang_logo.svg"
              className="logo"
              alt="Logo"
              width={100}
              height={50} 
            />
          </div>
          <a href={productB_url} target="_blank" rel="noopener noreferrer" className="title link">
            {ProductB.product_name}
          </a>
          <div className="shop-items">
            <div className="item-block">
              <div className="image-area">
                <Image src={`https:${ProductB.img_url}`} width={360} height={360} className="image" />
              </div>
              <div className='star mt-2 flex items-center justify-center bg-#FFF rounded-xl'>
                <StarRating rating={ProductB.star}/>
                <div className="name m-3"> ({ProductB.star}점)</div>
              </div>
            </div>
          </div>
        </div>
         )}
      </div>
    
      <div id="review-summary" className="fixed bottom-0 left-0 w-full bg-customNavy text-center p-2">
        ▼ 리뷰 요약 결과를 확인하세요!
      </div>
      
      <div id="product-summary" className="fixed top-0 left-0 w-full bg-customNavy text-center p-2 opacity-0">
        ▲ 상품을 확인해봐요!
      </div>

      {/* 테이블 */}
      <div className="fade-in table-container bg-#FEEFC5">
        <Table ProductA={ProductA} ProductB={ProductB} result={Result}/>
      </div>

    </div>
  );
};