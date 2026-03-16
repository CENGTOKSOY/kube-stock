import os
import pika
import json
import uuid
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(title="Kube-Stock Order Service", version="1.1.0")

# --- ÇEVRESEL DEĞİŞKENLER (K8s'ten Gelecek) ---
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
DB_URL = os.getenv("DB_URL", "postgresql://admin:password123@localhost:5432/kubestock")

# --- VERİTABANI BAĞLANTISI (SQLAlchemy) ---
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Sipariş Tablosu Şeması
class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String)


# Tabloları veritabanında otomatik oluştur
Base.metadata.create_all(bind=engine)


# Veritabanı Oturumu (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- RABBITMQ FONKSİYONU ---
def send_to_queue(order_data):
    try:
        parameters = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='order_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=json.dumps(order_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        return True
    except Exception as e:
        print(f"RabbitMQ Hatası: {e}")
        return False


# --- UÇ NOKTALAR (ENDPOINTS) ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders")
def create_order(product_id: str, quantity: int, db: Session = Depends(get_db)):
    order_id = str(uuid.uuid4())

    # 1. Önce Veritabanına YAZ
    new_order = Order(id=order_id, product_id=product_id, quantity=quantity, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_data = {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "pending"
    }

    # 2. Sonra RabbitMQ'ya FIRLAT
    is_sent = send_to_queue(order_data)

    if is_sent:
        return {"message": "Sipariş veritabanına kaydedildi ve kuyruğa eklendi!", "order_id": order_id}
    else:
        return {"message": "Sipariş kaydedildi ama kuyruğa iletilemedi.", "status": "warning"}