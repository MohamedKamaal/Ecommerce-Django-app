
# 🛒 Django E-commerce Platform


A full-featured **E-commerce web application** built with Django and PostgreSQL, styled with TailwindCSS, and deployed on AWS EC2. The project supports modern e-commerce capabilities like product variations, shopping cart, Stripe payments, order management, email notifications, and user authentication.

## Demo
live demo http://56.228.60.131/

## 🧩 Tech Stack

- **Backend**: Django
- **Frontend**: TailwindCSS (via Django templates)
- **Database**: PostgreSQL
- **Authentication**: `django-allauth`, social login
- **Cloud Image Hosting**: Cloudinary
- **Payments**: Stripe
- **Deployment**: AWS EC2 (Ubuntu/Linux)
- **Others**:
  - `django-countries`, `phonenumber_field`
  - `colorfield` for product color variants
  - `django-extensions` for dev tools
  - `taggit` for product tagging
  - `cities-light` for location autocomplete

## 🧱 Apps Structure

| App        | Responsibility                                       |
|------------|------------------------------------------------------|
| `users`    | Custom user model & manager, profile logic          |
| `store`    | Products, categories, product variations             |
| `cart`     | Cart logic and views (add, remove, update, total)   |
| `orders`   | Order creation, confirmation, and tracking          |
| `payments` | Stripe integration and payment verification         |
| `shipping` | Shipping address and delivery info forms            |
| `reviews`  | Product reviews and ratings                         |
## 🚀 Features

### 🔐 Authentication
- Custom User Model (email as unique identifier)
- User registration, login, logout
- Email verification with `django-allauth`

### 🏪 Storefront
- Home page with **latest** and **popular** products
- Category-based browsing
- Product detail pages with:
  - Variations (size, color, price)
  - Cloudinary-hosted product images
  - Tag support (`django-taggit`)
  - Review and rating system
- Search and filter capabilities

### 🛒 Shopping Cart
- Session-based cart logic (`add`, `remove`, `clear`, `get total`, etc.)
- Cart preview and CRUD before checkout
- Supports quantity updates and variation options

### 💳 Checkout & Orders
- Stripe integration for secure payments
- Shipping information form
- Order summary and confirmation
- Order saved only on successful payment
- Email notifications:
  - On order creation
  - After payment confirmation

### 🌍 Internationalization
- Country and phone field support
- City autocomplete with `cities_light`

### 🌐 Admin Panel
- Powered by Django admin
- Manage products, categories, users, orders
- SEO-friendly model settings

---
## Deployment

Deployed on aws ec2

## 📦 Installation

Follow these steps to get the project running locally:

### 1. Clone the repository

```bash
git clone https://github.com/MohamedKamaal/Ecommerce-Django-app.git
cd Ecommerce-App
pip install -r requirements.txt
```

### 2. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 3. Run the development server
```bash
python manage.py runserver
```
