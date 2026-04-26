from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BarangDB, BarangCreate, BarangUpdate, BarangResponse
from typing import List

router = APIRouter(prefix="/barang", tags=["Barang - CRUD"])


@router.post("/", response_model=BarangResponse)
def tambah_barang(barang: BarangCreate, db: Session = Depends(get_db)):
    """Tambah barang preloved baru"""
    db_barang = BarangDB(**barang.model_dump())
    db.add(db_barang)
    db.commit()
    db.refresh(db_barang)
    return db_barang


@router.get("/", response_model=List[BarangResponse])
def get_semua_barang(db: Session = Depends(get_db)):
    """Ambil semua daftar barang preloved"""
    return db.query(BarangDB).all()


@router.get("/{barang_id}", response_model=BarangResponse)
def get_barang(barang_id: int, db: Session = Depends(get_db)):
    """Ambil detail satu barang berdasarkan ID"""
    barang = db.query(BarangDB).filter(BarangDB.id == barang_id).first()
    if not barang:
        raise HTTPException(status_code=404, detail=f"Barang dengan ID {barang_id} tidak ditemukan")
    return barang


@router.put("/{barang_id}", response_model=BarangResponse)
def update_barang(barang_id: int, barang_update: BarangUpdate, db: Session = Depends(get_db)):
    """Update data barang, hanya field yang diisi yang akan diupdate"""
    barang = db.query(BarangDB).filter(BarangDB.id == barang_id).first()
    if not barang:
        raise HTTPException(status_code=404, detail=f"Barang dengan ID {barang_id} tidak ditemukan")

    update_data = barang_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(barang, field, value)

    db.commit()
    db.refresh(barang)
    return barang


@router.delete("/{barang_id}")
def hapus_barang(barang_id: int, db: Session = Depends(get_db)):
    """Hapus barang berdasarkan ID"""
    barang = db.query(BarangDB).filter(BarangDB.id == barang_id).first()
    if not barang:
        raise HTTPException(status_code=404, detail=f"Barang dengan ID {barang_id} tidak ditemukan")

    db.delete(barang)
    db.commit()

    return {
        "status": "success",
        "message": f"Barang '{barang.nama}' berhasil dihapus"
    }