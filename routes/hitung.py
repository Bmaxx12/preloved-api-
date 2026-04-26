from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BarangDB, HitungRequest

router = APIRouter(prefix="/hitung", tags=["Hitung - Komputasi"])

# Data ongkir per kota (estimasi dalam Rupiah per kg)
# Asumsi berat barang rata-rata 1 kg
ONGKIR_PER_KOTA = {
    "jakarta":     15000,
    "bandung":     12000,
    "surabaya":    20000,
    "yogyakarta":  15000,
    "semarang":    15000,
    "medan":       35000,
    "makassar":    30000,
    "bali":        25000,
    "palembang":   25000,
    "malang":      20000,
}

ONGKIR_DEFAULT = 40000  # kota lain yang tidak ada di list


@router.post("/total")
def hitung_total(request: HitungRequest, db: Session = Depends(get_db)):
    """
    Hitung total belanja termasuk diskon dan ongkir.

    - **barang_id**: ID barang yang dibeli
    - **jumlah**: Jumlah barang yang dibeli
    - **diskon_persen**: Persentase diskon (0-100), default 0
    - **kota_tujuan**: Kota tujuan pengiriman
    """
    # Ambil data barang dari database
    barang = db.query(BarangDB).filter(BarangDB.id == request.barang_id).first()
    if not barang:
        raise HTTPException(status_code=404, detail=f"Barang dengan ID {request.barang_id} tidak ditemukan")

    # Cek stok
    if request.jumlah > barang.stok:
        raise HTTPException(
            status_code=400,
            detail=f"Stok tidak cukup. Stok tersedia: {barang.stok}"
        )

    # Validasi diskon
    if not (0 <= request.diskon_persen <= 100):
        raise HTTPException(status_code=400, detail="Diskon harus antara 0 dan 100")

    # ── Komputasi ──────────────────────────────────────────

    # 1. Harga asli total
    harga_asli = barang.harga * request.jumlah

    # 2. Hitung diskon
    nilai_diskon = harga_asli * (request.diskon_persen / 100)
    harga_setelah_diskon = harga_asli - nilai_diskon

    # 3. Hitung ongkir berdasarkan kota tujuan
    kota_key = request.kota_tujuan.lower().strip()
    ongkir = ONGKIR_PER_KOTA.get(kota_key, ONGKIR_DEFAULT)

    # 4. Total akhir
    total_akhir = harga_setelah_diskon + ongkir

    # ── Response ───────────────────────────────────────────
    return {
        "status": "success",
        "data": {
            "barang": {
                "id":       barang.id,
                "nama":     barang.nama,
                "kondisi":  barang.kondisi,
                "kategori": barang.kategori,
            },
            "rincian_harga": {
                "harga_satuan":        f"Rp{barang.harga:,.0f}",
                "jumlah":              request.jumlah,
                "harga_asli_total":    f"Rp{harga_asli:,.0f}",
                "diskon":              f"{request.diskon_persen}%",
                "nilai_diskon":        f"Rp{nilai_diskon:,.0f}",
                "harga_setelah_diskon":f"Rp{harga_setelah_diskon:,.0f}",
                "ongkir_ke":           request.kota_tujuan.title(),
                "biaya_ongkir":        f"Rp{ongkir:,.0f}",
                "total_akhir":         f"Rp{total_akhir:,.0f}",
            },
            "catatan": "Ongkir merupakan estimasi, harga final dapat berbeda tergantung ekspedisi"
        }
    }