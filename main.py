import sys
import unittest
from models import Food, Drink, Household
from utils import AuthService, DataValidator
from services import InventoryManager, TransactionManager, ReportManager

# 15. StoreApp (Controller Aplikasi)
class StoreApp:
    def __init__(self):
        self.auth = AuthService()
        self.inventory = InventoryManager()
        self.transaction = TransactionManager(self.inventory)
        self.current_user = None
        self.is_logged_in = False

    def run(self):
        # LOOP LUAR: Menjaga program tetap hidup dan kembali ke Login setelah logout
        while True:
            self.current_user = self.auth.login()
            
            # LOOP DALAM: Menahan user di menu sesuai perannya selama belum logout
            self.is_logged_in = True
            while self.is_logged_in:
                if self.current_user.role == "ADMIN": 
                    self.admin_menu()
                else: 
                    self.cashier_menu()

    def admin_menu(self):
        print("\n=== MENU ADMIN ===")
        print("1. Pencarian Produk")
        print("2. Tambah Produk Baru")
        print("3. Hapus Produk (Expired/Habis)")
        print("4. Laporan Stok & Harga Modal Rahasia")
        print("5. Laporan Transaksi")
        print("0. Logout")

        p = DataValidator.input_tidak_kosong("Pilih menu: ")
        if p == '1': 
            self.inventory.search_product(input("Kata kunci: "))
        elif p == '2':
            print("\n--- TAMBAH PRODUK BARU ---")
            print("Pilih Kategori:")
            print("1. Makanan (Food)")
            print("2. Minuman (Drink)")
            print("3. Alat RT (Household)")
            
            kat = input("Pilih (1/2/3): ")
            nama = input("Nama Produk: ")
            hj_raw = input("Harga Jual: ")
            hm_raw = input("Harga Modal: ")
            stok_raw = input("Stok Awal: ")

            if not kat or not nama or not hj_raw or not hm_raw or not stok_raw:
                print("\n[WARNING] Data tidak boleh ada yang kosong!")
            else:
                try:
                    hj, hm, stok = int(hj_raw), int(hm_raw), int(stok_raw)
                    # LOGIKA PEMILIHAN KATEGORI (Dynamic Object Creation)
                    if kat == '1':
                        new_prod = Food(nama, hj, hm, stok)
                    elif kat == '2':
                        new_prod = Drink(nama, hj, hm, stok)
                    elif kat == '3':
                        new_prod = Household(nama, hj, hm, stok)
                    else:
                        print("[ERROR] Kategori tidak valid!")
                        return
                    self.inventory.add_product(new_prod)
                    print(f"\n[SUKSES] '{nama}' berhasil masuk kategori {new_prod.category}!")
                except ValueError:
                    print("\n[ERROR] Harga/Stok harus angka!")
        elif p == '3': 
            self.inventory.delete_product(DataValidator.input_tidak_kosong("Nama produk dihapus: "))
        elif p == '4':
            ReportManager.print_stock_report(self.inventory)
            print("\n[DATA RAHASIA] Pengecekan Harga Modal:")
            for prod in self.inventory.products[:3]: # Tampilkan 3 untuk demo
                print(f"- {prod.name}: Modal Rp{prod.buy_price}, Jual Rp{prod.sell_price}")
        elif p == '5': 
            ReportManager.print_transaction_report(self.transaction.history)
        elif p == '0': 
            # Mengubah dari sys.exit() menjadi mengubah status login
            print("\n[INFO] Logout berhasil. Kembali ke halaman Login...")
            self.is_logged_in = False 
        else :
            print(f"\n[WARNING] Menu '{p}' tidak tersedia! Silakan pilih angka 0-6.")

    def cashier_menu(self):
        print("\n=== MENU KASIR ===")
        print("1. Transaksi Penjualan")
        print("2. Cari Produk")
        print("0. Logout")
        
        p = DataValidator.input_tidak_kosong("Pilih menu: ")
        if p == '1': 
            self.transaction.process_sale(self.current_user.username)
        elif p == '2': 
            self.inventory.search_product(input("Kata kunci: "))
        elif p == '0': 
            # Mengubah dari sys.exit() menjadi mengubah status login
            print("\n[INFO] Logout berhasil. Kembali ke halaman Login...")
            self.is_logged_in = False
        else :
            print(f"\n[WARNING] Menu '{p}' tidak tersedia! Silakan pilih angka 0-2.")


# --- UNIT TESTING ---
class TestSmartStore(unittest.TestCase):
    def setUp(self):
        self.inv = InventoryManager()
        self.trx_manager = TransactionManager(self.inv)
        self.test_prod = self.inv.products[0] # Ambil produk pertama (Indomie, stok: 50)

    # TEST 1: Memastikan Enkapsulasi & Name Mangling berjalan
    def test_1_encapsulation(self):
        with self.assertRaises(AttributeError):
            print(self.test_prod.__buy_price)
        self.assertIsNotNone(self.test_prod.buy_price)

    # TEST 2: Memastikan stok berkurang saat transaksi berhasil
    def test_2_stock_reduction(self):
        awal = self.test_prod.stock
        self.test_prod.reduce_stock(5)
        self.assertEqual(self.test_prod.stock, awal - 5)

    # TEST 3: Memastikan sistem menolak transaksi jika stok kurang (PERTANYAAN ANDA)
    def test_3_failed_transaction(self):
        awal = self.test_prod.stock
        result = self.test_prod.reduce_stock(awal + 10) # Beli lebih dari stok yang ada
        self.assertFalse(result) # Harus False (Gagal)
        self.assertEqual(self.test_prod.stock, awal) # Stok tidak boleh berubah

    # TEST 4: Memastikan laporan transaksi dan stok sesuai keadaan
    def test_4_report_accuracy(self):
        self.test_prod.reduce_stock(2) 
        harga_total = self.test_prod.sell_price * 2
        # Simulasi transaksi masuk ke riwayat
        self.trx_manager.history.append({
            "kasir": "ridho", 
            "tanggal": "2026-03-31", 
            "total": harga_total, 
            "items": []
        })
        
        # Cek kebenaran data laporan
        self.assertEqual(self.inv.products[0].stock, 98) # 100 - 2 = 98
        self.assertEqual(self.trx_manager.history[0]["total"], harga_total)


if __name__ == "__main__":
    print("Menjalankan Automasi Pengujian (Unit Tests)...")
    unittest.main(exit=False, verbosity=2) 

    print("\n" + "="*50)
    print("PENGUJIAN SELESAI. MEMULAI SISTEM SMARTSTORE...")
    print("="*50)
    
    # Supaya tidak error kalau user iseng tekan Ctrl+C di terminal
    try:
        app = StoreApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nSistem dimatikan secara paksa. Terima kasih telah menggunakan SmartStore.")
        sys.exit()