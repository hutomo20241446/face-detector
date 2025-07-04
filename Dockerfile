# ---------- Build stage ----------
FROM python:3.8.20-slim AS builder

WORKDIR /app

# Salin file dependencies terlebih dahulu agar layer caching lebih efektif
COPY requirements.txt .

# Instal dependensi tanpa menyimpan cache
RUN pip install --user --no-cache-dir -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.8.20-slim

WORKDIR /app

# Set environment lebih awal
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

# Salin environment Python dari builder
COPY --from=builder /root/.local /root/.local

# Salin semua source code
COPY . .

# Gunakan entrypoint agar fleksibel dalam eksekusi
ENTRYPOINT ["python", "main.py"]
