-- Pembuatan database (opsional, jika belum dibuat)
CREATE DATABASE IF NOT EXISTS restorify;
USE restorify;

-- Tabel karyawan
CREATE TABLE IF NOT EXISTS karyawan (
    karyawan_id VARCHAR(5) PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL,
    position VARCHAR(25) NOT NULL
);

INSERT INTO karyawan (karyawan_id, employee_name, position) VALUES
    ('K001', 'Adi', 'Waiter'),
    ('K002', 'Agus', 'Waiter'),
    ('K003', 'Sinta', 'Cashier'),
    ('K004', 'Budi', 'Manajer'),
    ('K005', 'Bryan', 'Chef'),
    ('K006', 'Dian', 'Operational');

-- Tabel pelanggan
CREATE TABLE IF NOT EXISTS pelanggan (
    pelanggan_id VARCHAR(5) PRIMARY KEY,
    cus_name VARCHAR(50) NOT NULL,
    contact_info VARCHAR(15) NOT NULL
);

INSERT INTO pelanggan (pelanggan_id, cus_name, contact_info) VALUES
    ('P001', 'Dini', '0823416777'),
    ('P002', 'Anita', '0823452267'),
    ('P003', 'Daffa', '0890867736'),
    ('P004', 'Tiara', '083342156'),
    ('P005', 'Torik', '0876544325'),
    ('P006', 'Aziz', '087665489'),
    ('P007', 'Ayu', '087655394'),
    ('P008', 'Dedi', '0823416657');

-- Tabel supplier
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id VARCHAR(5) PRIMARY KEY,
    supplier_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL
);

INSERT INTO supplier (supplier_id, supplier_name, address) VALUES
    ('S001', 'Indofood', 'Jakarta'),
    ('S002', 'Ayla Farm', 'Bandung'),
    ('S003', 'FoodFresh', 'Tangerang');

-- Tabel bahan_baku
CREATE TABLE IF NOT EXISTS bahan_baku (
    bahan_id VARCHAR(5) PRIMARY KEY,
    nama_bahan VARCHAR(50) NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0),
    satuan VARCHAR(20) NOT NULL,
    harga_bahan DECIMAL(15,2) NOT NULL,
    supplier_id VARCHAR(5),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);

INSERT INTO bahan_baku (bahan_id, nama_bahan, stock, satuan, harga_bahan, supplier_id) VALUES
    ('BB1', 'Ayam Potong', 50, 'Kg', 500000.00, 'S001'),
    ('BB2', 'Sayuran', 30, 'Kg', 200000.00, 'S002'),
    ('BB3', 'Ikan Lele', 20, 'Kg', 350000.00, 'S003'),
    ('BB4', 'Bawang', 50, 'Kg', 250000.00, 'S001'),
    ('BB5', 'Bumbu', 100, 'Bungkus', 600000.00, 'S001');

-- Tabel menu
CREATE TABLE IF NOT EXISTS menu (
    menu_id VARCHAR(5) PRIMARY KEY,
    nama_menu VARCHAR(50) NOT NULL,
    harga DECIMAL(15,2) NOT NULL CHECK (harga >= 0)
);

INSERT INTO menu (menu_id, nama_menu, harga) VALUES
    ('MN1', 'Ayam Bakar', 20000.00),
    ('MN2', 'Nasi Goreng', 15000.00),
    ('MN3', 'Oseng Kangkung', 10000.00),
    ('MN4', 'Tumis Labu', 12000.00),
    ('MN5', 'Es Krim', 10000.00),
    ('MN6', 'Es Jeruk', 6000.00),
    ('MN7', 'Es Teh Manis', 5000.00);

-- Tabel transaksi
CREATE TABLE IF NOT EXISTS transaksi (
    transaksi_id VARCHAR(5) PRIMARY KEY,
    tanggal_pembelian DATE NOT NULL,
    pelanggan_id VARCHAR(5) NOT NULL,
    karyawan_id VARCHAR(5) NOT NULL,
    total_transaksi DECIMAL(15,2) NOT NULL CHECK (total_transaksi >= 0),
    FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(pelanggan_id),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

INSERT INTO transaksi (transaksi_id, tanggal_pembelian, pelanggan_id, karyawan_id, total_transaksi) VALUES
    ('T001', '2024-12-01', 'P001', 'K003', 170000.00),
    ('T002', '2024-12-03', 'P002', 'K003', 250000.00),
    ('T003', '2024-12-05', 'P003', 'K003', 150000.00),
    ('T004', '2024-12-04', 'P004', 'K003', 200000.00),
    ('T005', '2024-12-06', 'P005', 'K003', 280000.00),
    ('T006', '2024-12-07', 'P006', 'K003', 500000.00);

-- Tabel detail_transaksi
CREATE TABLE IF NOT EXISTS detail_transaksi (
    detail_id INT PRIMARY KEY AUTO_INCREMENT,
    transaksi_id VARCHAR(5) NOT NULL,
    menu_id VARCHAR(5) NOT NULL,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    harga DECIMAL(15,2) NOT NULL CHECK (harga >= 0),
    FOREIGN KEY (transaksi_id) REFERENCES transaksi(transaksi_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, harga) VALUES
    ('T001', 'MN1', 2, 20000.00),
    ('T001', 'MN6', 2, 6000.00),
    ('T002', 'MN2', 2, 15000.00),
    ('T002', 'MN6', 3, 6000.00),
    ('T003', 'MN3', 1, 10000.00),
    ('T003', 'MN7', 2, 5000.00),
    ('T004', 'MN4', 2, 12000.00),
    ('T004', 'MN7', 1, 5000.00),
    ('T005', 'MN1', 3, 20000.00),
    ('T005', 'MN5', 1, 10000.00),
    ('T006', 'MN2', 4, 15000.00),
    ('T006', 'MN6', 2, 6000.00);

-- Tabel komposisi_menu
CREATE TABLE IF NOT EXISTS komposisi_menu (
    menu_id VARCHAR(5) NOT NULL,
    bahan_id VARCHAR(5) NOT NULL,
    jumlah_bahan INT NOT NULL CHECK (jumlah_bahan > 0),
    PRIMARY KEY (menu_id, bahan_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    FOREIGN KEY (bahan_id) REFERENCES bahan_baku(bahan_id)
);

INSERT INTO komposisi_menu (menu_id, bahan_id, jumlah_bahan) VALUES
    ('MN1', 'BB1', 1),
    ('MN1', 'BB5', 1),
    ('MN2', 'BB2', 1),
    ('MN2', 'BB5', 1),
    ('MN3', 'BB2', 1),
    ('MN3', 'BB5', 1),
    ('MN4', 'BB2', 1),
    ('MN4', 'BB5', 1),
    ('MN5', 'BB5', 1),
    ('MN6', 'BB5', 1),
    ('MN7', 'BB4', 1);

-- Tabel jadwal_kerja
CREATE TABLE IF NOT EXISTS jadwal_kerja (
    jadwal_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(5) NOT NULL,
    tanggal DATE NOT NULL,
    shift VARCHAR(10) NOT NULL,
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

INSERT INTO jadwal_kerja (karyawan_id, tanggal, shift) VALUES
    ('K001', '2024-12-01', 'Pagi'),
    ('K002', '2024-12-01', 'Siang'),
    ('K003', '2024-12-01', 'Malam'),
    ('K001', '2024-12-02', 'Siang'),
    ('K002', '2024-12-02', 'Pagi'),
    ('K003', '2024-12-02', 'Malam');

-- Tabel absensi
CREATE TABLE IF NOT EXISTS absensi (
    absensi_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(5) NOT NULL,
    tanggal DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

INSERT INTO absensi (karyawan_id, tanggal, status) VALUES
    ('K001', '2024-12-01', 'Hadir'),
    ('K002', '2024-12-01', 'Hadir'),
    ('K003', '2024-12-01', 'Hadir'),
    ('K001', '2024-12-02', 'Sakit'),
    ('K002', '2024-12-02', 'Hadir'),
    ('K003', '2024-12-02', 'Hadir');

-- Tabel penggajian
CREATE TABLE IF NOT EXISTS penggajian (
    penggajian_id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id VARCHAR(5) NOT NULL,
    bulan INT NOT NULL CHECK (bulan BETWEEN 1 AND 12),
    tahun INT NOT NULL,
    jumlah_gaji DECIMAL(15,2) NOT NULL CHECK (jumlah_gaji >= 0),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

INSERT INTO penggajian (karyawan_id, bulan, tahun, jumlah_gaji) VALUES
    ('K001', 12, 2024, 3000000.00),
    ('K002', 12, 2024, 2800000.00),
    ('K003', 12, 2024, 3200000.00);

-- Tabel pemesanan_bahan
CREATE TABLE IF NOT EXISTS pemesanan_bahan (
    pemesanan_id VARCHAR(5) PRIMARY KEY,
    supplier_id VARCHAR(5) NOT NULL,
    tanggal_pemesanan DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);

INSERT INTO pemesanan_bahan (pemesanan_id, supplier_id, tanggal_pemesanan, status) VALUES
    ('PB001', 'S001', '2024-12-05', 'Dipesan'),
    ('PB002', 'S002', '2024-12-05', 'Dikirim');

-- Tabel detail_pemesanan_bahan
CREATE TABLE IF NOT EXISTS detail_pemesanan_bahan (
    detail_pemesanan_id INT PRIMARY KEY AUTO_INCREMENT,
    pemesanan_id VARCHAR(5) NOT NULL,
    bahan_id VARCHAR(5) NOT NULL,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    harga_satuan DECIMAL(15,2) NOT NULL CHECK (harga_satuan >= 0),
    FOREIGN KEY (pemesanan_id) REFERENCES pemesanan_bahan(pemesanan_id),
    FOREIGN KEY (bahan_id) REFERENCES bahan_baku(bahan_id)
);

INSERT INTO detail_pemesanan_bahan (pemesanan_id, bahan_id, jumlah, harga_satuan) VALUES
    ('PB001', 'BB1', 20, 500000.00),
    ('PB001', 'BB4', 30, 250000.00),
    ('PB002', 'BB2', 50, 200000.00);

-- Tabel feedback pelanggan
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    pelanggan_id VARCHAR(5) NOT NULL,
    karyawan_id VARCHAR(5) NOT NULL,
    tanggal DATE NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    komentar TEXT,
    FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(pelanggan_id),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(karyawan_id)
);

INSERT INTO feedback (pelanggan_id, karyawan_id, tanggal, rating, komentar) VALUES
    ('P001', 'K003', '2024-12-02', 5, 'Pelayanan sangat memuaskan.'),
    ('P002', 'K001', '2024-12-03', 4, 'Makanan enak dan tempat nyaman.'),
    ('P003', 'K002', '2024-12-04', 3, NULL);