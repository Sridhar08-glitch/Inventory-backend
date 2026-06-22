<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a73e8,100:00c853&height=220&section=header&text=Inventory%20Hub%20API&fontSize=72&fontColor=ffffff&fontAlignY=40&desc=Django%20REST%20Framework%20%E2%80%94%20Production-Ready%20Inventory%20Backend&descAlignY=60&descSize=18&descColor=e0f7ef&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.15-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Token Auth](https://img.shields.io/badge/Auth-Token_Based-FF8C00?style=for-the-badge&logo=jsonwebtokens&logoColor=white)]()

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
[![Code Style](https://img.shields.io/badge/Code_Style-PEP_8-blue?style=for-the-badge)](https://pep8.org/)
[![Status](https://img.shields.io/badge/Status-Active-00c853?style=for-the-badge)]()

<br/>

[![Quick Start](https://img.shields.io/badge/⚡_Quick_Start-Read_Below-1a73e8?style=for-the-badge)](#-quick-start)
[![API Docs](https://img.shields.io/badge/🔌_API_Reference-Browse_Endpoints-00c853?style=for-the-badge)](#-api-reference)
[![Report Bug](https://img.shields.io/badge/🐛_Report_Bug-Open_Issue-red?style=for-the-badge)](https://github.com/sridhar-mahalingam/inventory-hub/issues)

</div>

---

## 📋 Table of Contents

- [📖 About](#-about)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🗂️ Project Structure](#️-project-structure)
- [⚡ Quick Start](#-quick-start)
- [🔑 Environment Variables](#-environment-variables)
- [🔌 API Reference](#-api-reference)
- [🔐 Authentication](#-authentication)
- [🛡️ Django Admin Panel](#️-django-admin-panel)
- [🚀 Production Checklist](#-production-checklist)
- [🔧 Known Limitations & Roadmap](#-known-limitations--roadmap)
- [🤝 Contributing](#-contributing)
- [👨‍💻 Author](#-author)
- [📜 License](#-license)

---

## 📖 About

**Inventory Hub API** is a production-ready **Django REST Framework** backend powering a full-stack inventory management system. It handles product catalogs, supplier relationships, color-coded categories, sale order processing with automatic stock deduction, stock movement tracking with server-side integrity, and per-user business profiles — all behind a clean, token-authenticated REST API.

> 💡 Every stock movement is computed **server-side** to guarantee inventory integrity. The client never supplies `stock_before` or `stock_after` values — the API computes them atomically before responding.

### Why Inventory Hub API?

| 🚩 Challenge | ✅ How We Solve It |
|---|---|
| Stock drift from race conditions | Server-side atomic stock computation on every movement — no client-supplied values |
| 🔒 Hardcoded secrets in codebase | `python-decouple` — all secrets live in `.env`, never in source code |
| 🌐 CORS wildcard exposure | Locked to explicit `CORS_ALLOWED_ORIGINS` whitelist, `CORS_ALLOW_ALL_ORIGINS = False` |
| 🗑️ Wildcard `import *` chaos | All imports are explicit, named, and traceable throughout the codebase |
| 📋 Client-supplied server-computed fields | `read_only` serializer fields + `serializer.save(**kwargs)` pattern |
| 👁️ Debug information leakage | `DEBUG=False` by default via environment — no accidental production tracebacks |

---

## ✨ Features

<table>
<tr>
<td valign="top">

### 📦 Product Catalog
- Full CRUD with product image upload (`Pillow`)
- SKU-based unique product identification
- Barcode field for scanner integrations
- Low-stock alert threshold per product (`min_stock_alert`)
- Bulk product import via CSV endpoint (`/bulk_create/`)
- Status lifecycle: `active` → `inactive` → `discontinued`
- Expiry date tracking for perishable goods

</td>
<td valign="top">

### 🏭 Stock Control
- Atomic stock-in / stock-out / adjustment movements
- Server-computed `stock_before` & `stock_after` on every record
- Movement history with `reason` and `reference` fields
- Automatic stock deduction on sale order creation
- Full movement audit trail ordered by timestamp

</td>
</tr>
<tr>
<td valign="top">

### 🛒 Sales Orders
- Full order lifecycle (creation → items → stock update → movement log)
- Multi-line item support per order
- Payment status: `pending` / `paid` / `partial` / `refunded`
- Customer name + email capture
- Subtotal, tax amount, and total stored independently
- Cascading delete — removing an order removes its items

</td>
<td valign="top">

### 👤 Users & Admin
- DRF Token Authentication (one token per user)
- Per-user business profile (name, address, currency, tax rate)
- `GET /me/` and `PUT /me/update/` for self-service profile management
- Rich Django Admin panel for all 7 models
- `SaleItem` inline view inside `SaleOrderAdmin`
- Superuser-based access control

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                React Frontend (Vite 8)                  │
│  Authorization: Token <token>  →  Every API request     │
└──────────────────┬──────────────────────────────────────┘
                   │  HTTP  /  REST  /  JSON
┌──────────────────▼──────────────────────────────────────┐
│              Django REST Framework API                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │categories│  │ products │  │  sales   │  │ stock  │  │
│  │ ViewSet  │  │ ViewSet  │  │ ViewSet  │  │ViewSet │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       └──────────────┴─────────────┴─────────────┘      │
│                        │                                 │
│  ┌─────────────────────▼──────────────────────────────┐ │
│  │             Serializers (DRF)                       │ │
│  │   Validates input · Enforces read_only fields       │ │
│  └─────────────────────┬──────────────────────────────┘ │
│                         │                                │
│  ┌──────────────────────▼──────────────────────────────┐│
│  │                 Django ORM / Models                  ││
│  │  Category · Supplier · Product · SaleOrder ·        ││
│  │  SaleItem · StockMovement · UserProfile              ││
│  └──────────────────────┬──────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                           │
              ┌────────────▼─────────────┐
              │        MySQL 8.0          │
              │    database: inven        │
              └──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Web Framework** | Django | 5.1 | ORM, routing, migrations, admin |
| **REST Layer** | Django REST Framework | 3.15 | Serializers, ViewSets, routers, pagination |
| **Authentication** | DRF Token Auth | built-in | Stateless per-user token authentication |
| **Database** | MySQL + `mysqlclient` | 8.0 | Primary relational data store |
| **Env Management** | `python-decouple` | 3.8+ | `.env`-based secret management |
| **CORS** | `django-cors-headers` | 4.4+ | Cross-origin request policy enforcement |
| **Images** | `Pillow` | 10.0+ | Product image field processing & validation |
| **Pagination** | DRF `PageNumberPagination` | built-in | 100 records per page |
| **File Storage** | Django `default_storage` | built-in | Media file uploads under `media/uploads/` |

---

## 🗂️ Project Structure

```
Inventory-Backend/
│
├── 📄 manage.py                    # Django management CLI
├── 📄 requirements.txt             # Python dependency pinning
├── 📄 .env                         # 🔒 Secrets — never commit!
├── 📄 .env.example                 # Template — copy to .env
│
├── 📁 Inventory/                   # Django project configuration
│   ├── 📄 settings.py              # All config via python-decouple
│   ├── 📄 urls.py                  # Root URL: /api/ + /media/ + /admin/
│   ├── 📄 wsgi.py                  # WSGI entrypoint (Gunicorn in prod)
│   └── 📄 asgi.py                  # ASGI entrypoint (future async)
│
├── 📁 api/                         # Main Django application
│   ├── 📄 models.py                # 7 models with __str__, typed fields
│   │                               #   Category · Supplier · Product
│   │                               #   SaleOrder · SaleItem
│   │                               #   StockMovement · UserProfile
│   ├── 📄 serializers.py           # DRF serializers — explicit imports,
│   │                               #   read_only stock fields, nested items
│   ├── 📄 views.py                 # ViewSets + auth views + upload endpoint
│   ├── 📄 urls.py                  # Router (5 resources) + manual auth paths
│   ├── 📄 admin.py                 # Rich admin registration — all 7 models,
│   │                               #   fieldsets, search, filter, inline items
│   ├── 📄 apps.py
│   └── 📁 migrations/              # Django auto-generated migrations
│
└── 📁 media/                       # Runtime-generated (gitignored)
    ├── 📁 products/                # Product images from ImageField
    └── 📁 uploads/                 # Files from /api/upload/ endpoint
```

---

## ⚡ Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white&style=flat-square) | 3.10 or higher |
| ![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white&style=flat-square) | 8.0 or higher |
| ![Git](https://img.shields.io/badge/Git-Latest-f05032?logo=git&logoColor=white&style=flat-square) | Any recent version |

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd Inventory-Backend
```

### 2️⃣ Create & Activate Virtual Environment

```bash
# Create
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

```bash
cp .env.example .env
# Open .env and fill in your values
```

### 5️⃣ Create the MySQL Database

```sql
-- In your MySQL client
CREATE DATABASE inven
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 6️⃣ Run Database Migrations

```bash
python manage.py migrate
```

### 7️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

### 8️⃣ Start the Development Server

```bash
python manage.py runserver
```

> ✅ API live at **`http://127.0.0.1:8000/api/`**  
> ✅ Admin panel at **`http://127.0.0.1:8000/admin/`**  
> ✅ Media files at **`http://127.0.0.1:8000/media/`**

---

## 🔑 Environment Variables

Copy `.env.example` → `.env` and set each value:

```env
# Django Core
SECRET_KEY=your-long-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS — comma-separated frontend origins
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# MySQL Database
DB_NAME=inven
DB_USER=root
DB_PASSWORD=your-db-password-here
DB_HOST=localhost
DB_PORT=3306
```

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `SECRET_KEY` | — | ✅ Yes | Django cryptographic secret — keep it long, random, and private |
| `DEBUG` | `False` | — | `True` for development; **always `False` in production** |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | ✅ Prod | Comma-separated allowed host/domain names |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,...` | ✅ Yes | Comma-separated frontend origins that may call the API |
| `DB_NAME` | `inven` | ✅ Yes | MySQL database name |
| `DB_USER` | `root` | ✅ Yes | MySQL username |
| `DB_PASSWORD` | — | ✅ Yes | MySQL password |
| `DB_HOST` | `localhost` | — | MySQL host |
| `DB_PORT` | `3306` | — | MySQL port |

> ⚠️ **Never commit `.env` to version control.** It is already in `.gitignore`.

---

## 🔌 API Reference

All endpoints are prefixed with `/api/`. All endpoints **except** `POST /api/auth/login/` require:

```http
Authorization: Token <your-token-here>
```

---

### 🔐 Authentication Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/login/` | Public | Obtain token + user profile |
| `POST` | `/api/auth/logout/` | 🔑 Token | Invalidate and delete current token |
| `GET` | `/api/auth/me/` | 🔑 Token | Retrieve current user + business profile |
| `PUT` | `/api/auth/me/update/` | 🔑 Token | Update user fields and business profile |

**Login request / response:**

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "yourpassword"
}
```

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User"
  },
  "business_name": "Sridhar",
  "business_email": "sridharansridhar22@gmail.com"
}
```

---

### 📂 Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/categories/` | List all categories |
| `POST` | `/api/categories/` | Create a category |
| `GET` | `/api/categories/{id}/` | Retrieve a single category |
| `PUT` | `/api/categories/{id}/` | Full update |
| `PATCH` | `/api/categories/{id}/` | Partial update |
| `DELETE` | `/api/categories/{id}/` | Delete a category |

**Fields:** `id`, `name`, `description`, `color` (hex string), `created_date`, `updated_date`

---

### 🏭 Suppliers

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/suppliers/` | List all suppliers |
| `POST` | `/api/suppliers/` | Create a supplier |
| `GET` | `/api/suppliers/{id}/` | Retrieve a supplier |
| `PUT` | `/api/suppliers/{id}/` | Full update |
| `PATCH` | `/api/suppliers/{id}/` | Partial update |
| `DELETE` | `/api/suppliers/{id}/` | Delete a supplier |

**Fields:** `id`, `name`, `email`, `phone`, `address`, `contact_person`, `notes`, `created_date`, `updated_date`

---

### 📦 Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | List products — supports `?search=` |
| `POST` | `/api/products/` | Create a product |
| `GET` | `/api/products/{id}/` | Retrieve a product |
| `PUT` | `/api/products/{id}/` | Full update |
| `PATCH` | `/api/products/{id}/` | Partial update |
| `DELETE` | `/api/products/{id}/` | Delete a product |
| `POST` | `/api/products/bulk_create/` | Bulk import an array of products |

**Search** (`?search=`) queries across `name`, `sku`, `category`, and `supplier`.

```http
GET /api/products/?search=coffee
```

**Fields:** `id`, `name`, `sku`, `category`, `supplier`, `purchase_price`, `selling_price`, `stock_quantity`, `min_stock_alert`, `barcode`, `expiry_date`, `status`, `warehouse`, `image`, `image_url`, `created_date`, `updated_date`

---

### 🛒 Sales Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/sales/` | List all sale orders |
| `POST` | `/api/sales/` | Create order + items + auto-deduct stock |
| `GET` | `/api/sales/{id}/` | Retrieve order with nested items |
| `PUT` | `/api/sales/{id}/` | Full update |
| `PATCH` | `/api/sales/{id}/` | Partial update |
| `DELETE` | `/api/sales/{id}/` | Delete a sale order |

**Create sale order — request body:**

```json
{
  "order_number": "ORD-2024-001",
  "customer_name": "Jane Doe",
  "customer_email": "jane@example.com",
  "subtotal": "100.00",
  "tax_amount": "10.00",
  "total_amount": "110.00",
  "payment_status": "paid",
  "notes": "Rush delivery",
  "items": [
    {
      "product_id": "1",
      "product_name": "Coffee Beans 1kg",
      "sku": "COF-001",
      "quantity": 2,
      "unit_price": "50.00",
      "total": "100.00"
    }
  ]
}
```

> On creation, the API automatically deducts each item's `quantity` from `Product.stock_quantity` and records a `StockMovement` of type `out` for each product.

**Payment statuses:** `pending` · `paid` · `partial` · `refunded`

---

### 📊 Stock Movements

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/stock-movements/` | List all stock movements |
| `POST` | `/api/stock-movements/` | Record a movement (server computes before/after) |
| `GET` | `/api/stock-movements/{id}/` | Retrieve a single movement |
| `DELETE` | `/api/stock-movements/{id}/` | Delete a movement record |

**Create stock movement — request body:**

```json
{
  "product_id": "1",
  "product_name": "Coffee Beans 1kg",
  "product_sku": "COF-001",
  "type": "in",
  "quantity": 50,
  "reason": "Monthly restock from supplier",
  "reference": "PO-2024-042"
}
```

> ⚠️ `stock_before` and `stock_after` are **always computed server-side** and ignored if provided in the request body.

**Movement types:**

| Type | Effect |
|------|--------|
| `in` | `stock_after = stock_before + quantity` |
| `out` | `stock_after = max(0, stock_before − quantity)` |
| `adjustment` | `stock_after = quantity` (absolute set) |

---

### 📁 File Upload

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload/` | Upload an image file — returns its public URL |

```http
POST /api/upload/
Content-Type: multipart/form-data

file: <binary image>
```

**Response:**
```json
{
  "file_url": "http://127.0.0.1:8000/media/uploads/product-image.jpg"
}
```

---

## 🔐 Authentication

Inventory Hub uses **DRF Token Authentication** — one token per user, stored in the database, persisting until explicitly deleted via logout.

```
Auth Flow
══════════════════════════════════════════════════════════════
  1.  POST /api/auth/login/    →  { username, password }
  2.  Server responds          →  { token: "abc123...", user: {...} }
  3.  Client stores token      →  localStorage / secure cookie
  4.  Every request includes   →  Authorization: Token abc123...
  5.  Logout                   →  POST /api/auth/logout/
                                   (token row deleted from DB)
══════════════════════════════════════════════════════════════
```

All ViewSets are protected by default via Django REST Framework's global defaults:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES':     ['rest_framework.permissions.IsAuthenticated'],
}
```

Only `POST /api/auth/login/` carries `@permission_classes([AllowAny])`.

---

## 🛡️ Django Admin Panel

Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser account. All models are registered with rich configurations:

| Model | List Columns | Search Fields | Filters | Special |
|-------|-------------|---------------|---------|---------|
| **Category** | name, color, timestamps | name, description | — | — |
| **Supplier** | name, contact, email, phone | name, email, contact, phone | — | — |
| **Product** | name, sku, stock, status, price | name, sku, barcode | status, category | Grouped fieldsets |
| **SaleOrder** | order#, customer, total, payment | order#, customer, email | payment_status, status | `SaleItemInline` tab |
| **StockMovement** | product, type, qty, before, after | name, sku, reference | type | stock fields read-only |
| **UserProfile** | user, business, currency, tax | username, email, business | — | user field read-only |

---

## 🚀 Production Checklist

Before going live, verify every item:

- [ ] `DEBUG=False` in `.env`
- [ ] `SECRET_KEY` is long (50+ chars), random, and unique — never shared
- [ ] `ALLOWED_HOSTS` lists only your real domain(s)
- [ ] `CORS_ALLOWED_ORIGINS` lists only your production frontend URL
- [ ] Database password is strong and not reused elsewhere
- [ ] `python manage.py collectstatic` — static files collected
- [ ] Media files served by **Nginx** (not Django's `runserver`)
- [ ] **Gunicorn** (or uWSGI) used as the WSGI application server
- [ ] HTTPS enforced — no HTTP in production
- [ ] Database backups automated and tested
- [ ] `python manage.py check --deploy` passes without errors

---

## 🔧 Known Limitations & Roadmap

| Area | Current State | Planned Improvement |
|------|--------------|-------------------|
| **Product relations** | `category` and `supplier` stored as `CharField` | Migrate to proper `ForeignKey` for referential integrity |
| **Concurrency** | No DB-level row locking during stock updates | Add `select_for_update()` to eliminate race conditions under load |
| **Tests** | No automated test suite | Add `pytest-django` unit + integration tests |
| **API docs** | No Swagger/OpenAPI spec | Integrate `drf-spectacular` for auto-generated docs |
| **Auth tokens** | Simple static tokens | Consider JWT with refresh tokens for mobile clients |
| **Async tasks** | Fully synchronous | Add Celery + Redis for bulk import jobs and email notifications |
| **Filtering** | Search only | Add `django-filter` for multi-field filtering on list endpoints |

---

## 🤝 Contributing

Contributions are welcome and appreciated!

1. 🍴 **Fork** the repository
2. 🌿 **Create** your feature branch: `git checkout -b feature/your-feature-name`
3. ✍️ **Write** your code following [PEP 8](https://pep8.org/) conventions
4. ✅ **Test** your changes manually (automated tests coming soon)
5. 💾 **Commit** with a descriptive message: `git commit -m 'feat: add amazing feature'`
6. 📤 **Push** to your branch: `git push origin feature/your-feature-name`
7. 🔁 **Open** a Pull Request — describe what changed and why

---

## 👨‍💻 Author

<div align="center">

**Sridhar**

[![Email](https://img.shields.io/badge/Email-sridharansridhar22%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sridharansridhar22@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sridhar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sridhar-mahalingam-6b8357245)
[![Portfolio](https://img.shields.io/badge/Portfolio-sridharportfolio1.netlify.app-1a73e8?style=for-the-badge&logo=google-chrome&logoColor=white)](https://sridharportfolio1.netlify.app/)

</div>

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00c853,100:1a73e8&height=130&section=footer&text=Built%20with%20%E2%9D%A4%EF%B8%8F%20by%20Sridhar%20Mahalingam&fontSize=22&fontColor=ffffff&fontAlignY=65&animation=fadeIn" width="100%"/>

⭐ **If this helped you, give the repo a star!** ⭐

</div>
