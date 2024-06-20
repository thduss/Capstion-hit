import MainHead from './Header';

export default function Home() {
  return (
    <main className="flex flex-col h-screen">
      <MainHead/>
      <div className="flex flex-col h-screen bg-yellow-100 mx-20 py-10 items-center">
        <h1 className='text-3xl m-6'>사용 방법</h1>
        <div className='flex w-full bg-red-100'> 
          {/* 왼쪽 */}
          <div className="flex-1 bg-blue-100 m-4">
            왼쪽
          </div>

          {/* 오른쪽 */}
          <div className="flex-1 bg-blue-100 m-4">
            오른쪽
          </div>
        </div>
      </div>
    </main>
  );
}