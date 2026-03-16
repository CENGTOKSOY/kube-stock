
# ☸️ Kube-Stock

**Event-Driven Polyglot Microservices on Kubernetes**

Kube-Stock is a cloud-native microservices project demonstrating how multiple services written in different languages can communicate through an event-driven architecture.

The system uses Python (FastAPI), Node.js, and Go services connected through RabbitMQ, with persistent data stored in PostgreSQL. All services are orchestrated using Kubernetes, making the project a practical demonstration of modern distributed systems.

The repository is designed to be educational, reproducible, and production-inspired, and can run locally using Minikube.

---

## ✨ Features

- ⚡ Event-Driven Microservices Architecture
- 🐇 RabbitMQ based asynchronous communication
- 🧠 Polyglot microservices (Python, Node.js, Go)
- ☸️ Kubernetes native deployments
- 🗄️ PostgreSQL persistent storage with PVC
- 🔁 Multi-replica service scalability
- 🌐 Internal service discovery via Kubernetes DNS
- 🚀 Zero-downtime deployments
- 🔒 Secure internal networking

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestration | Kubernetes |
| Containerization | Docker |
| Message Broker | RabbitMQ |
| Database | PostgreSQL |
| Order Service | Python (FastAPI) |
| Inventory Service | Node.js |
| Notification Service | Go |
| Local Cluster | Minikube |

---
## 📂 Project Structure

kube-stock/
│
├── docker-compose.yml
│
├── k8s/
│   ├── inventory-deployment.yaml
│   ├── notification-deployment.yaml
│   ├── order-deployment.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-pv.yaml
│   └── rabbitmq-deployment.yaml
│
├── scripts/
│   └── setup.sh
│
└── services/
    ├── inventory-service/
    │   ├── Dockerfile
    │   ├── index.js
    │   └── package.json
    │
    ├── notification-service/
    │   ├── Dockerfile
    │   ├── go.mod
    │   └── main.go
    │
    └── order-service/
        ├── Dockerfile
        ├── main.py
        └── requirements.txt

## 🧠 Architecture Overview

Kube-Stock follows a clean event-driven microservice pattern.

| Service | Language | Responsibility | Communication |
|---------|----------|----------------|---------------|
| Order Service | Python (FastAPI) | Accepts orders, writes to PostgreSQL, publishes events | REST → DB → RabbitMQ |
| Inventory Service | Node.js | Consumes order events and reserves stock | RabbitMQ Consumer |
| Notification Service | Go | Processes order notifications | RabbitMQ Consumer |
| RabbitMQ | Message Broker | Asynchronous communication backbone | AMQP |
| PostgreSQL | Database | Persistent order storage | Stateful |

---

## 🛠️ Prerequisites

Make sure the following tools are installed:
- Docker
- Docker Desktop
- Minikube
- kubectl
- Python 3.11+
- Node.js 18+
- Go 1.20+

---

## 🚀 Installation & Setup

**1️⃣ Start the Kubernetes Cluster**

```bash
minikube start --driver=docker
```

---

**2️⃣ Build Service Images**

```bash
docker build -t kube-stock-order-service:v2 ./services/order-service
docker build -t kube-stock-inventory-service:latest ./services/inventory-service
docker build -t kube-stock-notification-service:latest ./services/notification-service
```

---

**3️⃣ Load Images into Minikube**

```bash
minikube image load kube-stock-order-service:v2 \
kube-stock-inventory-service:latest \
kube-stock-notification-service:latest
```

---

**4️⃣ Deploy Infrastructure**

```bash
kubectl apply -f k8s/rabbitmq-deployment.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
```

---

**5️⃣ Deploy Application Services**

```bash
kubectl apply -f k8s/inventory-deployment.yaml
kubectl apply -f k8s/notification-deployment.yaml
kubectl apply -f k8s/order-deployment.yaml
```

Check deployment status:

```bash
kubectl get pods
kubectl get svc
```

---

## 🧪 End-to-End Testing

**Access the Order API**

```bash
minikube service order-service
```

Then open:

```
/docs
```

You will see the FastAPI Swagger UI.

---

**Send a Test Order**

Example request:

```bash
curl -X POST \
"http://<ORDER-SERVICE-URL>/orders?product_id=MacBook-pro-m3pro&quantity=2" \
-H "accept: application/json" \
-d ""
```

---

**Verify Event Processing**

```bash
kubectl logs -f -l app=inventory-service
```

Expected output:

```
Order received
Stock checked
Reservation successful
Message ACKed
```

---

**RabbitMQ Management Panel**

```bash
kubectl port-forward svc/rabbitmq 15672:15672
```

Open in browser:

```
http://localhost:15672
```

Login credentials:

```
guest / guest
```

---

**Verify PostgreSQL Data**

Find the PostgreSQL pod:

```bash
kubectl get pods -l app=postgres
```

Connect to database:

```bash
kubectl exec -it <POSTGRES_POD> -- psql -U admin -d kubestock
```

Run query:

```sql
SELECT * FROM orders;
```

---

## 📸 Project Screenshots

**Docker Images**

![Docker Images](images/Ekran%20Resmi%202026-03-16%2012.52.27.png)

**Inventory Service Logs**

![Inventory Logs](images/Ekran%20Resmi%202026-03-16%2012.48.10.png)

**Swagger Order API**

![Swagger API](images/Ekran%20Resmi%202026-03-16%2012.50.03.png)

**Kubernetes Pods**

![Kubernetes Pods](images/Ekran%20Resmi%202026-03-16%2012.54.41.png)

**Docker Containers**

![Docker Containers](images/Ekran%20Resmi%202026-03-16%2012.55.12.png)

**Docker Containers Detailed**

![Docker Containers](images/Ekran%20Resmi%202026-03-16%2012.56.03.png)

**Minikube Container Stats**

![Minikube Stats](images/Ekran%20Resmi%202026-03-16%2012.57.22.png)

**PostgreSQL Query Result**

![Postgres Query](images/Ekran%20Resmi%202026-03-16%2012.58.44.png)

**RabbitMQ Queue**

![RabbitMQ Queue](images/Ekran%20Resmi%202026-03-16%2012.59.30.png)

**RabbitMQ Overview**

![RabbitMQ Overview](images/Ekran%20Resmi%202026-03-16%2013.00.12.png)

**RabbitMQ Login**

![RabbitMQ Login](images/Ekran%20Resmi%202026-03-16%2013.01.05.png)

**Swagger API Example**

![Swagger API](images/Ekran%20Resmi%202026-03-16%2013.02.44.png)

---

## 🎯 Purpose of the Project

Kube-Stock was developed to:
- Demonstrate event-driven microservices
- Practice polyglot service architecture
- Learn Kubernetes deployments
- Implement message-based service communication
- Simulate real-world distributed system design

---

## 📈 Future Improvements

- Helm chart support
- Prometheus monitoring
- Grafana dashboards
- Centralized logging (ELK / Loki)
- CI/CD pipeline integration
- Kubernetes Secrets for credentials
- Cloud deployment (AWS / GCP)

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/YourFeature
```

3. Commit changes

```bash
git commit -m "Add YourFeature"
```

4. Push branch

```bash
git push origin feature/YourFeature
```

5. Open a Pull Request

---

## 📜 License

MIT License

---

## 👤 Author

**Ali Toksoy**

GitHub: [https://github.com/CENGTOKSOY](https://github.com/CENGTOKSOY)

---

## ⭐ Support

If you find this project useful, consider giving it a star ⭐ on GitHub.

---
