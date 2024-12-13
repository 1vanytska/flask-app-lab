import unittest
from app import create_app, db, bcrypt
from app.users.models import User
from flask import session

class UserTests(unittest.TestCase):
    def setUp(self):
        """Налаштування перед кожним тестом."""
        self.app = create_app("test")  # Використання тестової конфігурації
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Створення тестового користувача
        hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')
        self.user = User(username="testuser", email="test@example.com", password=hashed_password)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Очистка після кожного тесту."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # --- Тестування Views ---
    def test_registration_page_loads(self):
        """Перевіряє, чи сторінка реєстрації завантажується успішно."""
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page_loads(self):
        """Перевіряє, чи сторінка входу завантажується успішно."""
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    # --- Тестування функціоналу реєстрації ---
    def test_user_registration(self):
        """Перевіряє, чи користувач успішно зберігається в базу даних при реєстрації."""
        response = self.client.post("/users/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword"
        })

        self.assertEqual(response.status_code, 302)

        # Перевіряємо, чи новий користувач збережений у БД
        user = User.query.filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "newuser")

    def test_registration_with_existing_email(self):
        """Перевіряє, чи забороняється реєстрація з вже існуючою електронною поштою."""
        response = self.client.post("/users/register", data={
            "username": "duplicateuser",
            "email": "test@example.com",  # Вже існуючий email
            "password": "password123",
            "confirm_password": "password123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email is already registered", response.data)

    def test_user_login(self):
        with self.client:
            response = self.client.post('/users/login', data={
                'username': 'testuser',
                'password': 'password123',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome', response.data)


    def test_user_logout(self):
        with self.client:
            # Увійти
            self.client.post('/users/login', data={
                'username': 'testuser',
                'password': 'password123',
            })
            # Вийти
            response = self.client.get('/users/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with self.client.session_transaction() as sess:
                self.assertNotIn("user_id", sess)


if __name__ == "__main__":
    unittest.main()
