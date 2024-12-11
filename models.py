# models.py

from sqlalchemy import Column, String, Integer, Date, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from db_config import engine

Base = declarative_base()

class Karyawan(Base):
    __tablename__ = 'karyawan'
    karyawan_id = Column(String(5), primary_key=True)
    employee_name = Column(String(50), nullable=False)
    position = Column(String(25), nullable=False)
    
    # Relationships
    transaksi = relationship('Transaksi', back_populates='karyawan')
    absensi = relationship('Absensi', back_populates='karyawan')
    penggajian = relationship('Penggajian', back_populates='karyawan')
    feedbacks = relationship('Feedback', back_populates='karyawan')
    jadwal_kerja = relationship('JadwalKerja', back_populates='karyawan')

class Pelanggan(Base):
    __tablename__ = 'pelanggan'
    pelanggan_id = Column(String(5), primary_key=True)
    cus_name = Column(String(50), nullable=False)
    contact_info = Column(String(15), nullable=False)
    
    # Relationships
    transaksi = relationship('Transaksi', back_populates='pelanggan')
    feedbacks = relationship('Feedback', back_populates='pelanggan')

class Menu(Base):
    __tablename__ = 'menu'
    menu_id = Column(String(5), primary_key=True)
    nama_menu = Column(String(50), nullable=False)
    harga = Column(DECIMAL(15,2), nullable=False)
    
    # Relationships
    detail_transaksi = relationship('DetailTransaksi', back_populates='menu')
    komposisi_menu = relationship('KomposisiMenu', back_populates='menu')

class BahanBaku(Base):
    __tablename__ = 'bahan_baku'
    bahan_id = Column(String(5), primary_key=True)
    nama_bahan = Column(String(50), nullable=False)
    stock = Column(Integer, nullable=False)
    satuan = Column(String(20), nullable=False)
    harga_bahan = Column(DECIMAL(15,2), nullable=False)
    supplier_id = Column(String(5), ForeignKey('supplier.supplier_id'))
    
    # Relationships
    supplier = relationship('Supplier', back_populates='bahan_baku')
    komposisi_menu = relationship('KomposisiMenu', back_populates='bahan_baku')
    detail_pemesanan = relationship('DetailPemesananBahan', back_populates='bahan_baku')

class Supplier(Base):
    __tablename__ = 'supplier'
    supplier_id = Column(String(5), primary_key=True)
    supplier_name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    
    # Relationships
    bahan_baku = relationship('BahanBaku', back_populates='supplier')
    pemesanan_bahan = relationship('PemesananBahan', back_populates='supplier')

class Transaksi(Base):
    __tablename__ = 'transaksi'
    transaksi_id = Column(String(5), primary_key=True)
    tanggal_pembelian = Column(Date, nullable=False)
    pelanggan_id = Column(String(5), ForeignKey('pelanggan.pelanggan_id'), nullable=False)
    karyawan_id = Column(String(5), ForeignKey('karyawan.karyawan_id'), nullable=False)
    total_transaksi = Column(DECIMAL(15,2), nullable=False)
    
    # Relationships
    pelanggan = relationship('Pelanggan', back_populates='transaksi')
    karyawan = relationship('Karyawan', back_populates='transaksi')
    detail_transaksi = relationship('DetailTransaksi', back_populates='transaksi')

class DetailTransaksi(Base):
    __tablename__ = 'detail_transaksi'
    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    transaksi_id = Column(String(5), ForeignKey('transaksi.transaksi_id'), nullable=False)
    menu_id = Column(String(5), ForeignKey('menu.menu_id'), nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga = Column(DECIMAL(15,2), nullable=False)
    
    # Relationships
    transaksi = relationship('Transaksi', back_populates='detail_transaksi')
    menu = relationship('Menu', back_populates='detail_transaksi')

class KomposisiMenu(Base):
    __tablename__ = 'komposisi_menu'
    menu_id = Column(String(5), ForeignKey('menu.menu_id'), primary_key=True)
    bahan_id = Column(String(5), ForeignKey('bahan_baku.bahan_id'), primary_key=True)
    jumlah_bahan = Column(Integer, nullable=False)
    
    # Relationships
    menu = relationship('Menu', back_populates='komposisi_menu')
    bahan_baku = relationship('BahanBaku', back_populates='komposisi_menu')

class Absensi(Base):
    __tablename__ = 'absensi'
    absensi_id = Column(Integer, primary_key=True, autoincrement=True)
    karyawan_id = Column(String(5), ForeignKey('karyawan.karyawan_id'), nullable=False)
    tanggal = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)
    
    # Relationships
    karyawan = relationship('Karyawan', back_populates='absensi')

class Penggajian(Base):
    __tablename__ = 'penggajian'
    penggajian_id = Column(Integer, primary_key=True, autoincrement=True)
    karyawan_id = Column(String(5), ForeignKey('karyawan.karyawan_id'), nullable=False)
    bulan = Column(Integer, nullable=False)
    tahun = Column(Integer, nullable=False)
    jumlah_gaji = Column(DECIMAL(15,2), nullable=False)
    
    # Relationships
    karyawan = relationship('Karyawan', back_populates='penggajian')

class PemesananBahan(Base):
    __tablename__ = 'pemesanan_bahan'
    pemesanan_id = Column(String(5), primary_key=True)
    supplier_id = Column(String(5), ForeignKey('supplier.supplier_id'), nullable=False)
    tanggal_pemesanan = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    
    # Relationships
    supplier = relationship('Supplier', back_populates='pemesanan_bahan')
    detail_pemesanan = relationship('DetailPemesananBahan', back_populates='pemesanan_bahan')

class DetailPemesananBahan(Base):
    __tablename__ = 'detail_pemesanan_bahan'
    detail_pemesanan_id = Column(Integer, primary_key=True, autoincrement=True)
    pemesanan_id = Column(String(5), ForeignKey('pemesanan_bahan.pemesanan_id'), nullable=False)
    bahan_id = Column(String(5), ForeignKey('bahan_baku.bahan_id'), nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(DECIMAL(15,2), nullable=False)
    
    # Relationships
    pemesanan_bahan = relationship('PemesananBahan', back_populates='detail_pemesanan')
    bahan_baku = relationship('BahanBaku', back_populates='detail_pemesanan')

class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    pelanggan_id = Column(String(5), ForeignKey('pelanggan.pelanggan_id'), nullable=False)
    karyawan_id = Column(String(5), ForeignKey('karyawan.karyawan_id'), nullable=False)
    tanggal = Column(Date, nullable=False)
    komentar = Column(Text, nullable=False)
    
    # Relationships
    pelanggan = relationship('Pelanggan', back_populates='feedbacks')
    karyawan = relationship('Karyawan', back_populates='feedbacks')

class JadwalKerja(Base):
    __tablename__ = 'jadwal_kerja'
    jadwal_id = Column(Integer, primary_key=True, autoincrement=True)
    karyawan_id = Column(String(5), ForeignKey('karyawan.karyawan_id'), nullable=False)
    tanggal = Column(Date, nullable=False)
    shift = Column(String(10), nullable=False)
    
    # Relationships
    karyawan = relationship('Karyawan', back_populates='jadwal_kerja')


# Membuat semua tabel di database (jika belum ada)
Base.metadata.create_all(bind=engine)

