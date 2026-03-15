# 1. Hafif bir Node.js işletim sistemi seçiyoruz (Alpine Linux tabanlı)
FROM node:18-alpine

# 2. Konteynerin içindeki çalışma klasörümüz
WORKDIR /usr/src/app

# 3. Önce SADECE package.json dosyasını kopyalıyoruz (Docker Cache Optimizasyonu)
COPY package*.json ./

# 4. Kütüphaneleri kuruyoruz
RUN npm install --production

# 5. Yazdığımız index.js kodunu içeri kopyalıyoruz
COPY . .

# 6. Dış dünyaya açılacak port (index.js içinde 3000 belirlemiştik)
EXPOSE 3000

# 7. Konteyner ayağa kalktığında çalışacak komut
CMD [ "npm", "start" ]