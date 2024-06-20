# Stage 1: Build the frontend
FROM node:18.17.0 AS frontend-builder
WORKDIR /app/frontend

# package.json과 package-lock.json을 별도로 복사하여 캐시를 최적화
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# 모든 프론트엔드 파일을 복사하고 빌드
COPY frontend .
RUN npm run build

# Stage 2: Build the backend
FROM python:3.9 AS backend-builder
WORKDIR /app/backend

# requirements.txt를 별도로 복사하여 캐시를 최적화
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# 모든 백엔드 파일을 복사
COPY backend .

# Final stage: Create the final image
FROM node:18.17.0
WORKDIR /app

# Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# backend-builder 단계에서 백엔드 파일 복사
COPY --from=backend-builder /app/backend /app/backend
# COPY --from=backend-builder /app/model /app/model

# frontend-builder 단계에서 빌드 아티팩트 복사
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /app/frontend/package.json
COPY --from=frontend-builder /app/frontend/package-lock.json /app/frontend/package-lock.json

# 프로덕션 종속성 설치
WORKDIR /app/frontend
RUN npm ci --production

# 작업 디렉토리를 frontend로 설정
WORKDIR /app/frontend

# next.js를 전역으로 설치
RUN npm install -g next

# 서비스 포트 노출
EXPOSE 8000
EXPOSE 3000

# FastAPI와 Next.js를 실행하는 명령어
CMD ["sh", "-c", "npm run dev & cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000"]