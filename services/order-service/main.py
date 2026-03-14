from fastapi import FastAPI
import uuid

app = FastAPI(title="Kube-Stock Order Service", version="1.0.0")


# --- CLOUD ARCHITECT DETAYI: Health Check ---
# K8s bu adrese saniyede bir ping atar. Cevap alamazsa pod'u acımasızca siler ve yenisini açar.
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}


# --- SİPARİŞ ALMA UCU ---
@app.post("/orders")
def create_order(product_id: str, quantity: int):
    order_id = str(uuid.uuid4())

    # İleride burada doğrudan veritabanına YAZMAYACAĞIZ.
    # Bu veriyi alıp RabbitMQ'ya fırlatacağız (Event-Driven).
    # Şimdilik mimariyi ayağa kaldırmak için sahte (mock) yanıt dönüyoruz.
    return {
        "message": "Sipariş kuyruğa eklendi",
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "processing"
    }