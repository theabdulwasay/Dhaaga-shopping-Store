<div align="center">

# 🧵 DHAAGA
### *Modern Cloth Brand E-Commerce Web Application*

<img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img src="https://img.shields.io/badge/AI-Chatbot-FF6B35?style=for-the-badge"/>

**A complete Django-powered online clothing store featuring product management, shopping cart, checkout, customer contact, AI chatbot, and an intuitive admin dashboard.**

</div>

---

# ✨ Features

## 🛍️ Customer Features

- 👕 Beautiful Product Catalog
- 🧵 Fabric Categories
- 🔍 Product Detail Pages
- 🛒 Session-Based Shopping Cart
- 💳 Cash on Delivery Checkout
- 📩 Contact Form
- 🤖 AI Chatbot on Every Page
- 📱 Fully Responsive Design

---

## ⚙️ Admin Features

- Manage Products
- Manage Fabrics
- Manage Orders
- View Customer Messages
- View AI Chat Logs
- Inventory Management
- Price Management
- Stock Management

Everything is handled directly from the **Django Admin Panel**.

---

# 🚀 Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | Django |
| Language | Python |
| Database | SQLite (Development) |
| Production Database | PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript |
| Static Files | WhiteNoise |
| AI | Anthropic Claude API |
| Environment Variables | python-dotenv |

---

# 📂 Project Structure

```
DHAAGA/
│
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── cart.py
│   ├── admin.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_shop.py
│
├── templates/
│   └── shop/
│       ├── base.html
│       ├── home.html
│       ├── cart.html
│       ├── checkout.html
│       ├── contact.html
│       └── ...
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
│
├── media/
├── staticfiles/
├── requirements.txt
├── manage.py
└── README.md
```

---

# 🧱 Database Models

The project includes the following models:

| Model | Description |
|---------|------------|
| Fabric | Fabric categories |
| Product | Clothing products |
| Order | Customer orders |
| OrderItem | Products inside orders |
| ContactMessage | Customer inquiries |
| ChatLog | AI chatbot conversations |

---

# ⚡ Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/dhaaga.git

cd dhaaga
```

---

## 2️⃣ Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

---

## 5️⃣ Seed Demo Data

```bash
python manage.py seed_shop
```

Adds:

- Fabric Categories
- Demo Products
- Sample Inventory

---

## 6️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

---

## 7️⃣ Run Development Server

```bash
python manage.py runserver
```

---

# 🌐 Application URLs

| URL | Description |
|------|------------|
| http://127.0.0.1:8000 | Storefront |
| http://127.0.0.1:8000/admin | Django Admin |

---

# 🔑 Demo Admin

```
Username : admin

Password : dhaaga123
```

> ⚠️ **Change this password before deploying to production.**

---

# 🤖 AI Chatbot

Every page includes an AI chatbot.

Without an API key:

> Friendly "Chatbot not configured yet" message

With API key:

- Customer support
- Product questions
- Order assistance
- Chat history logging

Enable it using:

```bash
export ANTHROPIC_API_KEY=sk-ant-...

python manage.py runserver
```

---

# 🛒 Shopping Cart

- Session Based
- No Login Required
- Update Quantity
- Remove Products
- Persistent During Session

---

# 💳 Checkout

Current payment flow:

✅ Cash on Delivery

Future integrations:

- JazzCash
- EasyPaisa
- Stripe
- PayPal

---

# 📩 Contact System

Customers can:

- Send inquiries
- Ask questions
- Report issues

Messages are stored inside Django Admin.

---

# 📊 Django Admin

Manage everything from one dashboard:

- Products
- Categories
- Fabrics
- Inventory
- Prices
- Orders
- Contact Messages
- Chat Logs

No coding required.

---

# 🚀 Production Deployment

## Configure Environment

Copy environment template:

```bash
cp .env.example .env
```

Example:

```env
DEBUG=False

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://user:password@localhost:5432/dhaaga_db

ANTHROPIC_API_KEY=sk-ant-...

SECURE_SSL_REDIRECT=True

SESSION_COOKIE_SECURE=True

CSRF_COOKIE_SECURE=True
```

---

## Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Create PostgreSQL Database

```bash
createdb dhaaga_db
```

---

## Run Migrations

```bash
python manage.py migrate

python manage.py seed_shop
```

---

## Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Run Gunicorn

```bash
gunicorn dhaaga_project.wsgi:application \
--bind 0.0.0.0:8000 \
--workers 3
```

---

# 🌍 Example Nginx Configuration

```nginx
server {

    listen 80;

    server_name yourdomain.com;

    location / {

        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;

    }

    location /static/ {

        alias /path/to/project/staticfiles/;

    }

    location /media/ {

        alias /path/to/project/media/;

    }

}
```

---

# 🔒 Enable HTTPS

Using Let's Encrypt:

```bash
sudo certbot --nginx \
-d yourdomain.com \
-d www.yourdomain.com
```

---

# ✅ Production Checklist

- [ ] DEBUG=False
- [ ] Secure SECRET_KEY
- [ ] PostgreSQL Database
- [ ] HTTPS Enabled
- [ ] Static Files Collected
- [ ] Media Files Configured
- [ ] Strong Admin Password
- [ ] AI API Key Added
- [ ] Firewall Configured
- [ ] Backups Enabled
- [ ] Logging Enabled

---

# 📜 Logging

Logs are stored in:

```
logs/django.log
```

Monitor:

- Errors
- Security Events
- Performance
- User Activity

---

# 💡 Future Improvements

- ❤️ Wishlist
- ⭐ Product Reviews
- 🔐 User Authentication
- 💳 Online Payments
- 📦 Order Tracking
- 📧 Email Notifications
- 🎟️ Discount Coupons
- 📈 Sales Dashboard
- 📱 Progressive Web App
- 🌍 Multi-language Support

---

# 📌 Notes

- Session-based cart (No login required)
- Easy to manage via Django Admin
- WhiteNoise for static file serving
- Environment variables managed using **python-dotenv**
- AI chatbot gracefully handles missing API keys
- Designed for easy deployment on VPS or cloud platforms

---

<div align="center">

## 🌟 If you like this project, don't forget to give it a ⭐ on GitHub!

**Made with ❤️ using Django & Python**

</div>
<img width="1878" height="825" alt="image" src="https://github.com/user-attachments/assets/51297b39-9440-4134-ba3c-47c6e194e36b" />
<img width="1877" height="825" alt="image" src="https://github.com/user-attachments/assets/77b5cd86-41fe-4fca-b907-4ce97dee2c7a" />
<img width="1870" height="824" alt="image" src="https://github.com/user-attachments/assets/0ae26383-21c3-4b94-9972-4edbbeb6d574" />
<img width="1876" height="815" alt="image" src="https://github.com/user-attachments/assets/9c5b2055-bf4d-4144-b735-8cccc38fff40" />

