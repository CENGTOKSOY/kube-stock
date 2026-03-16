const express = require('express');
const amqp = require('amqplib'); // RabbitMQ kütüphanemiz
const app = express();
const PORT = process.env.PORT || 3000;

// Çevresel değişkenlerden RabbitMQ adresini alıyoruz (Docker Compose'dan gelecek)
const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672';

app.use(express.json());

// 1. Health Check (Sağlık Kontrolü)
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy', service: 'inventory-service' });
});

// 2. RabbitMQ Dinleyici (Consumer) Fonksiyonu
async function connectRabbitMQ() {
    try {
        const connection = await amqp.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();
        const queue = 'order_queue';

        // Kuyruğun var olduğundan emin oluyoruz
        await channel.assertQueue(queue, { durable: true });
        console.log(`[*] ${queue} kuyruğu dinleniyor. Mesajlar bekleniyor...`);

        // Kuyruğu sürekli dinle
        channel.consume(queue, (msg) => {
            if (msg !== null) {
                // Mesajı kuyruktan alıp okuyoruz
                const orderData = JSON.parse(msg.content.toString());
                console.log(`\n[+] YENİ SİPARİŞ YAKALANDI!`);
                console.log(`    Ürün: ${orderData.product_id} | Miktar: ${orderData.quantity}`);

                // --- BURADA NORMALDE VERİTABANINDAN STOK DÜŞÜLÜR ---
                console.log(`    [x] Stok kontrol edildi, rezerve işlemi başarılı.`);

                // CLOUD ARCHITECT DETAYI: İşlem hatasız bitti, RabbitMQ'ya "Mesajı SİL" diyoruz.
                channel.ack(msg);
                console.log(`    [v] Sipariş tamamlandı, mesaj kuyruktan silindi. ID: ${orderData.order_id}`);
            }
        }, { noAck: false }); // noAck: false -> Otomatik silme! Biz "ack" diyene kadar bekle.

    } catch (error) {
        console.error("[!] RabbitMQ Bağlantı Hatası, 5 saniye sonra tekrar denenecek...", error);
        setTimeout(connectRabbitMQ, 5000); // Hata olursa sistemi çökertme, 5 saniye sonra tekrar dene (Resilience)
    }
}

app.listen(PORT, async () => {
    console.log(`Inventory Service is running on port ${PORT}`);
    // Sunucu ayağa kalkar kalkmaz RabbitMQ'ya bağlan
    await connectRabbitMQ();
});