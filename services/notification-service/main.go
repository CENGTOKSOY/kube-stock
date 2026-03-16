package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// Sağlık durumu için veri yapısı
type HealthResponse struct {
	Status  string `json:"status"`
	Service string `json:"service"`
}

func main() {
	// --- CLOUD ARCHITECT DETAYI: Health Check ---
	// K8s'in bu servisi hayatta tutması için gereken can damarı.
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(HealthResponse{Status: "healthy", Service: "notification-service"})
	})

	// --- BİLDİRİM UCU (İleride RabbitMQ'ya bağlanacak) ---
	http.HandleFunc("/notify", func(w http.ResponseWriter, r *http.Request) {
		// Gerçek senaryoda burada SMTP veya Twilio ile e-posta/SMS atılır
		fmt.Println("[x] Kullanıcıya E-Posta / SMS gönderiliyor...")
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Bildirim basariyla gonderildi"}`))
	})

	port := ":8080"
	fmt.Println("Notification Service running on port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}