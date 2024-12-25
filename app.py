# app.py

import streamlit as st
from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd
import locale

from db_config import engine, SessionLocal, Base
from models import (
    Karyawan, Pelanggan, Supplier, BahanBaku,
    Menu, KomposisiMenu, Transaksi, DetailTransaksi,
    Absensi, Penggajian, Feedback, JadwalKerja
)

# Mengatur locale untuk format mata uang (opsional)
try:
    locale.setlocale(locale.LC_ALL, '')
except:
    # Jika environment tidak punya locale ID, bisa diabaikan
    pass

def format_rupiah(number):
    """Fungsi membantu format angka ke rupiah (opsional)."""
    try:
        return f"Rp {locale.format_string('%0.2f', number, grouping=True)}"
    except:
        return f"Rp {number:.2f}"

def get_session():
    """Fungsi pembuat sesi database."""
    return SessionLocal()

def show_home():
    st.subheader("Selamat Datang di Sistem Manajemen Restoran")
    st.write("""
        Aplikasi ini membantu Anda dalam mengelola operasi restoran secara efisien.
        Anda dapat mengelola data karyawan, pelanggan, supplier, bahan baku, menu, transaksi,
        feedback, dan juga fitur absensi sidik jari (mockup).
    """)
    st.image(
        "https://img.freepik.com/free-vector/"
        "woman-wearing-medical-mask-client_52683-41295.jpg",
        use_container_width=True
    )

# -------------------- FUNGSI CRUD KARYAWAN --------------------
def manage_karyawan(session: Session):
    st.subheader("Kelola Data Karyawan")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])

    if action == "Tambah":
        st.subheader("Tambah Data Karyawan")
        with st.form("form_tambah_karyawan", clear_on_submit=True):
            karyawan_id = st.text_input("ID Karyawan")
            employee_name = st.text_input("Nama Karyawan")
            position = st.selectbox("Posisi", ["Waiter", "Cashier", "Chef", "Manager", "Operational"])
            fingerprint_id = st.text_input("ID Sidik Jari (Opsional, mock)")
            submit = st.form_submit_button("Simpan")  # Tombol submit

            if submit:
                if not karyawan_id or not employee_name or not position:
                    st.error("Semua field wajib diisi (kecuali sidik jari opsional).")
                else:
                    existing_karyawan = session.query(Karyawan).filter_by(karyawan_id=karyawan_id).first()
                    if existing_karyawan:
                        st.error("ID Karyawan sudah ada.")
                    else:
                        new_karyawan = Karyawan(
                            karyawan_id=karyawan_id,
                            employee_name=employee_name,
                            position=position,
                            fingerprint_id=fingerprint_id if fingerprint_id else None
                        )
                        session.add(new_karyawan)
                        session.commit()
                        st.success("Data karyawan berhasil ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Karyawan")
        karyawan_list = session.query(Karyawan).all()
        if karyawan_list:
            df = pd.DataFrame(
                [
                    (k.karyawan_id, k.employee_name, k.position, k.fingerprint_id if k.fingerprint_id else "-")
                    for k in karyawan_list
                ],
                columns=["ID Karyawan", "Nama", "Posisi", "Fingerprint ID"]
            )
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_karyawan.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data karyawan.")

    elif action == "Perbarui":
        st.subheader("Perbarui Data Karyawan")
        karyawan_list = session.query(Karyawan).all()
        karyawan_ids = [k.karyawan_id for k in karyawan_list]
        if karyawan_ids:
            selected_karyawan_id = st.selectbox("Pilih ID Karyawan", karyawan_ids)
            selected_karyawan = session.query(Karyawan).filter_by(karyawan_id=selected_karyawan_id).first()
            if selected_karyawan:
                with st.form("form_perbarui_karyawan"):
                    employee_name = st.text_input("Nama Karyawan", value=selected_karyawan.employee_name)
                    position_options = ["Waiter", "Cashier", "Chef", "Manager", "Operational"]
                    pos_idx = position_options.index(selected_karyawan.position) if selected_karyawan.position in position_options else 0
                    position = st.selectbox("Posisi", position_options, index=pos_idx)
                    fingerprint_val = selected_karyawan.fingerprint_id if selected_karyawan.fingerprint_id else ""
                    fingerprint_id = st.text_input("ID Sidik Jari (Opsional)", value=fingerprint_val)
                    submit = st.form_submit_button("Perbarui")  # Tombol submit

                    if submit:
                        if not employee_name or not position:
                            st.error("Nama dan Posisi wajib diisi.")
                        else:
                            selected_karyawan.employee_name = employee_name
                            selected_karyawan.position = position
                            selected_karyawan.fingerprint_id = fingerprint_id if fingerprint_id else None
                            session.commit()
                            st.success("Data karyawan berhasil diperbarui.")
        else:
            st.info("Belum ada data karyawan.")

    elif action == "Hapus":
        st.subheader("Hapus Data Karyawan")
        karyawan_list = session.query(Karyawan).all()
        karyawan_ids = [k.karyawan_id for k in karyawan_list]
        if karyawan_ids:
            selected_karyawan_id = st.selectbox("Pilih ID Karyawan", karyawan_ids)
            if st.button("Hapus"):
                selected_karyawan = session.query(Karyawan).filter_by(karyawan_id=selected_karyawan_id).first()
                if selected_karyawan:
                    session.delete(selected_karyawan)
                    session.commit()
                    st.success("Data karyawan berhasil dihapus.")
        else:
            st.info("Belum ada data karyawan.")

# -------------------- FUNGSI CRUD PELANGGAN --------------------
def manage_pelanggan(session: Session):
    st.subheader("Kelola Data Pelanggan")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])

    if action == "Tambah":
        st.subheader("Tambah Data Pelanggan")
        with st.form("form_tambah_pelanggan", clear_on_submit=True):
            pelanggan_id = st.text_input("ID Pelanggan")
            cus_name = st.text_input("Nama Pelanggan")
            contact_info = st.text_input("Kontak")
            submit = st.form_submit_button("Simpan")  # Tombol submit

            if submit:
                if not pelanggan_id or not cus_name or not contact_info:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_pelanggan = session.query(Pelanggan).filter_by(pelanggan_id=pelanggan_id).first()
                    if existing_pelanggan:
                        st.error("ID Pelanggan sudah ada.")
                    else:
                        new_pelanggan = Pelanggan(
                            pelanggan_id=pelanggan_id,
                            cus_name=cus_name,
                            contact_info=contact_info
                        )
                        session.add(new_pelanggan)
                        session.commit()
                        st.success("Data pelanggan berhasil ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Pelanggan")
        pelanggan_list = session.query(Pelanggan).all()
        if pelanggan_list:
            df = pd.DataFrame(
                [(p.pelanggan_id, p.cus_name, p.contact_info) for p in pelanggan_list],
                columns=["ID Pelanggan", "Nama", "Kontak"]
            )
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_pelanggan.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data pelanggan.")

    elif action == "Perbarui":
        st.subheader("Perbarui Data Pelanggan")
        pelanggan_list = session.query(Pelanggan).all()
        pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
        if pelanggan_ids:
            selected_pelanggan_id = st.selectbox("Pilih ID Pelanggan", pelanggan_ids)
            selected_pelanggan = session.query(Pelanggan).filter_by(pelanggan_id=selected_pelanggan_id).first()
            if selected_pelanggan:
                with st.form("form_perbarui_pelanggan"):
                    cus_name = st.text_input("Nama Pelanggan", value=selected_pelanggan.cus_name)
                    contact_info = st.text_input("Kontak", value=selected_pelanggan.contact_info)
                    submit = st.form_submit_button("Perbarui")  # Tombol submit

                    if submit:
                        if not cus_name or not contact_info:
                            st.error("Semua field wajib diisi.")
                        else:
                            selected_pelanggan.cus_name = cus_name
                            selected_pelanggan.contact_info = contact_info
                            session.commit()
                            st.success("Data pelanggan berhasil diperbarui.")
        else:
            st.info("Belum ada data pelanggan.")

    elif action == "Hapus":
        st.subheader("Hapus Data Pelanggan")
        pelanggan_list = session.query(Pelanggan).all()
        pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
        if pelanggan_ids:
            selected_pelanggan_id = st.selectbox("Pilih ID Pelanggan", pelanggan_ids)
            if st.button("Hapus"):
                selected_pelanggan = session.query(Pelanggan).filter_by(pelanggan_id=selected_pelanggan_id).first()
                if selected_pelanggan:
                    session.delete(selected_pelanggan)
                    session.commit()
                    st.success("Data pelanggan berhasil dihapus.")
        else:
            st.info("Belum ada data pelanggan.")

# -------------------- FUNGSI CRUD SUPPLIER --------------------
def manage_supplier(session: Session):
    st.subheader("Kelola Data Supplier")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])

    if action == "Tambah":
        st.subheader("Tambah Data Supplier")
        with st.form("form_tambah_supplier", clear_on_submit=True):
            supplier_id = st.text_input("ID Supplier")
            supplier_name = st.text_input("Nama Supplier")
            address = st.text_input("Alamat")
            submit = st.form_submit_button("Simpan")  # Tombol submit

            if submit:
                if not supplier_id or not supplier_name or not address:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_supplier = session.query(Supplier).filter_by(supplier_id=supplier_id).first()
                    if existing_supplier:
                        st.error("ID Supplier sudah ada.")
                    else:
                        new_supplier = Supplier(
                            supplier_id=supplier_id,
                            supplier_name=supplier_name,
                            address=address
                        )
                        session.add(new_supplier)
                        session.commit()
                        st.success("Data supplier berhasil ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Supplier")
        supplier_list = session.query(Supplier).all()
        if supplier_list:
            df = pd.DataFrame(
                [(s.supplier_id, s.supplier_name, s.address) for s in supplier_list],
                columns=["ID Supplier", "Nama Supplier", "Alamat"]
            )
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_supplier.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data supplier.")

    elif action == "Perbarui":
        st.subheader("Perbarui Data Supplier")
        supplier_list = session.query(Supplier).all()
        supplier_ids = [s.supplier_id for s in supplier_list]
        if supplier_ids:
            selected_supplier_id = st.selectbox("Pilih ID Supplier", supplier_ids)
            selected_supplier = session.query(Supplier).filter_by(supplier_id=selected_supplier_id).first()
            if selected_supplier:
                with st.form("form_perbarui_supplier"):
                    supplier_name = st.text_input("Nama Supplier", value=selected_supplier.supplier_name)
                    address = st.text_input("Alamat", value=selected_supplier.address)
                    submit = st.form_submit_button("Perbarui")  # Tombol submit

                    if submit:
                        if not supplier_name or not address:
                            st.error("Semua field wajib diisi.")
                        else:
                            selected_supplier.supplier_name = supplier_name
                            selected_supplier.address = address
                            session.commit()
                            st.success("Data supplier berhasil diperbarui.")
        else:
            st.info("Belum ada data supplier.")

    elif action == "Hapus":
        st.subheader("Hapus Data Supplier")
        supplier_list = session.query(Supplier).all()
        supplier_ids = [s.supplier_id for s in supplier_list]
        if supplier_ids:
            selected_supplier_id = st.selectbox("Pilih ID Supplier", supplier_ids)
            if st.button("Hapus"):
                selected_supplier = session.query(Supplier).filter_by(supplier_id=selected_supplier_id).first()
                if selected_supplier:
                    session.delete(selected_supplier)
                    session.commit()
                    st.success("Data supplier berhasil dihapus.")
        else:
            st.info("Belum ada data supplier.")

# -------------------- FUNGSI CRUD BAHAN BAKU --------------------
def manage_bahan_baku(session: Session):
    st.subheader("Kelola Data Bahan Baku")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])

    if action == "Tambah":
        st.subheader("Tambah Data Bahan Baku")
        with st.form("form_tambah_bahan_baku", clear_on_submit=True):
            bahan_id = st.text_input("ID Bahan Baku")
            nama_bahan = st.text_input("Nama Bahan")
            stock = st.number_input("Stok", min_value=0, value=0)
            satuan = st.text_input("Satuan")
            harga_bahan = st.number_input("Harga Bahan", min_value=0.0, value=0.0)

            supplier_list = session.query(Supplier).all()
            supplier_ids = [s.supplier_id for s in supplier_list]
            if supplier_ids:
                supplier_id = st.selectbox("Supplier ID", supplier_ids)
            else:
                st.warning("Belum ada supplier. Tambahkan supplier terlebih dahulu.")
                supplier_id = None

            submit = st.form_submit_button("Simpan")  # Tombol submit
            if submit:
                if not bahan_id or not nama_bahan or not satuan or not supplier_id:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_bahan = session.query(BahanBaku).filter_by(bahan_id=bahan_id).first()
                    if existing_bahan:
                        st.error("ID Bahan Baku sudah ada.")
                    else:
                        new_bahan = BahanBaku(
                            bahan_id=bahan_id,
                            nama_bahan=nama_bahan,
                            stock=stock,
                            satuan=satuan,
                            harga_bahan=harga_bahan,
                            supplier_id=supplier_id
                        )
                        session.add(new_bahan)
                        session.commit()
                        st.success("Data bahan baku berhasil ditambahkan.")
        if not session.query(Supplier).all():
            st.warning("Belum ada supplier. Tambahkan supplier terlebih dahulu.")

    elif action == "Lihat":
        st.subheader("Daftar Bahan Baku")
        bahan_baku_list = session.query(BahanBaku).all()
        if bahan_baku_list:
            df = pd.DataFrame(
                [
                    (
                        b.bahan_id,
                        b.nama_bahan,
                        b.stock,
                        b.satuan,
                        float(b.harga_bahan),
                        b.supplier_id
                    )
                    for b in bahan_baku_list
                ],
                columns=["ID Bahan Baku", "Nama Bahan", "Stok", "Satuan", "Harga Bahan", "Supplier ID"]
            )
            df["Harga Bahan"] = df["Harga Bahan"].apply(format_rupiah)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_bahan_baku.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data bahan baku.")

    elif action == "Perbarui":
        st.subheader("Perbarui Data Bahan Baku")
        bahan_baku_list = session.query(BahanBaku).all()
        bahan_ids = [b.bahan_id for b in bahan_baku_list]
        if bahan_ids:
            selected_bahan_id = st.selectbox("Pilih ID Bahan Baku", bahan_ids)
            selected_bahan = session.query(BahanBaku).filter_by(bahan_id=selected_bahan_id).first()
            if selected_bahan:
                with st.form("form_perbarui_bahan_baku"):
                    nama_bahan = st.text_input("Nama Bahan", value=selected_bahan.nama_bahan)
                    stock = st.number_input("Stok", min_value=0, value=selected_bahan.stock)
                    satuan = st.text_input("Satuan", value=selected_bahan.satuan)
                    harga_bahan = st.number_input("Harga Bahan", min_value=0.0, value=float(selected_bahan.harga_bahan))

                    supplier_list = session.query(Supplier).all()
                    supplier_ids = [s.supplier_id for s in supplier_list]
                    if selected_bahan.supplier_id in supplier_ids:
                        idx = supplier_ids.index(selected_bahan.supplier_id)
                    else:
                        idx = 0
                    if supplier_ids:
                        supplier_id = st.selectbox("Supplier ID", supplier_ids, index=idx)
                    else:
                        st.warning("Belum ada supplier. Tambahkan supplier terlebih dahulu.")
                        supplier_id = None

                    submit = st.form_submit_button("Perbarui")  # Tombol submit
                    if submit:
                        if not nama_bahan or not satuan or not supplier_id:
                            st.error("Semua field wajib diisi.")
                        else:
                            selected_bahan.nama_bahan = nama_bahan
                            selected_bahan.stock = stock
                            selected_bahan.satuan = satuan
                            selected_bahan.harga_bahan = harga_bahan
                            selected_bahan.supplier_id = supplier_id
                            session.commit()
                            st.success("Data bahan baku berhasil diperbarui.")
        else:
            st.info("Belum ada data bahan baku.")

    elif action == "Hapus":
        st.subheader("Hapus Data Bahan Baku")
        bahan_baku_list = session.query(BahanBaku).all()
        bahan_ids = [b.bahan_id for b in bahan_baku_list]
        if bahan_ids:
            selected_bahan_id = st.selectbox("Pilih ID Bahan Baku", bahan_ids)
            if st.button("Hapus"):
                selected_bahan = session.query(BahanBaku).filter_by(bahan_id=selected_bahan_id).first()
                if selected_bahan:
                    session.delete(selected_bahan)
                    session.commit()
                    st.success("Data bahan baku berhasil dihapus.")
        else:
            st.info("Belum ada data bahan baku.")

# -------------------- FUNGSI CRUD MENU --------------------
def manage_menu(session: Session):
    st.subheader("Kelola Data Menu")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus", "Kelola Komposisi"])

    if action == "Tambah":
        st.subheader("Tambah Data Menu")
        with st.form("form_tambah_menu", clear_on_submit=True):
            menu_id = st.text_input("ID Menu")
            nama_menu = st.text_input("Nama Menu")
            harga = st.number_input("Harga", min_value=0.0, value=0.0)
            submit = st.form_submit_button("Simpan")  # Tombol submit

            if submit:
                if not menu_id or not nama_menu:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_menu = session.query(Menu).filter_by(menu_id=menu_id).first()
                    if existing_menu:
                        st.error("ID Menu sudah ada.")
                    else:
                        new_menu = Menu(
                            menu_id=menu_id,
                            nama_menu=nama_menu,
                            harga=harga
                        )
                        session.add(new_menu)
                        session.commit()
                        st.success("Data menu berhasil ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Menu")
        menu_list = session.query(Menu).all()
        if menu_list:
            df = pd.DataFrame(
                [(m.menu_id, m.nama_menu, float(m.harga)) for m in menu_list],
                columns=["ID Menu", "Nama Menu", "Harga"]
            )
            df["Harga"] = df["Harga"].apply(format_rupiah)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_menu.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data menu.")

    elif action == "Perbarui":
        st.subheader("Perbarui Data Menu")
        menu_list = session.query(Menu).all()
        menu_ids = [m.menu_id for m in menu_list]
        if menu_ids:
            selected_menu_id = st.selectbox("Pilih ID Menu", menu_ids)
            selected_menu = session.query(Menu).filter_by(menu_id=selected_menu_id).first()
            if selected_menu:
                with st.form("form_perbarui_menu"):
                    nama_menu = st.text_input("Nama Menu", value=selected_menu.nama_menu)
                    harga = st.number_input("Harga", min_value=0.0, value=float(selected_menu.harga))
                    submit = st.form_submit_button("Perbarui")  # Tombol submit

                    if submit:
                        if not nama_menu:
                            st.error("Nama menu wajib diisi.")
                        else:
                            selected_menu.nama_menu = nama_menu
                            selected_menu.harga = harga
                            session.commit()
                            st.success("Data menu berhasil diperbarui.")
        else:
            st.info("Belum ada data menu.")

    elif action == "Hapus":
        st.subheader("Hapus Data Menu")
        menu_list = session.query(Menu).all()
        menu_ids = [m.menu_id for m in menu_list]
        if menu_ids:
            selected_menu_id = st.selectbox("Pilih ID Menu", menu_ids)
            if st.button("Hapus"):
                selected_menu = session.query(Menu).filter_by(menu_id=selected_menu_id).first()
                if selected_menu:
                    session.delete(selected_menu)
                    session.commit()
                    st.success("Data menu berhasil dihapus.")
        else:
            st.info("Belum ada data menu.")

    elif action == "Kelola Komposisi":
        st.subheader("Kelola Komposisi Menu")
        menu_list = session.query(Menu).all()
        menu_ids = [m.menu_id for m in menu_list]
        if menu_ids:
            selected_menu_id = st.selectbox("Pilih ID Menu", menu_ids)
            selected_menu = session.query(Menu).filter_by(menu_id=selected_menu_id).first()
            if selected_menu:
                st.write(f"Nama Menu: {selected_menu.nama_menu}")

                # Tampilkan komposisi saat ini
                komposisi_list = session.query(KomposisiMenu).filter_by(menu_id=selected_menu_id).all()
                if komposisi_list:
                    df_komposisi = pd.DataFrame(
                        [
                            (k.bahan_id, k.bahan_baku.nama_bahan, k.jumlah_bahan)
                            for k in komposisi_list
                        ],
                        columns=["ID Bahan", "Nama Bahan", "Jumlah"]
                    )
                    st.dataframe(df_komposisi)
                else:
                    st.info("Belum ada komposisi untuk menu ini.")

                st.write("---")
                st.write("### Tambah Bahan Baku ke Komposisi")
                bahan_baku_list = session.query(BahanBaku).all()
                bahan_ids = [b.bahan_id for b in bahan_baku_list]
                if bahan_ids:
                    selected_bahan_id = st.selectbox("Pilih ID Bahan Baku", bahan_ids)
                    jumlah_bahan = st.number_input("Jumlah Bahan", min_value=1, value=1)
                    tambah_item = st.button("Tambah ke Komposisi")

                    if tambah_item:
                        existing_komposisi = session.query(KomposisiMenu).filter_by(
                            menu_id=selected_menu_id,
                            bahan_id=selected_bahan_id
                        ).first()
                        if existing_komposisi:
                            st.error("Bahan baku sudah ada dalam komposisi.")
                        else:
                            new_komposisi = KomposisiMenu(
                                menu_id=selected_menu_id,
                                bahan_id=selected_bahan_id,
                                jumlah_bahan=jumlah_bahan
                            )
                            session.add(new_komposisi)
                            session.commit()
                            st.success("Bahan baku berhasil ditambahkan ke komposisi.")
                else:
                    st.info("Belum ada data bahan baku.")
        else:
            st.info("Belum ada data menu.")

# -------------------- FUNGSI CRUD TRANSAKSI --------------------
def manage_transaksi(session: Session):
    st.subheader("Kelola Data Transaksi")
    action = st.selectbox("Aksi", ["Tambah", "Lihat"])

    if action == "Tambah":
        st.subheader("Tambah Data Transaksi")
        with st.form("form_tambah_transaksi", clear_on_submit=True):
            transaksi_id = st.text_input("ID Transaksi")
            tanggal_pembelian = st.date_input("Tanggal Pembelian", datetime.today())

            pelanggan_list = session.query(Pelanggan).all()
            pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
            karyawan_list = session.query(Karyawan).all()
            karyawan_ids = [k.karyawan_id for k in karyawan_list]

            if not pelanggan_ids:
                st.warning("Belum ada pelanggan.")
            if not karyawan_ids:
                st.warning("Belum ada karyawan.")

            pelanggan_id = st.selectbox("Pelanggan ID", pelanggan_ids) if pelanggan_ids else None
            karyawan_id = st.selectbox("Karyawan ID", karyawan_ids) if karyawan_ids else None

            submit = st.form_submit_button("Lanjutkan")  # Tombol submit

        if submit and pelanggan_id and karyawan_id:
            existing_transaksi = session.query(Transaksi).filter_by(transaksi_id=transaksi_id).first()
            if existing_transaksi:
                st.error("ID Transaksi sudah ada.")
                return

            new_transaksi = Transaksi(
                transaksi_id=transaksi_id,
                tanggal_pembelian=tanggal_pembelian,
                pelanggan_id=pelanggan_id,
                karyawan_id=karyawan_id,
                total_transaksi=0.0  # akan di-update setelah detail ditambahkan
            )
            session.add(new_transaksi)
            session.commit()
            st.success("Transaksi berhasil dibuat. Silakan tambahkan detail transaksi.")

            # Menambahkan detail transaksi via session state
            if 'detail_transaksi' not in st.session_state:
                st.session_state.detail_transaksi = []

            with st.expander("Tambah Detail Transaksi"):
                menu_list = session.query(Menu).all()
                menu_ids = [m.menu_id for m in menu_list]

                if not menu_ids:
                    st.warning("Tidak ada menu tersedia.")
                else:
                    menu_id = st.selectbox("Pilih Menu", menu_ids)
                    jumlah = st.number_input("Jumlah", min_value=1, value=1)
                    tambah_item = st.button("Tambah Item")

                    if tambah_item:
                        selected_menu = session.query(Menu).filter_by(menu_id=menu_id).first()
                        harga = float(selected_menu.harga) * jumlah

                        # Validasi stok bahan baku
                        komposisi_list = session.query(KomposisiMenu).filter_by(menu_id=menu_id).all()
                        insufficient_stock = False
                        for komposisi in komposisi_list:
                            bahan = session.query(BahanBaku).filter_by(bahan_id=komposisi.bahan_id).with_for_update().first()
                            if bahan:
                                total_kebutuhan = komposisi.jumlah_bahan * jumlah
                                if bahan.stock < total_kebutuhan:
                                    st.error(f"Stok bahan {bahan.nama_bahan} tidak mencukupi.")
                                    insufficient_stock = True
                                    break

                        if insufficient_stock:
                            session.rollback()
                            st.warning("Penambahan item dibatalkan karena stok tidak cukup.")
                        else:
                            # Kurangi stok
                            for komposisi in komposisi_list:
                                bahan = session.query(BahanBaku).filter_by(bahan_id=komposisi.bahan_id).first()
                                if bahan:
                                    total_kebutuhan = komposisi.jumlah_bahan * jumlah
                                    bahan.stock -= total_kebutuhan
                                    session.commit()
                                    st.info(f"Stok {bahan.nama_bahan} berkurang {total_kebutuhan} {bahan.satuan}.")

                            # Tambah detail transaksi
                            new_detail = DetailTransaksi(
                                transaksi_id=transaksi_id,
                                menu_id=menu_id,
                                jumlah=jumlah,
                                harga=harga
                            )
                            session.add(new_detail)
                            st.session_state.detail_transaksi.append({
                                "Menu": selected_menu.nama_menu,
                                "Jumlah": jumlah,
                                "Harga": harga
                            })
                            session.commit()
                            st.success(f"Item {selected_menu.nama_menu} ({jumlah}) ditambahkan.")

        # Tampilkan detail transaksi yang telah ditambahkan
        if st.session_state.get('detail_transaksi'):
            df_detail = pd.DataFrame(st.session_state.detail_transaksi)
            st.table(df_detail)

        # Tombol untuk menyelesaikan transaksi
        if st.button("Selesaikan Transaksi"):
            if 'detail_transaksi' in st.session_state and st.session_state.detail_transaksi:
                total_transaksi = sum(item["Harga"] for item in st.session_state.detail_transaksi)
                current_transaksi = session.query(Transaksi).filter_by(transaksi_id=transaksi_id).first()
                current_transaksi.total_transaksi = total_transaksi
                session.commit()

                st.success(f"Transaksi selesai dengan total: {format_rupiah(total_transaksi)}")

                # Reset session state detail
                st.session_state.detail_transaksi = []

                # Bagian feedback
                st.subheader("Beri Rating dan Feedback")
                with st.form("form_feedback"):
                    rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=5)
                    komentar = st.text_area("Komentar (Opsional)", height=100)
                    submit_feedback = st.form_submit_button("Simpan Feedback")
                    if submit_feedback:
                        new_feedback = Feedback(
                            pelanggan_id=pelanggan_id,
                            karyawan_id=karyawan_id,
                            tanggal=datetime.today(),
                            rating=rating,
                            komentar=komentar if komentar.strip() != '' else None
                        )
                        session.add(new_feedback)
                        session.commit()
                        st.success("Feedback berhasil disimpan. Terima kasih!")
            else:
                st.warning("Tidak ada detail transaksi yang ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Transaksi")
        transaksi_list = session.query(Transaksi).all()
        if transaksi_list:
            df = pd.DataFrame(
                [
                    (
                        t.transaksi_id,
                        t.tanggal_pembelian.strftime('%Y-%m-%d'),
                        t.pelanggan_id,
                        t.karyawan_id,
                        float(t.total_transaksi)
                    )
                    for t in transaksi_list
                ],
                columns=["ID Transaksi", "Tanggal Pembelian", "ID Pelanggan", "ID Karyawan", "Total Transaksi"]
            )
            df["Total Transaksi"] = df["Total Transaksi"].apply(format_rupiah)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_transaksi.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data transaksi.")

# -------------------- FUNGSI CRUD FEEDBACK --------------------
def manage_feedback(session: Session):
    st.subheader("Kelola Feedback")
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])

    if action == "Tambah":
        st.subheader("Tambah Feedback")
        with st.form("form_tambah_feedback", clear_on_submit=True):
            tanggal = st.date_input("Tanggal Feedback", datetime.today())
            pelanggan_list = session.query(Pelanggan).all()
            pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
            karyawan_list = session.query(Karyawan).all()
            karyawan_ids = [k.karyawan_id for k in karyawan_list]

            pelanggan_id = st.selectbox("Pelanggan ID", pelanggan_ids) if pelanggan_ids else None
            karyawan_id = st.selectbox("Karyawan ID", karyawan_ids) if karyawan_ids else None
            rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=5)
            komentar = st.text_area("Komentar (Opsional)", height=100)

            submit = st.form_submit_button("Simpan Feedback")  # Tombol submit
            if submit:
                if not pelanggan_id or not karyawan_id:
                    st.error("Pelanggan dan Karyawan wajib dipilih.")
                else:
                    new_feedback = Feedback(
                        pelanggan_id=pelanggan_id,
                        karyawan_id=karyawan_id,
                        tanggal=tanggal,
                        rating=rating,
                        komentar=komentar if komentar.strip() != '' else None
                    )
                    session.add(new_feedback)
                    session.commit()
                    st.success("Feedback berhasil ditambahkan.")

    elif action == "Lihat":
        st.subheader("Daftar Feedback")
        feedback_list = session.query(Feedback).all()
        if feedback_list:
            df = pd.DataFrame(
                [
                    (
                        f.feedback_id,
                        f.pelanggan_id,
                        f.karyawan_id,
                        f.tanggal.strftime('%Y-%m-%d'),
                        f.rating,
                        f.komentar
                    )
                    for f in feedback_list
                ],
                columns=["ID Feedback", "ID Pelanggan", "ID Karyawan", "Tanggal", "Rating", "Komentar"]
            )
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='daftar_feedback.csv',
                mime='text/csv',
            )
        else:
            st.info("Belum ada data feedback.")

    elif action == "Perbarui":
        st.subheader("Perbarui Feedback")
        feedback_list = session.query(Feedback).all()
        feedback_ids = [f.feedback_id for f in feedback_list]
        if feedback_ids:
            selected_feedback_id = st.selectbox("Pilih ID Feedback", feedback_ids)
            selected_feedback = session.query(Feedback).filter_by(feedback_id=selected_feedback_id).first()
            if selected_feedback:
                with st.form("form_perbarui_feedback"):
                    tanggal = st.date_input("Tanggal Feedback", selected_feedback.tanggal)
                    pelanggan_list = session.query(Pelanggan).all()
                    pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
                    karyawan_list = session.query(Karyawan).all()
                    karyawan_ids = [k.karyawan_id for k in karyawan_list]

                    pelanggan_id = st.selectbox("Pelanggan ID", pelanggan_ids, 
                                                index=pelanggan_ids.index(selected_feedback.pelanggan_id)) if pelanggan_ids else None
                    karyawan_id = st.selectbox("Karyawan ID", karyawan_ids, 
                                               index=karyawan_ids.index(selected_feedback.karyawan_id)) if karyawan_ids else None
                    rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=selected_feedback.rating)
                    komentar_val = selected_feedback.komentar if selected_feedback.komentar else ""
                    komentar = st.text_area("Komentar (Opsional)", value=komentar_val, height=100)

                    submit = st.form_submit_button("Perbarui Feedback")  # Tombol submit
                    if submit:
                        if not pelanggan_id or not karyawan_id:
                            st.error("Pelanggan dan Karyawan wajib dipilih.")
                        else:
                            selected_feedback.pelanggan_id = pelanggan_id
                            selected_feedback.karyawan_id = karyawan_id
                            selected_feedback.tanggal = tanggal
                            selected_feedback.rating = rating
                            selected_feedback.komentar = komentar if komentar.strip() != '' else None
                            session.commit()
                            st.success("Feedback berhasil diperbarui.")
        else:
            st.info("Belum ada data feedback.")

    elif action == "Hapus":
        st.subheader("Hapus Feedback")
        feedback_list = session.query(Feedback).all()
        feedback_ids = [f.feedback_id for f in feedback_list]
        if feedback_ids:
            selected_feedback_id = st.selectbox("Pilih ID Feedback", feedback_ids)
            if st.button("Hapus Feedback"):
                selected_feedback = session.query(Feedback).filter_by(feedback_id=selected_feedback_id).first()
                if selected_feedback:
                    session.delete(selected_feedback)
                    session.commit()
                    st.success("Feedback berhasil dihapus.")
        else:
            st.info("Belum ada data feedback.")

# -------------------- FUNGSI ABSENSI SIDIK JARI (MOCK) --------------------
def manage_fingerprint_absensi(session: Session):
    st.subheader("Absensi dengan Sidik Jari (Mockup)")
    
    tab1, tab2 = st.tabs(["Pendaftaran Sidik Jari", "Scan Sidik Jari & Absen"])

    # Tab 1: Pendaftaran Sidik Jari
    with tab1:
        st.write("## Daftarkan/Mutakhirkan ID Sidik Jari Karyawan")
        karyawan_list = session.query(Karyawan).all()
        karyawan_ids = [k.karyawan_id for k in karyawan_list]
        if karyawan_ids:
            selected_karyawan_id = st.selectbox("Pilih Karyawan", karyawan_ids)
            karyawan_terpilih = session.query(Karyawan).filter_by(karyawan_id=selected_karyawan_id).first()
            if karyawan_terpilih:
                st.write(f"ID Sidik Jari sekarang: **{karyawan_terpilih.fingerprint_id or '(Belum ada)'}**")
                new_fp = st.text_input("Masukkan ID Sidik Jari Baru (mis. FIDxxx)")
                if st.button("Simpan Sidik Jari"):
                    if not new_fp:
                        st.error("Masukkan ID Sidik Jari.")
                    else:
                        karyawan_terpilih.fingerprint_id = new_fp
                        session.commit()
                        st.success("ID Sidik Jari berhasil diperbarui.")
        else:
            st.info("Belum ada data karyawan. Tambahkan karyawan terlebih dahulu.")

    # Tab 2: Scan Sidik Jari & Absen
    with tab2:
        st.write("## Lakukan Scan Sidik Jari (Mock)")
        fp_input = st.text_input("Masukkan ID Sidik Jari yang terdeteksi sensor (mock)")
        if st.button("Absen"):
            if not fp_input:
                st.error("Tolong isi ID Sidik Jari.")
            else:
                # Cari karyawan dengan fingerprint_id = fp_input
                karyawan_found = session.query(Karyawan).filter_by(fingerprint_id=fp_input).first()
                if karyawan_found:
                    new_absen = Absensi(
                        karyawan_id=karyawan_found.karyawan_id,
                        tanggal=datetime.now().date(),
                        status="Hadir"
                    )
                    session.add(new_absen)
                    session.commit()
                    st.success(f"{karyawan_found.employee_name} berhasil absen (ID: {karyawan_found.karyawan_id}).")
                else:
                    st.error("Sidik jari tidak dikenali!")

        st.write("---")
        st.write("### Riwayat Absensi Terakhir")
        absensi_list = session.query(Absensi).order_by(Absensi.absensi_id.desc()).limit(10).all()
        if absensi_list:
            df = pd.DataFrame(
                [
                    (
                        a.absensi_id,
                        a.karyawan_id,
                        a.karyawan.employee_name,
                        a.tanggal.strftime("%Y-%m-%d"),
                        a.status
                    )
                    for a in absensi_list
                ],
                columns=["Absensi ID", "Karyawan ID", "Nama Karyawan", "Tanggal", "Status"]
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data absensi.")

# -------------------- MAIN APP --------------------
def main():
    st.set_page_config(page_title="Sistem Manajemen Restoran", layout="wide")
    st.title("Sistem Manajemen Restoran")

    menu_options = [
        "Beranda",
        "Karyawan",
        "Pelanggan",
        "Supplier",
        "Bahan Baku",
        "Menu",
        "Transaksi",
        "Feedback",
        "Absensi Sidik Jari"  # Menu Baru
    ]

    selected_menu = st.sidebar.selectbox("Navigasi", menu_options)
    session = get_session()

    # Membuat semua tabel di database (jika belum ada)
    Base.metadata.create_all(bind=engine)

    if selected_menu == "Beranda":
        show_home()
    elif selected_menu == "Karyawan":
        manage_karyawan(session)
    elif selected_menu == "Pelanggan":
        manage_pelanggan(session)
    elif selected_menu == "Supplier":
        manage_supplier(session)
    elif selected_menu == "Bahan Baku":
        manage_bahan_baku(session)
    elif selected_menu == "Menu":
        manage_menu(session)
    elif selected_menu == "Transaksi":
        manage_transaksi(session)
    elif selected_menu == "Feedback":
        manage_feedback(session)
    elif selected_menu == "Absensi Sidik Jari":
        manage_fingerprint_absensi(session)

    session.close()

if __name__ == "__main__":
    main()
