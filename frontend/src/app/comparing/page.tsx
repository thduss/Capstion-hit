'use client'
import { useSearchParams, useRouter } from 'next/navigation';
import { useEffect, useState, useCallback, Suspense } from "react";

function ComparingPage() {
  const [status, setStatus] = useState('processing');
  const searchParams = useSearchParams();
  const queueId = searchParams.get('queueId');
  const router = useRouter();

  console.log(queueId);

  // 롱폴링 구현 함수
  const checkStatus = useCallback(async (queueId: string | string[]) => {
    const interval = 10000; // 10초 간격

    const poll = async () => {
      try {
        const response = await fetch(`http://34.64.246.251:8000/api/results/${queueId}`);
        console.log("Response Status:", response.status); // 응답 상태 로깅

        if (response.status === 500) {
          console.log("분석 중");
          setTimeout(poll, interval);
        } else if (response.status === 200) {
          const data = await response.json();
          console.log("Response Data:", data); 

          if (data) {
            console.log("분석 완료");
            setStatus('completed');

            // 서버에 결과 저장
            const saveResponse = await fetch('/api/saveResult', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ queueId, data }),
            });

            if (!saveResponse.ok) {
              throw new Error('결과 저장 중 오류 발생');
            }else{
              console.log("저장 완료");
            }
            setStatus('completed');
            
            // 결과가 저장되면 결과 페이지로 이동
            router.push(`/results?queueId=${queueId}`);

          } else {
            setStatus('error');
          }
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error("ERROR : ", error);
        setStatus('error');  // 상태를 'error'로 설정하여 에러 상태를 확인
        setTimeout(poll, interval);
      }
    };

    if (queueId) {
      poll();
    }
  }, [router, queueId]);

  useEffect(() => {
    if (queueId) {
      checkStatus(queueId);
    }
  }, [queueId, checkStatus]);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className="flex min-h-screen flex-col items-center p-24">
        {status === 'processing' && (
          <>
            <h1 className="m-20 text-3xl">분석 중입니다</h1>
            <div role="status">
              <svg aria-hidden="true" className="inline w-20 h-20 text-gray-300 animate-spin dark:text-gray-500 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
              </svg>
              <span className="sr-only">Loading...</span>
            </div>
          </>
        )}
        {status === 'completed' && (
          <h1 className="m-20 text-3xl">분석이 완료되었습니다!</h1>
        )}
        {status === 'timeout' && (
          <h1 className="m-20 text-3xl">시간 초과되었습니다.</h1>
        )}
        {status === 'error' && (
          <h1 className="m-20 text-3xl">서버 오류가 발생했습니다.</h1>
        )}
      </div>
    </Suspense>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading....</div>}>
      <ComparingPage />
    </Suspense>
  );
}