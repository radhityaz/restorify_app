-- Pembuatan database (opsional, jika belum dibuat)
CREATE DATABASE IF NOT EXISTS restorify;
USE restorify;

-- Tabel karyawan
CREATE TABLE IF NOT EXISTS karyawan (
    karyawan_id VARCHAR(255) PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL,
    position VARCHAR(25) NOT NULL
);

-- Tabel pelanggan
CREATE TABLE IF NOT EXISTS pelanggan (
    pelanggan_id VARCHAR(255) PRIMARY KEY,
    cus_name VARCHAR(50) NOT NULL,
    contact_info VARCHAR(255) NOT NULL
);

-- Tabel supplier
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id VARCHAR(255) PRIMARY KEY,
    supplier_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL
);

-- Tabel bahan_baku
CREATE TABLE IF NOT EXISTS bahan_baku (
    bahan_id VARCHAR(255) PRIMARY KEY,
    nama_bahan VARCHAR(50) NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0),
    satuan VARCHAR(20) NOT NULL,
    harga_bahan DECIMAL(15,2) NOT NULL,
    supplier_id VARCHAR(255),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);

-- Tabel menu
CREATE TABLE IF NOT EXISTS menu (
    menu_id VARCHAR(255) PRIMARY KEY,
    nama_menu VARCHAR(50) NOT NULL,
    harga DECIMAL(15,2) NOT NULL CHECK (harga >= 0)
);

-- Tabel transaksi
CREATE TABLE IF NOT EXISTS transaksi (
    transaksi_id VARCHAR(255) PRIMARY KEY,
    tanggal_pembelian DATE NOT NULL,
    pelanggan_id VARCHAR(255) NOT NULL,
    karyawan_id VARCHAR(255) NOT NULL,
    total_transaksi DECIMAL(15,2) NOT NULL CHECK (total_transaksi >= 0),
    FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(pelanggan_id),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

-- Tabel detail_transaksi
CREATE TABLE IF NOT EXISTS detail_transaksi (
    detail_id INT PRIMARY KEY AUTO_INCREMENT,
    transaksi_id VARCHAR(255) NOT NULL,
    menu_id VARCHAR(255) NOT NULL,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    harga DECIMAL(15,2) NOT NULL CHECK (harga >= 0),
    FOREIGN KEY (transaksi_id) REFERENCES transaksi(transaksi_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

-- Tabel komposisi_menu
CREATE TABLE IF NOT EXISTS komposisi_menu (
    menu_id VARCHAR(255) NOT NULL,
    bahan_id VARCHAR(255) NOT NULL,
    jumlah_bahan INT NOT NULL CHECK (jumlah_bahan > 0),
    PRIMARY KEY (menu_id, bahan_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    FOREIGN KEY (bahan_id) REFERENCES bahan_baku(bahan_id)
);

-- Tabel absensi
CREATE TABLE IF NOT EXISTS absensi (
    absensi_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(255) NOT NULL,
    tanggal DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

-- Tabel penggajian
CREATE TABLE IF NOT EXISTS penggajian (
    penggajian_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(255) NOT NULL,
    bulan INT NOT NULL CHECK (bulan BETWEEN 1 AND 12),
    tahun INT NOT NULL,
    jumlah_gaji DECIMAL(15,2) NOT NULL CHECK (jumlah_gaji >= 0),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

-- Tabel pemesanan_bahan
CREATE TABLE IF NOT EXISTS pemesanan_bahan (
    pemesanan_id VARCHAR(255) PRIMARY KEY,
    supplier_id VARCHAR(255) NOT NULL,
    tanggal_pemesanan DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);

-- Tabel detail_pemesanan_bahan
CREATE TABLE IF NOT EXISTS detail_pemesanan_bahan (
    detail_pemesanan_id INT PRIMARY KEY AUTO_INCREMENT,
    pemesanan_id VARCHAR(255) NOT NULL,
    bahan_id VARCHAR(255) NOT NULL,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    harga_satuan DECIMAL(15,2) NOT NULL CHECK (harga_satuan >= 0),
    FOREIGN KEY (pemesanan_id) REFERENCES pemesanan_bahan(pemesanan_id),
    FOREIGN KEY (bahan_id) REFERENCES bahan_baku(bahan_id)
);

-- Tabel feedback
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    pelanggan_id VARCHAR(255) NOT NULL,
    karyawan_id VARCHAR(255) NOT NULL,
    tanggal DATE NOT NULL,
    rating INT, -- Rating bisa null jika tidak ada rating
    komentar TEXT,
    FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(pelanggan_id),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

-- Tabel jadwal_kerja
CREATE TABLE IF NOT EXISTS jadwal_kerja (
    jadwal_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(255) NOT NULL,
    tanggal DATE NOT NULL,
    shift VARCHAR(10) NOT NULL,
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);