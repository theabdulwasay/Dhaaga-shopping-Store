# DHAAGA — Cloth Brand Web App (Django + SQLite)

A full storefront for a cloth brand: product catalog, cart, checkout (cash on
delivery), contact form, Django admin, and an AI chatbot widget on every page.

## What's inside
- **shop/models.py** — Fabric, Product, Order, OrderItem, ContactMessage, ChatLog
- **shop/views.py** — catalog, cart, checkout, contact, and `/api/chat/` endpoint
- **shop/cart.py** — simple session-based cart (no extra packages needed)
- **templates/shop/** — all pages, extending `base.html`
- **static/css/style.css**, **static/js/chat.js** — styling + chatbot widget JS
- SQLite database (`db.sqlite3`) — created automatically on first migrate

## Quick Start (Development)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_shop      # adds starter fabrics + 6 products
python manage.py createsuperuser

python manage.py runserver
```

Visit:
- http://127.0.0.1:8000/ — storefront
- http://127.0.0.1:8000/admin/ — manage products, orders, messages, chat logs

A demo admin account is already included in this build:
- username: `admin`
- password: `dhaaga123`
**Change this password before deploying anywhere public.**

## Production Deployment

### 1. Environment Configuration

Copy the example environment file and configure it for production:

```bash
cp .env.example .env
```

Edit `.env` with production values:
```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/dhaaga_db
ANTHROPIC_API_KEY=sk-ant-...
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Important:**
- Generate a secure `SECRET_KEY` using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Set `DEBUG=False` in production
- Use PostgreSQL instead of SQLite for production
- Configure SSL/TLS certificates

### 2. Install Production Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup (PostgreSQL)

Create a PostgreSQL database:
```bash
createdb dhaaga_db
```

Update `.env` with your database credentials.

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run Migrations

```bash
python manage.py migrate
python manage.py seed_shop
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run with Gunicorn

```bash
gunicorn dhaaga_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

For production, consider using a process manager like systemd or supervisor.

### 8. Web Server Configuration (Nginx)

Example Nginx configuration:

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
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

### 9. SSL/TLS Configuration

Use Let's Encrypt for free SSL certificates:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Security Checklist

Before deploying to production, ensure:

- [ ] `DEBUG=False` in environment variables
- [ ] Strong `SECRET_KEY` generated and set
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] PostgreSQL database instead of SQLite
- [ ] SSL/TLS enabled (HTTPS)
- [ ] Static files collected
- [ ] Media files properly configured
- [ ] Firewall configured (only allow necessary ports)
- [ ] Regular backups configured
- [ ] Admin password changed from default
- [ ] `ANTHROPIC_API_KEY` configured (if using chatbot)

## Enabling the live chatbot
The chat widget posts to `/api/chat/`, which calls the Anthropic API
server-side. Without a key it replies with a friendly "not configured yet"
message instead of failing. To turn it on:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python manage.py runserver
```

Chat turns are logged in the `ChatLog` model, viewable in the admin, so you
can see what customers are asking.

## Managing products
Everything (fabrics, products, stock, prices, orders, contact messages) is
editable from `/admin/` — no code changes needed to update the catalog.

## Logging

Production logs are stored in `logs/django.log`. Monitor logs regularly for:
- Application errors
- Security issues
- Performance bottlenecks
- User activity

## Notes
- Cart is stored in the session, so it doesn't require login.
- Checkout is cash-on-delivery style: it just records the order; wire up a
  payment gateway (e.g. JazzCash/EasyPaisa/Stripe) later if needed.
- The project uses Whitenoise for static file serving in production.
- Environment variables are loaded from `.env` file using python-dotenv.
