from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BarangDB, RekomendasiRequest
from config import call_groq
import json

router = APIRouter(prefix="/ai", tags=["AI - Rekomendasi"])


@router.post("/rekomendasi")
def rekomendasi_barang(request: RekomendasiRequest, db: Session = Depends(get_db)):
    """
    Dapatkan rekomendasi barang serupa menggunakan AI.

    - **barang_id**: ID barang yang ingin dicari rekomendasinya
    """
    barang = db.query(BarangDB).filter(BarangDB.id == request.barang_id).first()
    if not barang:
        raise HTTPException(status_code=404, detail=f"Barang ID {request.barang_id} tidak ditemukan")

    semua_barang = db.query(BarangDB).filter(BarangDB.id != request.barang_id).all()
    if not semua_barang:
        raise HTTPException(status_code=404, detail="Tidak ada barang lain untuk direkomendasikan")

    daftar_barang = [
        {
            "id":       b.id,
            "nama":     b.nama,
            "kategori": b.kategori,
            "kondisi":  b.kondisi,
            "harga":    b.harga,
            "kota":     b.kota_penjual
        }
        for b in semua_barang
    ]

    response = call_groq(
        system_prompt="""Kamu adalah sistem rekomendasi barang preloved yang cerdas.
        Analisis barang yang dipilih dan rekomendasikan barang lain yang paling relevan.
        Pertimbangkan: kategori, kondisi, harga yang mirip, dan relevansi.
        Jawab HANYA dalam format JSON tanpa markdown:
        {
            "rekomendasi": [
                {
                    "id": 1,
                    "nama": "nama barang",
                    "alasan": "kenapa direkomendasikan"
                }
            ],
            "ringkasan": "penjelasan singkat rekomendasi"
        }
        Maksimal 3 rekomendasi, urutkan dari yang paling relevan.""",
        user_message=f"""Barang yang dipilih:
        - Nama: {barang.nama}
        - Kategori: {barang.kategori}
        - Kondisi: {barang.kondisi}
        - Harga: Rp{barang.harga:,.0f}
        - Kota: {barang.kota_penjual}
        - Deskripsi: {barang.deskripsi or 'tidak ada'}

        Daftar barang tersedia:
        {json.dumps(daftar_barang, ensure_ascii=False)}

        Rekomendasikan maksimal 3 barang paling relevan."""
    )

    return {
        "status": "success",
        "barang_dipilih": {
            "id":       barang.id,
            "nama":     barang.nama,
            "kategori": barang.kategori,
            "harga":    f"Rp{barang.harga:,.0f}"
        },
        "data": response
    }