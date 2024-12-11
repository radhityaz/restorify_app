import streamlit as st
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (
    Base, Karyawan, Pelanggan, Supplier, BahanBaku,
    Menu, KomposisiMenu, Transaksi, DetailTransaksi,
    Absensi, Penggajian, Feedback, JadwalKerja
)
from db_config import SessionLocal
import pandas as pd
import locale

# Mengatur locale untuk format mata uang Rupiah
locale.setlocale(locale.LC_ALL, '')

def format_rupiah(number):
    return f"Rp {locale.format_string('%0.2f', number, grouping=True)}"

# Fungsi untuk membuat session database
def get_session():
    session = SessionLocal()
    return session

def main():
    st.set_page_config(page_title="Sistem Manajemen Restoran", layout="wide")
    st.title("Sistem Manajemen Restoran")

    menu_options = [
        "Karyawan",
        "Pelanggan",
        "Supplier",
        "Bahan Baku",
        "Menu",
        "Transaksi",
        "Feedback",
    ]

    selected_menu = st.sidebar.selectbox("Navigasi", menu_options)

    session = get_session()

    if selected_menu == "Karyawan":
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

    session.close()

# Fungsi untuk mengelola data Karyawan
def manage_karyawan(session: Session):
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])
    if action == "Tambah":
        st.subheader("Tambah Data Karyawan")
        with st.form("form_tambah_karyawan", clear_on_submit=True):
            karyawan_id = st.text_input("ID Karyawan")
            employee_name = st.text_input("Nama Karyawan")
            position = st.selectbox("Posisi", ["Waiter", "Cashier", "Chef", "Manager", "Operational"])
            submit = st.form_submit_button("Simpan")
            if submit:
                if not karyawan_id or not employee_name or not position:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_karyawan = session.query(Karyawan).filter(Karyawan.karyawan_id == karyawan_id).first()
                    if existing_karyawan:
                        st.error("ID Karyawan sudah ada.")
                    else:
                        new_karyawan = Karyawan(
                            karyawan_id=karyawan_id,
                            employee_name=employee_name,
                            position=position
                        )
                        session.add(new_karyawan)
                        session.commit()
                        st.success("Data karyawan berhasil ditambahkan.")
    elif action == "Lihat":
        st.subheader("Daftar Karyawan")
        karyawan_list = session.query(Karyawan).all()
        if karyawan_list:
            df = pd.DataFrame(
                [(k.karyawan_id, k.employee_name, k.position) for k in karyawan_list],
                columns=["ID Karyawan", "Nama", "Posisi"]
            )
            st.dataframe(df, use_container_width=True)
            # Export ke CSV
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
            selected_karyawan = session.query(Karyawan).filter(Karyawan.karyawan_id == selected_karyawan_id).first()
            if selected_karyawan:
                with st.form("form_perbarui_karyawan"):
                    employee_name = st.text_input("Nama Karyawan", value=selected_karyawan.employee_name)
                    position_options = ["Waiter", "Cashier", "Chef", "Manager", "Operational"]
                    position = st.selectbox("Posisi", position_options, index=position_options.index(selected_karyawan.position))
                    submit = st.form_submit_button("Perbarui")
                    if submit:
                        if not employee_name or not position:
                            st.error("Semua field wajib diisi.")
                        else:
                            selected_karyawan.employee_name = employee_name
                            selected_karyawan.position = position
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
                selected_karyawan = session.query(Karyawan).filter(Karyawan.karyawan_id == selected_karyawan_id).first()
                session.delete(selected_karyawan)
                session.commit()
                st.success("Data karyawan berhasil dihapus.")
        else:
            st.info("Belum ada data karyawan.")

# Fungsi untuk mengelola data Pelanggan
def manage_pelanggan(session: Session):
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])
    if action == "Tambah":
        st.subheader("Tambah Data Pelanggan")
        with st.form("form_tambah_pelanggan", clear_on_submit=True):
            pelanggan_id = st.text_input("ID Pelanggan")
            cus_name = st.text_input("Nama Pelanggan")
            contact_info = st.text_input("Kontak")
            submit = st.form_submit_button("Simpan")
            if submit:
                if not pelanggan_id or not cus_name or not contact_info:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_pelanggan = session.query(Pelanggan).filter(Pelanggan.pelanggan_id == pelanggan_id).first()
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
            # Export ke CSV
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
            selected_pelanggan = session.query(Pelanggan).filter(Pelanggan.pelanggan_id == selected_pelanggan_id).first()
            if selected_pelanggan:
                with st.form("form_perbarui_pelanggan"):
                    cus_name = st.text_input("Nama Pelanggan", value=selected_pelanggan.cus_name)
                    contact_info = st.text_input("Kontak", value=selected_pelanggan.contact_info)
                    submit = st.form_submit_button("Perbarui")
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
                selected_pelanggan = session.query(Pelanggan).filter(Pelanggan.pelanggan_id == selected_pelanggan_id).first()
                session.delete(selected_pelanggan)
                session.commit()
                st.success("Data pelanggan berhasil dihapus.")
        else:
            st.info("Belum ada data pelanggan.")

# Fungsi untuk mengelola data Supplier
def manage_supplier(session: Session):
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])
    if action == "Tambah":
        st.subheader("Tambah Data Supplier")
        with st.form("form_tambah_supplier", clear_on_submit=True):
            supplier_id = st.text_input("ID Supplier")
            supplier_name = st.text_input("Nama Supplier")
            address = st.text_input("Alamat")
            submit = st.form_submit_button("Simpan")
            if submit:
                if not supplier_id or not supplier_name or not address:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_supplier = session.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
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
            # Export ke CSV
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
            selected_supplier = session.query(Supplier).filter(Supplier.supplier_id == selected_supplier_id).first()
            if selected_supplier:
                with st.form("form_perbarui_supplier"):
                    supplier_name = st.text_input("Nama Supplier", value=selected_supplier.supplier_name)
                    address = st.text_input("Alamat", value=selected_supplier.address)
                    submit = st.form_submit_button("Perbarui")
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
                selected_supplier = session.query(Supplier).filter(Supplier.supplier_id == selected_supplier_id).first()
                session.delete(selected_supplier)
                session.commit()
                st.success("Data supplier berhasil dihapus.")
        else:
            st.info("Belum ada data supplier.")

# Fungsi untuk mengelola data Bahan Baku
def manage_bahan_baku(session: Session):
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
            supplier_id = st.selectbox("Supplier ID", supplier_ids) if supplier_ids else None
            submit = st.form_submit_button("Simpan")
            if submit:
                if not bahan_id or not nama_bahan or not satuan or not supplier_id:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_bahan = session.query(BahanBaku).filter(BahanBaku.bahan_id == bahan_id).first()
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
        if not supplier_list:
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
                        b.harga_bahan,
                        b.supplier_id
                    )
                    for b in bahan_baku_list
                ],
                columns=["ID Bahan Baku", "Nama Bahan", "Stok", "Satuan", "Harga Bahan", "Supplier ID"]
            )
            df["Harga Bahan"] = df["Harga Bahan"].apply(format_rupiah)
            st.dataframe(df, use_container_width=True)
            # Export ke CSV
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
            selected_bahan = session.query(BahanBaku).filter(BahanBaku.bahan_id == selected_bahan_id).first()
            if selected_bahan:
                with st.form("form_perbarui_bahan_baku"):
                    nama_bahan = st.text_input("Nama Bahan", value=selected_bahan.nama_bahan)
                    stock = st.number_input("Stok", min_value=0, value=selected_bahan.stock)
                    satuan = st.text_input("Satuan", value=selected_bahan.satuan)
                    harga_bahan = st.number_input("Harga Bahan", min_value=0.0, value=float(selected_bahan.harga_bahan))
                    supplier_list = session.query(Supplier).all()
                    supplier_ids = [s.supplier_id for s in supplier_list]
                    supplier_id = st.selectbox("Supplier ID", supplier_ids, index=supplier_ids.index(selected_bahan.supplier_id)) if supplier_ids else None
                    submit = st.form_submit_button("Perbarui")
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
            if not supplier_list:
                st.warning("Belum ada supplier. Tambahkan supplier terlebih dahulu.")
        else:
            st.info("Belum ada data bahan baku.")
    elif action == "Hapus":
        st.subheader("Hapus Data Bahan Baku")
        bahan_baku_list = session.query(BahanBaku).all()
        bahan_ids = [b.bahan_id for b in bahan_baku_list]
        if bahan_ids:
            selected_bahan_id = st.selectbox("Pilih ID Bahan Baku", bahan_ids)
            if st.button("Hapus"):
                selected_bahan = session.query(BahanBaku).filter(BahanBaku.bahan_id == selected_bahan_id).first()
                session.delete(selected_bahan)
                session.commit()
                st.success("Data bahan baku berhasil dihapus.")
        else:
            st.info("Belum ada data bahan baku.")


# Fungsi untuk mengelola data Menu
def manage_menu(session: Session):
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus", "Kelola Komposisi"])
    if action == "Tambah":
        st.subheader("Tambah Data Menu")
        with st.form("form_tambah_menu", clear_on_submit=True):
            menu_id = st.text_input("ID Menu")
            nama_menu = st.text_input("Nama Menu")
            harga = st.number_input("Harga", min_value=0.0, value=0.0)
            submit = st.form_submit_button("Simpan")
            if submit:
                if not menu_id or not nama_menu:
                    st.error("Semua field wajib diisi.")
                else:
                    existing_menu = session.query(Menu).filter(Menu.menu_id == menu_id).first()
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
                [(m.menu_id, m.nama_menu, format_rupiah(m.harga)) for m in menu_list],
                columns=["ID Menu", "Nama Menu", "Harga"]
            )
            st.dataframe(df, use_container_width=True)
            # Export ke CSV
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
            selected_menu = session.query(Menu).filter(Menu.menu_id == selected_menu_id).first()
            if selected_menu:
                with st.form("form_perbarui_menu"):
                    nama_menu = st.text_input("Nama Menu", value=selected_menu.nama_menu)
                    harga = st.number_input("Harga", min_value=0.0, value=float(selected_menu.harga))
                    submit = st.form_submit_button("Perbarui")
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
                selected_menu = session.query(Menu).filter(Menu.menu_id == selected_menu_id).first()
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
            selected_menu = session.query(Menu).filter(Menu.menu_id == selected_menu_id).first()
            if selected_menu:
                st.write(f"Nama Menu: {selected_menu.nama_menu}")
                # Tampilkan komposisi saat ini
                komposisi_list = session.query(KomposisiMenu).filter(KomposisiMenu.menu_id == selected_menu_id).all()
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
                st.write("Tambah Bahan Baku ke Komposisi")
                bahan_baku_list = session.query(BahanBaku).all()
                bahan_ids = [b.bahan_id for b in bahan_baku_list]
                if bahan_ids:
                    selected_bahan_id = st.selectbox("Pilih ID Bahan Baku", bahan_ids)
                    jumlah_bahan = st.number_input("Jumlah Bahan", min_value=1, value=1)
                    if st.button("Tambah ke Komposisi"):
                        existing_komposisi = session.query(KomposisiMenu).filter(
                            KomposisiMenu.menu_id == selected_menu_id,
                            KomposisiMenu.bahan_id == selected_bahan_id
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
            
# Fungsi untuk mengelola data Transaksi
def manage_transaksi(session: Session):
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
    
            submit = st.form_submit_button("Lanjutkan")
    
        if submit and pelanggan_id and karyawan_id:
            existing_transaksi = session.query(Transaksi).filter(Transaksi.transaksi_id == transaksi_id).first()
            if existing_transaksi:
                st.error("ID Transaksi sudah ada.")
                return
    
            new_transaksi = Transaksi(
                transaksi_id=transaksi_id,
                tanggal_pembelian=tanggal_pembelian,
                pelanggan_id=pelanggan_id,
                karyawan_id=karyawan_id,
                total_transaksi=0.0  # Akan diupdate setelah detail ditambahkan
            )
            session.add(new_transaksi)
            session.commit()
            st.success("Transaksi berhasil dibuat. Silakan tambahkan detail transaksi.")
    
            # Menambahkan detail transaksi menggunakan session state
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
                        selected_menu = session.query(Menu).filter(Menu.menu_id == menu_id).first()
                        harga = float(selected_menu.harga) * jumlah
    
                        # Validasi stok bahan baku
                        komposisi_list = session.query(KomposisiMenu).filter(KomposisiMenu.menu_id == menu_id).all()
                        insufficient_stock = False
                        for komposisi in komposisi_list:
                            bahan = session.query(BahanBaku).filter(BahanBaku.bahan_id == komposisi.bahan_id).with_for_update().first()
                            if bahan:
                                total_kebutuhan = komposisi.jumlah_bahan * jumlah
                                if bahan.stock < total_kebutuhan:
                                    st.error(f"Stok bahan {bahan.nama_bahan} tidak mencukupi untuk transaksi ini.")
                                    insufficient_stock = True
                                    break  # Keluar dari loop jika stok tidak cukup
    
                        if insufficient_stock:
                            # Batalkan perubahan
                            session.rollback()
                            st.warning("Transaksi dibatalkan karena stok bahan baku tidak mencukupi.")
                        else:
                            # Mengurangi stok bahan baku
                            for komposisi in komposisi_list:
                                bahan = session.query(BahanBaku).filter(BahanBaku.bahan_id == komposisi.bahan_id).first()
                                if bahan:
                                    total_kebutuhan = komposisi.jumlah_bahan * jumlah
                                    bahan.stock -= total_kebutuhan
                                    session.commit()
                                    st.info(f"Stok bahan {bahan.nama_bahan} berkurang sebanyak {total_kebutuhan} {bahan.satuan}.")
    
                            # Menambahkan detail transaksi
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
                            st.success(f"Item {selected_menu.nama_menu} sebanyak {jumlah} berhasil ditambahkan.")
    
            # Menampilkan detail transaksi yang telah ditambahkan
            if st.session_state.detail_transaksi:
                df_detail = pd.DataFrame(st.session_state.detail_transaksi)
                st.table(df_detail)
    
            # Tombol untuk menyelesaikan transaksi
            if st.button("Selesaikan Transaksi"):
                total_transaksi = sum(item["Harga"] for item in st.session_state.detail_transaksi)
                current_transaksi = session.query(Transaksi).filter(Transaksi.transaksi_id == transaksi_id).first()
                current_transaksi.total_transaksi = total_transaksi
                session.commit()
                st.success(f"Transaksi selesai dengan total: {format_rupiah(total_transaksi)}")
                # Reset session state
                st.session_state.detail_transaksi = []
                
                # Bagian untuk memasukkan rating dan komentar feedback
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
                        st.success("Feedback Anda berhasil disimpan. Terima kasih atas partisipasinya!")
    
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
                            format_rupiah(t.total_transaksi)
                        )
                        for t in transaksi_list
                    ],
                    columns=["ID Transaksi", "Tanggal Pembelian", "ID Pelanggan", "ID Karyawan", "Total Transaksi"]
                )
                st.dataframe(df)
                # Export ke CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='daftar_transaksi.csv',
                    mime='text/csv',
                )
            else:
                st.info("Belum ada data transaksi.")


# Fungsi untuk mengelola Feedback
def manage_feedback(session: Session):
    action = st.selectbox("Aksi", ["Tambah", "Lihat", "Perbarui", "Hapus"])
    if action == "Tambah":
        st.subheader("Tambah Feedback")
        with st.form("form_tambah_feedback", clear_on_submit=True):
            tanggal = st.date_input("Tanggal Feedback", datetime.today())
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
            rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=5)
            komentar = st.text_area("Komentar (Opsional)", height=100)

            submit = st.form_submit_button("Simpan Feedback")
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
            # Tambahkan opsi export CSV
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
            selected_feedback = session.query(Feedback).filter(Feedback.feedback_id == selected_feedback_id).first()
            if selected_feedback:
                with st.form("form_perbarui_feedback"):
                    tanggal = st.date_input("Tanggal Feedback", selected_feedback.tanggal)
                    pelanggan_list = session.query(Pelanggan).all()
                    pelanggan_ids = [p.pelanggan_id for p in pelanggan_list]
                    karyawan_list = session.query(Karyawan).all()
                    karyawan_ids = [k.karyawan_id for k in karyawan_list]

                    pelanggan_id = st.selectbox("Pelanggan ID", pelanggan_ids, index=pelanggan_ids.index(selected_feedback.pelanggan_id)) if pelanggan_ids else None
                    karyawan_id = st.selectbox("Karyawan ID", karyawan_ids, index=karyawan_ids.index(selected_feedback.karyawan_id)) if karyawan_ids else None
                    rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=selected_feedback.rating)
                    komentar = st.text_area("Komentar (Opsional)", value=selected_feedback.komentar if selected_feedback.komentar else "", height=100)

                    submit = st.form_submit_button("Perbarui Feedback")
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
                selected_feedback = session.query(Feedback).filter(Feedback.feedback_id == selected_feedback_id).first()
                session.delete(selected_feedback)
                session.commit()
                st.success("Feedback berhasil dihapus.")
        else:
            st.info("Belum ada data feedback.")


def show_home():
    st.subheader("Selamat Datang di Sistem Manajemen Restoran")
    st.write("""
        Aplikasi ini membantu Anda dalam mengelola operasi restoran secara efisien.
        Anda dapat mengelola data karyawan, pelanggan, supplier, bahan baku, menu, transaksi, feedback, dan mendownload dalam format csv.
             by Radhitya Guntoro Adhi, Ahmad Hasyir Bastari, and Chindy Herpati
    """)
    st.image("https://img.freepik.com/free-vector/woman-wearing-medical-mask-client_52683-41295.jpg?t=st=1733793241~exp=1733796841~hmac=bb009a6af6983d59b067c6fcaa46fd80740848997d84ba9b81dd790fc548fd67&w=740", use_container_width=True)
    
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
    ]

    selected_menu = st.sidebar.selectbox("Navigasi", menu_options)

    session = get_session()

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

    session.close()

if __name__ == "__main__":
    main()
# Panggil fungsi main
