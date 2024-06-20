import { NextResponse } from 'next/server';

let resultDataStore = {};

export async function POST(req) {
  try {
    const body = await req.json();
    console.log('Received JSON:', body); 

    const { queueId, data } = body;
    resultDataStore[queueId] = data;
    console.log('POST resultDataStore[queueId] = ', resultDataStore[queueId]);
    return NextResponse.json({ message: 'Result saved successfully' }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ message: 'Error saving result' }, { status: 500 });
  }
}

export async function GET(req) {
  try {
    const { searchParams } = new URL(req.url);
    const queueId = searchParams.get('queueId');
    console.log('GET queueId: ', queueId);

    if (!queueId) {
      return NextResponse.json({ message: 'queueId is required' }, { status: 400 });
    }

    const resultData = resultDataStore[queueId];
    console.log('GET resultData: ', resultData);

    if (resultData) {
      return NextResponse.json(resultData, { status: 200 });
    } else {
      return NextResponse.json({ message: 'Result not found' }, { status: 404 });
    }
  } catch (error) {
    console.error('Error retrieving result:', error);
    return NextResponse.json({ message: 'Error retrieving result' }, { status: 500 });
  }
}