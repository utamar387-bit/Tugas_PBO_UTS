import sys
from models import Admin, Cashier

# 13. DataValidator
class DataValidator:
    @staticmethod
    def is_positive(value):
        try: return float(value) > 0
        except ValueError: return False


    def input_tidak_kosong(pesan):
        while True:
            value = input(pesan).strip()
            if value == "":
                print("[ERROR] Input tidak boleh kosong atau hanya spasi!")
            else:
                return value

# 14. AuthService (Keamanan & Login)
class AuthService:
    def __init__(self):
        self.users = [
            Admin("shelfia", "admin123"), # Admin kelompok, bisa mengakses sistem lebih banyak
            Cashier("ridho", "kasir1"),
            Cashier("tio", "kasir2"),
            Cashier("taufik", "kasir3")
        ]
        self.max_attempts = 3

    def login(self):
        print("\n" + "="*40)
        print("      LOGIN SISTEM SMARTSTORE")
        print("="*40)
        attempts = 0
        
        while attempts < self.max_attempts:
            # Tambahan info untuk cara mematikan sistem
            uname = DataValidator.input_tidak_kosong("Username: ")
            
            # SISTEM BERHETI: Jika user ketik 0, program langsung mati
            if uname == '0' or uname.lower() == 'exit':
                print("\n[INFO] Menutup Sistem SmartStore. Sampai jumpa!")
                sys.exit() # Mematikan program sepenuhnya
                
            pwd = DataValidator.input_tidak_kosong("Password: ")
            
            for user in self.users:
                if user.username == uname and user.password == pwd:
                    print(f"\n[SUKSES] Selamat datang, {user.username} ({user.role})!")
                    return user
                
            
            attempts += 1
            print(f"[GAGAL] Username/Password salah! Sisa percobaan: {self.max_attempts - attempts}")
            
        print("\n[WARNING] Anda gagal login 3 kali. Sistem dikunci demi keamanan!")
        print("Silakan jalankan ulang (run) program.")
        sys.exit()

