import datetime
from utils import DataValidator
from models import Food, Drink, Household

# 10. InventoryManager (CRUD & 30 Produk Default)
class InventoryManager:
    def __init__(self):
        self.products = []
        self._seed_data()

    def _seed_data(self):
            # 1. KATEGORI MAKANAN (Food)
            # Format: Food("Nama", HargaJual, HargaModal, Stok)
            food_items = [
                Food("Indomie Goreng", 3500, 2500, 100),
                Food("Beras 5kg", 75000, 68000, 20),
                Food("Telur 1kg", 28000, 24000, 30),
                Food("Minyak Goreng 2L", 34000, 30000, 25),
                Food("Gula Pasir 1kg", 16000, 14000, 40),
                Food("Roti Tawar", 15000, 12000, 15),
                Food("Sarden ABC", 22000, 18000, 20),
                Food("Susu UHT 1L", 18500, 16000, 24),
                Food("Garam Halus", 5000, 3500, 50),
                Food("Tepung Terigu", 12000, 10000, 30)
            ]

            # 2. KATEGORI MINUMAN (Drink)
            drink_items = [
                Drink("Aqua 600ml", 3500, 2000, 100),
                Drink("Coca Cola 1L", 15000, 12000, 12),
                Drink("Teh Pucuk", 4000, 2500, 50),
                Drink("Kopi Kapal Api", 12000, 9000, 30),
                Drink("Pocari Sweat", 8000, 6000, 24),
                Drink("Susu Beruang", 11000, 9500, 20),
                Drink("Sirup Marjan", 25000, 21000, 12),
                Drink("Jus Buah Kotak", 7000, 5000, 20),
                Drink("Sprite 1L", 15000, 12000, 12),
                Drink("Yakuult (5 pcs)", 10000, 8500, 15)
            ]

            # 3. KATEGORI ALAT RT (Household)
            house_items = [
                Household("Sabun Mandi", 5000, 3500, 40),
                Household("Sampo 170ml", 25000, 21000, 15),
                Household("Pasta Gigi", 14000, 11000, 25),
                Household("Sikat Gigi", 7500, 5000, 30),
                Household("Deterjen 800g", 28000, 24000, 20),
                Household("Pewangi Pakaian", 15000, 12000, 20),
                Household("Sabun Cuci Piring", 10000, 8000, 25),
                Household("Tisu Wajah", 12000, 9000, 30),
                Household("Pembersih Lantai", 18000, 15000, 15),
                Household("Spons Cuci", 3000, 1500, 50)
            ]

            # Gabungkan semua ke dalam list produk utama
            self.products.extend(food_items)
            self.products.extend(drink_items)
            self.products.extend(house_items)

    def search_product(self, keyword):
        results = [p for p in self.products if keyword.lower() in p.name.lower()]
        print(f"\n--- Hasil Pencarian: '{keyword}' ---")
        for p in results: print(p.display_info())
        if not results: print("Produk tidak ditemukan.")
        return results

    def add_product(self, product):
        self.products.append(product)
        print(f"[SUKSES] Produk {product.name} berhasil ditambahkan.")

    def delete_product(self, product_name):
        for p in self.products:
            if p.name.lower() == product_name.lower():
                self.products.remove(p)
                print(f"[SUKSES] Produk {p.name} dihapus (Alasan: Habis/Expired).")
                return True
        print("[GAGAL] Produk tidak ditemukan.")
        return False

# 11. TransactionManager (Logika Kasir)
class TransactionManager:
    def __init__(self, inventory):
        self.inventory = inventory
        self.history = []

    def process_sale(self, cashier_name):
        print("\n--- TRANSAKSI PENJUALAN ---")
        cart = []
        total_price = 0
        
        while True:
            keyword = DataValidator.input_tidak_kosong("Masukkan nama produk (atau 'selesai'): ")
            if keyword.lower() == 'selesai': break
            
            results = self.inventory.search_product(keyword)
            if results:
                prod = results[0]
                try:
                    qty = int(input(f"Berapa banyak {prod.name}? "))
                    if prod.reduce_stock(qty):
                        subtotal = prod.sell_price * qty
                        cart.append({"nama": prod.name, "qty": qty, "harga": prod.sell_price, "subtotal": subtotal})
                        total_price += subtotal
                        print(f"[+] {qty} {prod.name} ditambahkan.")
                    else:
                        print(f"[!] Stok tidak cukup! Sisa: {prod.stock}")
                except ValueError: print("[!] Input harus angka.")
        if cart:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append({"kasir": cashier_name, "tanggal": date_str, "total": total_price, "items": cart})
            
            print("\n" + "="*40)
            print(" "*12 + "STRUK PEMBELIAN")
            print("="*40)
            print(f"Tanggal : {date_str}\nKasir   : {cashier_name}")
            print("-" * 40)
            for item in cart: print(f"{item['nama']:20} x{item['qty']:<3} Rp{item['subtotal']}")
            print("-" * 40)
            print(f"TOTAL   : Rp{total_price}")
            print("="*40)

# 12. ReportManager (Cetak Laporan)
class ReportManager: 
    @staticmethod
    def print_stock_report(inventory):
        print("\n" + "="*90)
        print(" "*32+ "LAPORAN STOK BARANG")
        print("="*90)
        
        # Header tabel
        print(f"{'No':<4} | {'Nama Produk':20} | {'Kategori':12} | {'Stok':5} | {'Jual':10} | {'Modal':10} | {'Margin':10}")
        print("-"*90)
        
        # Isi data
        for i, p in enumerate(inventory.products, start=1):
            margin = p.sell_price - p.buy_price
            print(f"{i:<4} | {p.name:20} | {p.category:12} | {p.stock:<5} | Rp{p.sell_price:<8} | Rp{p.buy_price:<8} | Rp{margin:<8}")
        
        print("-"*90)
        print(f"Total Produk: {len(inventory.products)}")
        print("="*90)

    @staticmethod
    def print_transaction_report(history):
        print("\n=== LAPORAN TRANSAKSI KESELURUHAN ===")
        total_omzet = 0
        for trx in history:
            print(f"[{trx['tanggal']}] Kasir: {trx['kasir']} | Total: Rp{trx['total']}")
            total_omzet += trx['total']
        print(f"-> TOTAL OMZET: Rp{total_omzet}")