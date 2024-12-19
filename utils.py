# utils.py

from sqlalchemy.orm import Session
from models import Base

def get_all(session: Session, model):
    """Mengambil semua entri dari model tertentu."""
    return session.query(model).all()

def get_by_id(session: Session, model, id_value, id_field):
    """Mengambil entri berdasarkan ID dari model tertentu."""
    return session.query(model).filter(id_field == id_value).first()

def add_instance(session: Session, instance):
    """Menambahkan instansi baru ke database."""
    session.add(instance)
    session.commit()

def update_instance(session: Session):
    """Menyimpan perubahan pada database."""
    session.commit()

def delete_instance(session: Session, instance):
    """Menghapus instansi dari database."""
    session.delete(instance)
    session.commit()
