from fastapi import FastAPI
from database import Base, engine
from routes import barang, search, hitung, ai

# Buat tabel otomatis saat server pertama jalan
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Preloved API",
    description="""
    API untuk platform jual beli barang preloved.

    ## Fitur

    ### 📦 Barang (CRUD)
    - **POST** `/barang` → Tambah barang baru
    - **GET** `/barang` → Lihat semua barang
    - **GET** `/barang/{id}` → Lihat detail barang
    - **PUT** `/barang/{id}` → Update barang
    - **DELETE** `/barang/{id}` → Hapus barang

    ### 🔍 Search
    - **GET** `/search` → Cari & filter barang

    ### 🧮 Hitung
    - **POST** `/hitung/total` → Hitung diskon + ongkir + total

    ### 🤖 AI
    - **POST** `/ai/rekomendasi` → Rekomendasi barang serupa
    """,
    version="1.0.0"
)

app.include_router(barang.router)
app.include_router(search.router)
app.include_router(hitung.router)
app.include_router(ai.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Selamat datang di Preloved API 🛍️",
        "version": "1.0.0",
        "docs": "Buka /docs untuk dokumentasi lengkap",
        "endpoints": {
            "CRUD Barang": [
                "POST   /barang",
                "GET    /barang",
                "GET    /barang/{id}",
                "PUT    /barang/{id}",
                "DELETE /barang/{id}",
            ],
            "Searching":  ["GET  /search"],
            "Komputasi":  ["POST /hitung/total"],
            "AI":         ["POST /ai/rekomendasi"],
        }
    }