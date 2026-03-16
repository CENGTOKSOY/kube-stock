# --- 1. AŞAMA: İNŞA (Builder) ---
# Sadece derleme işlemini yapacak ağır ve dolu işletim sistemi
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod ./
COPY main.go ./

# Kaynak kodumuzu Linux'ta çalışacak tek bir çalıştırılabilir (exe) dosyaya dönüştürüyoruz
RUN CGO_ENABLED=0 GOOS=linux go build -o notification-service .

# --- 2. AŞAMA: CANLI ORTAM (Production) ---
# Sadece 5 MB boyutunda, bomboş ve çok güvenli bir işletim sistemi
FROM alpine:latest

WORKDIR /root/

# 1. aşamadaki o devasa kütüphaneleri ve kodları bırakıp, SADECE derlenmiş hazır programı alıyoruz
COPY --from=builder /app/notification-service .

# Dış dünyaya açılacak port (main.go içinde 8080 belirlemiştik)
EXPOSE 8080

# Konteyner ayağa kalktığında çalıştırılacak program
CMD ["./notification-service"]