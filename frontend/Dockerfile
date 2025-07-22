# 빌드 단계
FROM node:18-alpine

# 작업 디렉토리 생성 및 이동
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .

# 포트 노출 및 실행
EXPOSE 3000
ENV CHOKIDAR_USEPOLLING=true
CMD ["npm", "start"]