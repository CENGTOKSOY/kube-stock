# 1. En hafif Python işletim sistemini (Image) seçiyoruz
FROM python:3.11-slim

# 2. Konteynerin içinde çalışacağımız ana klasörü belirliyoruz
WORKDIR /app

# 3. Önce GEREKSİNİMLERİ kopyalıyoruz (Docker Cache optimizasyonu için)
COPY requirements.txt .

# 4. Kütüphaneleri kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Yazdığımız main.py kodunu içeri kopyalıyoruz
COPY . .

# 6. Uygulamanın dış dünyayla haberleşeceği portu açıyoruz
EXPOSE 8000

# 7. Konteyner ayağa kalktığında çalıştırılacak komut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]