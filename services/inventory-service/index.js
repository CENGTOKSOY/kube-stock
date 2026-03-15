const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// --- CLOUD ARCHITECT DETAYI: Health Check ---
// Tıpkı Python servisinde olduğu gibi, Kubernetes bu servisin de
// yaşayıp yaşamadığını bu adrese ping atarak anlayacak.
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy', service: 'inventory-service' });
});

// --- STOK KONTROL UCU (Şimdilik HTTP, ileride RabbitMQ olacak) ---
app.post('/inventory/check', (req, res) => {
    const { productId, quantity } = req.body;

    // Normalde burada veritabanına bağlanıp stoğu düşeceğiz.
    // Şimdilik mimariyi test etmek için sahte bir başarılı yanıt dönüyoruz.
    console.log(`[x] Stok kontrol ediliyor: Ürün ${productId}, Miktar: ${quantity}`);

    res.status(200).json({
        message: "Stok yeterli, rezerve edildi.",
        productId: productId,
        reserved: true
    });
});

app.listen(PORT, () => {
    console.log(`Inventory Service is running on port ${PORT}`);
});