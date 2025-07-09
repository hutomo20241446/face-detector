# **Face Detection Attendance System**  

## **📌 Overview**      
Sistem **Face Detection** adalah solusi pencatatan presensi mahasiswa berbasis pengenalan wajah yang memanfaatkan **computer vision** untuk mendeteksi dan mengenali wajah secara real-time. Sistem ini menggunakan ESP32-CAM sebagai perangkat pengambilan citra wajah yang terhubung melalui **wifi** ke backend aplikasi. Citra yang ditangkap dikirimkan ke server untuk diproses oleh modul deteksi dan pencocokan wajah. Seluruh sistem terintegrasi dengan database MySQL (Amazon RDS) dan dijalankan dalam Docker container pada Railway, memberikan solusi presensi yang akurat, efisien, dan minim interaksi manual. Dengan memanfaatkan ESP32-CAM yang hemat daya dan berbiaya rendah, sistem ini menjadi lebih fleksibel untuk implementasi di berbagai ruang kelas atau area kampus.  

---

## **🚀 Tech Stack**  
| Komponen | Teknologi |
|----------|-----------|
| **Backend** | Python 3.9+ |
| **Computer Vision** | OpenCV (cv2), SIFT (Scale-Invariant Feature Transform) |
| **Database** | MySQL (Amazon RDS) |
| **API & ORM** | SQLAlchemy (ORM), PyMySQL (MySQL Connector) |
| **Deployment** | Docker, Railway |
| **Networking** | ESP32-CAM (Live Video Stream via HTTP) |
| **Logging & Monitoring** | Python `logging` |
| **Storage** | Amazon S3 (Photos storage) |

---

## **✨ Fitur Utama**  
✅ **Deteksi Wajah Real-time**  
- Menggunakan **ESP32-CAM** untuk streaming video langsung  
- Proses deteksi berbasis **SIFT** untuk pencocokan fitur wajah  

✅ **Presensi Otomatis**  
- Mencatat kehadiran mahasiswa secara otomatis saat wajah terdeteksi  
- Memastikan **tidak ada duplikasi presensi** dalam periode tertentu  

✅ **Integrasi Database**  
- Menyimpan data kehadiran di **Amazon RDS (MySQL)**  
- Mendukung operasi CRUD melalui **SQLAlchemy**  

✅ **Optimasi & Scalability**  
- **Dockerized** untuk kemudahan deployment di **Railway**  
- **Connection Pooling** untuk efisiensi koneksi database  
- **Retry Mechanism** jika terjadi gangguan jaringan  

✅ **Keamanan & Monitoring**  
- Logging aktivitas deteksi dan error  
- Backup otomatis fitur wajah ke **Amazon S3** (opsional)  

---

## **💼 Keuntungan Bisnis**  
### **1. Efisiensi Waktu & SDM**  
- Mengurangi kebutuhan **manual attendance** (tidak perlu absen manual)  
- Meminimalkan **human error** dalam pencatatan kehadiran  

### **2. Akurasi Tinggi**  
- **False-positive rendah** berkat algoritma **SIFT**  
- Mampu membedakan mahasiswa yang mirip sekalipun  

### **3. Scalable & Cloud-Ready**  
- **Deployment via Docker** memudahkan scaling di Railway  
- Database terkelola dengan **Amazon RDS** (high availability)  

### **4. Biaya Operasional Rendah**  
- Menggunakan **ESP32-CAM** (murah) dibandingkan solusi biometrik komersial  
- **Serverless-ready** (bisa diintegrasikan dengan AWS Lambda untuk proses async)  

### **5. Compliance & Audit Trail**  
- Semua data presensi tersimpan terstruktur di **MySQL**  
- Log aktivitas memudahkan audit jika diperlukan 

---

## **📈 Roadmap Pengembangan**  
- [ ] **Face Recognition dengan Deep Learning** (FaceNet/ArcFace)  
- [ ] **Analisis Ekspresi Wajah** (Senang, Netral, Lelah)  
- [ ] **Notifikasi Real-time** (Telegram/Slack saat presensi)  
- [ ] **Multi-Camera Support** untuk ruangan besar  

---
