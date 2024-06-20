import React, { useEffect, useState } from 'react';

export default function Table({ ProductA, ProductB, result }) {
  // json to table
  const aspects = result ? Object.keys(result)
    .filter(key => key.startsWith('Aspect'))
    .map(key => {
      const aspect = result[key];
      return {
        aspectName: aspect["Aspect name"],
        summaries: {
          item1: aspect["Item 1"],
          item2: aspect["Item 2"]
        }
      };
    })
    : [];

    // title 가져오기
    console.log(aspects);
    const items = result ? result.Items : {};

    // title 단어별 개행
    const formatText = (text) => {
      if (!text) return '';
      const lastSpaceIndex = text.lastIndexOf(' ');
      const mainText = text.substring(0, lastSpaceIndex);
      const lastWord = text.substring(lastSpaceIndex + 1);
      return (
        <>
          {mainText}
          <br />
          {lastWord}
        </>
      );
    };

    // 리뷰 상세창
    const [showDetailLeft, setShowDetailLeft] = useState(false);
    const [showDetailRight, setShowDetailRight] = useState(false);  


  return (
    <div className="min-h-screen flex items-center justify-center p-4 font-sans text-lg bg-#FEEFC5">
      <div className=" rounded-lg overflow-hidden w-full max-w-7xl">
      <div className="content">
          <div className="left">
            < div class="title">
              <p>{formatText(items['Item 1'])}</p>
            </div>
            {/* 왼쪽 팝업 */}
            <div>
              <span
                className="cursor-pointer text-blue-600 text-base"
                onClick={() => setShowDetailLeft(!showDetailLeft)}
              >
                수집된 리뷰 데이터 &gt;
              </span>
              {showDetailLeft && (
                <div className="detail-popup left-popup">
                  <div>
                    <div className="popup-header">
                    <span>리뷰 목록</span>
                    <button className="close-btn" onClick={() => setShowDetailLeft(false)}>X</button>
                    </div>
                  {ProductA.reviews.map((review, index) => (
                    <p key={index} className='review-content'>
                      <p className='text-red-500'>review {index+1} </p> {review.review_content} </p>
                  ))}
                  </div>
                </div>
              )}
            </div>

          </div>
          <div className='right'>
            {/* title */}
            < div class="title">
              <p>{formatText(items['Item 2'])}</p>
            </div>
             {/* 오른쪽 팝업 */}
             <div>
              <span
                className="cursor-pointer text-blue-600 text-base"
                onClick={() => setShowDetailRight(!showDetailRight)}
              >
                수집된 리뷰 데이터 &gt;
              </span>
              {showDetailRight && (
                <div className="detail-popup right-popup">
                  <div className="popup-header">
                    <span>리뷰 목록</span>
                    <button className="close-btn" onClick={() => setShowDetailRight(false)}>X</button>
                    </div>
                 {ProductB.reviews.map((review, index) => (
                    <p key={index} className='review-content'>
                      <p className='text-red-500'>review {index+1} </p> {review.review_content} </p>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        <table className="table-auto w-full border-collapse p-4">
          <thead className="">
            <tr>
              <th className="w-2/5"></th>
              <th className="w-1/5 bg-customNavy text-red-500 p-5 rounded-t-full text-3xl">Aspect</th>
              <th className="2/5"></th>
            </tr>
          </thead>
          <tbody>
            {aspects.map((aspect, index) => (
              <tr key={index}>
                {/* item1 */}
                {index === 0 ? (
                  <td className="py-6 pl-6 bg-customYellow rounded-tl-3xl text-xl">{aspect.summaries.item1}
                    {/* <hr className="mx-auto border-b-1 border-customNavy mt-3"/> */}
                  </td>
                ) : index === aspects.length - 1 ? (
                  <td className="p-6 bg-customYellow rounded-bl-3xl text-xl">{aspect.summaries.item1}</td>
                ) : (
                  <td className="p-6 bg-customYellow text-xl">{aspect.summaries.item1}</td>
                )}
                
                {/* aspect */}
                <td className="p-6 border border-customNavy bg-customNavy text-black font-bold text-center text-2xl">{aspect.aspectName}</td>
                
                {/* item2 */}
                {index === 0 ? (
                  <td className="p-6 bg-customYellow rounded-tr-3xl text-xl">{aspect.summaries.item2}</td>
                ) : index === aspects.length - 1 ? (
                  <td className="p-6 bg-customYellow rounded-br-3xl text-xl">{aspect.summaries.item2}</td>
                ) : (
                  <td className="p-6 bg-customYellow text-xl">{aspect.summaries.item2}</td>
                )}
              </tr>
            ))}
            <td></td>
            <td className='bg-customNavy text-black p-3 rounded-b-full'></td>
            <td></td>
          </tbody>
        </table>
      </div>
    </div>
  );
};