from abc import ABC, abstractmethod

# 1. ABSTRACT BASE CLASS (ABC)
class BaseEntity(ABC):
    @abstractmethod
    def display_info(self): 
        pass


# 2. MIXIN & ENKAPSULASI (Name Mangling & Properties)
class StockManager:
    def __init__(self, stock):
        # 1. Name Mangling (Private Attribute)
        self.__stock = stock

    # 2. Property Getter (Mengakses atribut terlindungi)
    @property
    def stock(self): 
        return self.__stock

    # 3. Property Setter (Mengubah atribut terlindungi dengan aman)
    @stock.setter
    def stock(self, amount):
        if amount >= 0:
            self.__stock = amount
        else:
            raise ValueError("Stok tidak boleh negatif")

    def reduce_stock(self, amount):
        if self.__stock >= amount:
            self.__stock -= amount
            return True
        return False
        
    def add_stock(self, amount):
        self.__stock += amount


# 3. INHERITANCE & NAME MANGLING LANJUTAN
class Product(BaseEntity, StockManager, ABC):
    def __init__(self, name, sell_price, buy_price, stock, category):
        StockManager.__init__(self, stock)
        self.name = name
        
        # Public Attribute (Bisa diakses siapa saja)
        self.sell_price = sell_price
        
        # Name Mangling untuk data sensitif (Harga Modal)
        self.__buy_price = buy_price  
        self.category = category

    # Property untuk mengakses Harga Modal
    @property
    def buy_price(self):
        return self.__buy_price
    
    def margin(self):
        # Menghitung keuntungan per unit
        return self.sell_price - self.buy_price

    # Update fungsi display_info agar lebih lengkap untuk laporan
    def display_info(self):
        return f"{self.name:20} | {self.category:15} | {self.stock:<10}"

    def display_info(self):
        return f"{self.name:20} | Kategori: {self.category:15} | Stok: {self.stock:<4} | Harga: Rp{self.sell_price}"
    
    

# Kategori Produk (Inheritance dari Product)
class Food(Product):
    def __init__(self, name, sell_price, buy_price, stock):
        super().__init__(name, sell_price, buy_price, stock, "Makanan")


class Drink(Product):
    def __init__(self, name, sell_price, buy_price, stock):
        super().__init__(name, sell_price, buy_price, stock, "Minuman")


class Household(Product):
    def __init__(self, name, sell_price, buy_price, stock):
        super().__init__(name, sell_price, buy_price, stock, "Alat RT")


# 7. USER (ABC dengan Abstract Method)
class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        # Name Mangling untuk Password agar aman
        self.__password = password 
        self.role = role
        
    @property
    def password(self):
        return self.__password

    # Ditambah abstractmethod agar kelas ABC ini valid
    @abstractmethod
    def get_role_description(self):
        pass
    

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "ADMIN")
        
    def get_role_description(self):
        return "Administrator dengan akses penuh."


class Cashier(User):
    def __init__(self, username, password):
        super().__init__(username, password, "KASIR")
        
    def get_role_description(self):
        return "Kasir untuk melayani transaksi."