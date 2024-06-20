'use client'

import { useEffect, useState, Suspense } from 'react';
import Product from '../components/Product';
import { useSearchParams } from 'next/navigation';

function ResultsPage() {
  const searchParams = useSearchParams();
  const queueId = searchParams.get('queueId');  
 
  const [resultData, setResultData] = useState(null);
  const [productA, setProductA] = useState(null);
  const [productB, setProductB] = useState(null);
  const [items, setItems] = useState(null);

  useEffect(() => {
    const fetchResultData = async () => {
      try {
        const response = await fetch(`/api/saveResult?queueId=${queueId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const response_result = await response.json();
        console.log(response);
        console.log(response_result);
        if (response_result) {
          setResultData(response_result);
          setProductA(response_result.combined_info.A);
          setProductB(response_result.combined_info.B);
          
          const fetchedItems = response_result.result;
          setItems(fetchedItems);
          
          // Log each part of the data to debug
          console.log('Fetched result data:', response_result);
          console.log('Product A:', response_result.combined_info.A);
          console.log('Product B:', response_result.combined_info.B);
          console.log('fetchedItems: ',  fetchedItems);
          console.log('Items:', items);
        }
      } catch (error) {
        console.error('Error fetching result data:', error);
      }
    };

    if (queueId) {
      fetchResultData();
    }
  }, [queueId]);

  return (
    <div className='bg-#FEEFC5'>
      <Product ProductA={productA} ProductB={productB} Result={items} />
    </div>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ResultsPage />
    </Suspense>
  );
}