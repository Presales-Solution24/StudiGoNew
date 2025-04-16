
# ✅ Masuk ke container flask_api dan jalankan shell interaktif (opsional)
docker-compose exec flask_api sh

# ✅ Inisialisasi migration folder (hanya 1x di awal proyek)
docker-compose exec flask_api flask db init

# ✅ Generate migration script berdasarkan perubahan model (setiap kali ubah model)
docker-compose exec flask_api flask db migrate -m "deskripsi perubahan"

# ✅ Terapkan perubahan ke database (jalankan setelah migrate)
docker-compose exec flask_api flask db upgrade

# ✅ Downgrade ke migration sebelumnya (kalau perlu rollback)
docker-compose exec flask_api flask db downgrade

# ✅ Lihat history migration
docker-compose exec flask_api flask db history

# ✅ Cek status migration saat ini
docker-compose exec flask_api flask db current
