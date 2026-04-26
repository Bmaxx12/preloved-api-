from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from database import Base


# ============================================================
# DATABASE MODEL (struktur tabel PostgreSQL)
# ============================================================

class BarangDB(Base):
    """Model tabel barang di database"""
    __tablename__ = "barang"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama         = Column(String, nullable=False)
    kategori     = Column(String, nullable=False)
    kondisi      = Column(String, nullable=False)
    harga        = Column(Float, nullable=False)
    deskripsi    = Column(String, nullable=True)
    kota_penjual = Column(String, nullable=False)
    stok         = Column(Integer, default=1)
    created_at   = Column(DateTime, default=func.now())
    updated_at   = Column(DateTime, default=func.now(), onupdate=func.now())


# ============================================================
# PYDANTIC SCHEMA
# ============================================================

class BarangCreate(BaseModel):
    nama:         str
    kategori:     str
    kondisi:      str
    harga:        float
    deskripsi:    Optional[str] = None
    kota_penjual: str
    stok:         int = 1


class BarangUpdate(BaseModel):
    nama:         Optional[str]   = None
    kategori:     Optional[str]   = None
    kondisi:      Optional[str]   = None
    harga:        Optional[float] = None
    deskripsi:    Optional[str]   = None
    kota_penjual: Optional[str]   = None
    stok:         Optional[int]   = None


class BarangResponse(BaseModel):
    id:           int
    nama:         str
    kategori:     str
    kondisi:      str
    harga:        float
    deskripsi:    Optional[str]
    kota_penjual: str
    stok:         int

    class Config:
        from_attributes = True


class HitungRequest(BaseModel):
    barang_id:     int
    jumlah:        int   = 1
    diskon_persen: float = 0
    kota_tujuan:   str


class RekomendasiRequest(BaseModel):
    barang_id: int