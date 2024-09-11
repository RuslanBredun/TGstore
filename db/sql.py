from config import Config
import sqlite3


class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, name):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (user_id, name, role) VALUES (?, ?, ?)""",
                                       [user_id, name, 'admin' if user_id == Config.admin_ids else 'user'])

    async def get_products(self, category_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE category_id=(?)""", [category_id]).fetchall()

    async def get_lang(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT language FROM users WHERE user_id=(?)""",
                                       [user_id]).fetchall()

    async def set_lang(self, user_id, lang):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET language = (?) WHERE user_id = (?)""",
                                       [lang, user_id])

    async def get_promotion(self):
        with self.connect:
            return self.cursor.execute("""SELECT s.description, s.discount, p.photo, p.price, p.name, p.product_id \
             FROM news_promotions s JOIN products p ON s.product_id = p.product_id""").fetchall()

    async def get_lang(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT language FROM users WHERE user_id=(?)""", [user_id]).fetchall()

    async def set_currency(self, user_id, currency):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET currency = (?) WHERE user_id = (?)""",
                                       [currency, user_id])

    async def get_currency(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT currency FROM users WHERE user_id=(?)""", [user_id]).fetchall()

    async def get_user_product(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE product_id=(?)""", [product_id]).fetchall()

    async def get_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT p.name, p.category_id, c.count, c.product_id, p.price, \
            p.description, p.photo FROM cart c JOIN products p ON c.product_id = p.product_id \
            WHERE c.user_id =(?)""", [user_id]).fetchall()

    async def get_favorites(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT p.name, p.category_id, c.count, \
            c.product_id, p.description, p.photo FROM favorites c \
            JOIN products p ON c.product_id = p.product_id WHERE c.user_id =(?)""", [user_id]).fetchall()

    async def add_to_cart(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""INSERT INTO cart (user_id, product_id, count) VALUES (?, ?, ?)""",
                                       [user_id, product_id, 1])

    async def add_to_fav(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""INSERT INTO favorites (user_id, product_id, count) VALUES (?, ?, ?)""",
                                       [user_id, product_id, 1])

    async def empty_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM cart WHERE user_id=(?)""", [user_id])

    async def get_categories(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM categories""").fetchall()

    async def get_count_in_cart(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM cart WHERE user_id=(?) AND product_id=(?)""",
                                       [user_id, product_id]).fetchall()

    async def get_in_fav(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM favorites WHERE user_id=(?) AND product_id=(?)""",
                                       [user_id, product_id]).fetchall()

    async def get_count_in_stock(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM products WHERE product_id=(?)""",
                                       [product_id]).fetchall()

    async def remove_one_item(self, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM cart WHERE product_id=(?) AND user_id=(?)""",
                                       [product_id, user_id])

    async def remove_favorites(self, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM favorites WHERE product_id=(?) AND user_id=(?)""",
                                       [product_id, user_id])

    async def change_count(self, count, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE cart SET count=(?) WHERE product_id=(?) AND user_id=(?)""",
                                       [count, product_id, user_id])

    async def add_to_orders(self, order_id, product_id, count, status, user_id):
        with self.connect:
            return self.cursor.execute("""INSERT INTO orders (order_id, product_id, count, status, user_id) \
            VALUES (?, ?, ?, ?, ?)""", [order_id, product_id, count, status, user_id])

    async def change_order_shipment(self, order_id, shipping, address):
        with self.connect:
            return self.cursor.execute("""UPDATE orders SET shipping = ?, address = ? WHERE order_id = ?""",
                                       (shipping, address, order_id))

    async def change_order_status(self, order_id, status):
        with self.connect:
            return self.cursor.execute("""UPDATE orders SET status=(?) WHERE order_id=(?) """,
                                       [status, order_id])

    async def get_last_order(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT order_id FROM orders WHERE user_id=(?) ORDER BY id DESC LIMIT 1;""",
                                       [user_id]).fetchall()
