# **Face Detection Attendance System**  

## **📌 Overview**  
Sistem **Face Detection Attendance** adalah solusi pencatantan presensi mahasiswa berbasis **pengenalan wajah** yang memanfaatkan **computer vision** untuk mendeteksi dan mengenali wajah mahasiswa secara real-time. Sistem ini terintegrasi dengan **database MySQL (Amazon RDS)** dan di-deploy sebagai **Docker container pada AWS EC2**, memberikan solusi presensi yang akurat, efisien, dan minim interaksi manual.     
Sistem **Face Detection** adalah solusi pencatatan presensi mahasiswa berbasis pengenalan wajah yang memanfaatkan **computer vision** untuk mendeteksi dan mengenali wajah secara real-time. Sistem ini menggunakan ESP32-CAM sebagai perangkat pengambilan citra wajah yang terhubung melalui **wifi** ke backend aplikasi. Citra yang ditangkap dikirimkan ke server untuk diproses oleh modul deteksi dan pencocokan wajah. Seluruh sistem terintegrasi dengan database MySQL (Amazon RDS) dan dijalankan dalam Docker container pada AWS EC2, memberikan solusi presensi yang akurat, efisien, dan minim interaksi manual. Dengan memanfaatkan ESP32-CAM yang hemat daya dan berbiaya rendah, sistem ini menjadi lebih fleksibel untuk implementasi di berbagai ruang kelas atau area kampus.  

---

## **🚀 Tech Stack**  
| Komponen | Teknologi |
|----------|-----------|
| **Backend** | Python 3.9+ |
| **Computer Vision** | OpenCV (cv2), SIFT (Scale-Invariant Feature Transform) |
| **Database** | MySQL (Amazon RDS) |
| **API & ORM** | SQLAlchemy (ORM), PyMySQL (MySQL Connector) |
| **Deployment** | Docker, AWS EC2 |
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
- **Dockerized** untuk kemudahan deployment di **AWS EC2**  
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
- **Deployment via Docker** memudahkan scaling di AWS EC2  
- Database terkelola dengan **Amazon RDS** (high availability)  

### **4. Biaya Operasional Rendah**  
- Menggunakan **ESP32-CAM** (murah) dibandingkan solusi biometrik komersial  
- **Serverless-ready** (bisa diintegrasikan dengan AWS Lambda untuk proses async)  

### **5. Compliance & Audit Trail**  
- Semua data presensi tersimpan terstruktur di **MySQL**  
- Log aktivitas memudahkan audit jika diperlukan  

---

## **🛠️ Struktur Database (MySQL - Amazon RDS)**  
Berikut tabel utama yang digunakan:  

### **1. `Students`**  
| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `student_id` | VARCHAR(36) | ID unik mahasiswa (PK) |
| `name` | VARCHAR(100) | Nama lengkap mahasiswa |
| `photo` | VARCHAR(255) | URL foto mahasiswa (opsional) |

### **2. `Courses`**  
| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `course_id` | VARCHAR(36) | ID mata kuliah (PK) |
| `course_name` | VARCHAR(100) | Nama mata kuliah |

### **3. `CourseEnrollments`**  
| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `enrollment_id` | VARCHAR(36) | ID enroll (PK) |
| `student_id` | VARCHAR(36) | FK ke `Students` |
| `course_id` | VARCHAR(36) | FK ke `Courses` |

### **4. `ClassSessions`**  
| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `session_id` | VARCHAR(36) | ID sesi kelas (PK) |
| `course_id` | VARCHAR(36) | Mata kuliah terkait |
| `date` | DATE | Tanggal sesi |

### **5. `Attendances`**  
| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `attendance_id` | VARCHAR(36) | ID presensi (PK) |
| `session_id` | VARCHAR(36) | Sesi terkait |
| `student_id` | VARCHAR(36) | Mahasiswa yang hadir |
| `timestamp` | DATETIME | Waktu presensi |

---

## **🚀 Deployment (AWS EC2 + Docker)**  
### **1. Prasyarat**  
- **AWS Account** (EC2 + RDS)  
- **Docker** terinstal di EC2  
- **MySQL Database** (Amazon RDS) sudah running  

### **2. Langkah-Langkah**  
#### **🔹 A. Konfigurasi Database (RDS)**  
1. Buat database MySQL di **Amazon RDS**  
2. Set security group untuk mengizinkan akses dari **EC2 instance**  
3. Simpan **endpoint RDS**, **username**, dan **password**  

#### **🔹 B. Setup EC2 Instance**  
1. Launch EC2 instance (Ubuntu 22.04 LTS)  
2. Install Docker:  
   ```bash
   sudo apt update && sudo apt install docker.io -y
   sudo systemctl enable docker
   ```
3. Clone repository:  
   ```bash
   git clone [REPO_URL] && cd face_detection
   ```

#### **🔹 C. Konfigurasi Environment**  
Buat file `.env` di root project:  
```ini
# Database
DB_HOST=[RDS_ENDPOINT]
DB_PORT=3306
DB_USER=admin
DB_PASS=[RDS_PASSWORD]
DB_NAME=attendance_db

# Camera
CAMERA_URL=http://[ESP32_IP]:81/stream

# App Settings
MIN_MATCH_COUNT=10
LOG_LEVEL=INFO
```

#### **🔹 D. Build & Run Docker Container**  
```bash
docker-compose build
docker-compose up -d

```

#### **🔹 E. Verifikasi**  
- Cek logs:  
```bash
 docker logs -f face-detector
```

---

## **📈 Roadmap Pengembangan**  
- [ ] **Face Recognition dengan Deep Learning** (FaceNet/ArcFace)  
- [ ] **Analisis Ekspresi Wajah** (Senang, Netral, Lelah)  
- [ ] **Notifikasi Real-time** (Telegram/Slack saat presensi)  
- [ ] **Multi-Camera Support** untuk ruangan besar  

---

## **📜 License**  
Proyek ini dilisensikan di bawah **MIT License**.  

---
