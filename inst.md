# 🛒 E-Commerce Backend — Junior Developer Guide
### Framework: Django + Django REST Framework (DRF)
---

## 📌 Why Django (Not FastAPI)?

| Feature | Django + DRF | FastAPI |
|---|---|---|
| Built-in Admin Panel | ✅ Yes (manage products, orders instantly) | ❌ No |
| Built-in Auth System | ✅ Yes | ❌ Manual setup |
| ORM (database tool) | ✅ Django ORM | ❌ Manual (SQLAlchemy) |
| Best for Beginners | ✅ More structure, less decisions | ⚠️ More flexible but harder |
| Speed (raw performance) | Good | Faster |
| Community/Resources | Massive | Growing |

**Verdict:** For a beginner building an e-commerce site, **Django + DRF** wins. It gives you an admin dashboard, user auth, and database management out of the box. FastAPI is excellent but better once you understand the fundamentals.

---

## 📦 What We're Building

A full e-commerce REST API with:
- User registration, login, logout (JWT tokens)
- Product catalog with categories
- Shopping cart
- Order placement & management
- Payment record
- Product reviews
- Admin access

---

## 1️⃣ Prerequisites — Install These First

```bash
# Make sure you have Python 3.10+ installed
python --version  # Should show 3.10 or higher

# Install pip if not present
python -m ensurepip --upgrade
```

---

## 2️⃣ Project Setup (Do This Once)

```bash
# Step 1: Create a project folder
mkdir ecommerce_backend
cd ecommerce_backend

# Step 2: Create a virtual environment (isolates your project dependencies)
python -m venv venv

# Step 3: Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Step 4: Install all required packages
pip install django djangorestframework djangorestframework-simplejwt \
            django-cors-headers Pillow python-decouple psycopg2-binary \
            django-filter

# Step 5: Save your dependencies to a file
pip freeze > requirements.txt

# Step 6: Create the Django project
django-admin startproject core .
# The dot (.) means "create in current folder"

# Step 7: Create Django apps (each app = one feature area)
python manage.py startapp users
python manage.py startapp products
python manage.py startapp orders
python manage.py startapp cart
python manage.py startapp reviews
```

---

## 3️⃣ Full Project File Structure

```
ecommerce_backend/
│
├── core/                        ← Main project settings
│   ├── __init__.py
│   ├── settings.py              ← All configuration lives here
│   ├── urls.py                  ← Root URL router
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                       ← User auth & profiles
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                ← User & Address models
│   ├── serializers.py           ← Convert model ↔ JSON
│   ├── views.py                 ← API logic
│   ├── urls.py                  ← User-specific routes
│   ├── admin.py                 ← Register in admin panel
│   └── permissions.py          ← Custom permission rules
│
├── products/                    ← Product catalog
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                ← Category, Product, ProductImage
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── filters.py               ← Search/filter logic
│
├── cart/                        ← Shopping cart
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                ← Cart, CartItem
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders/                      ← Order management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                ← Order, OrderItem, Payment
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── reviews/                     ← Product reviews
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                ← Review
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── media/                       ← Uploaded images (auto-created)
├── .env                         ← Secret keys (NEVER commit this)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 4️⃣ Settings Configuration

### `.env` file (create this in root folder)
```env
SECRET_KEY=your-very-secret-key-change-this-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### `core/settings.py`
```python
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ──────────────────────────────────────────────
# INSTALLED APPS
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # Our apps
    'users',
    'products',
    'cart',
    'orders',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',          # ← Must be near the top
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ──────────────────────────────────────────────
# DATABASE — SQLite for development, switch to Postgres in production
# ──────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ──────────────────────────────────────────────
# CUSTOM USER MODEL
# ──────────────────────────────────────────────
AUTH_USER_MODEL = 'users.User'  # Tell Django to use our custom User

# ──────────────────────────────────────────────
# DRF — Django REST Framework settings
# ──────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ──────────────────────────────────────────────
# JWT — Token settings
# ──────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # Access token expires in 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Refresh token lasts 7 days
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ──────────────────────────────────────────────
# CORS — Allow frontend to talk to backend
# ──────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev server
    "http://localhost:5173",    # Vite dev server
]
CORS_ALLOW_CREDENTIALS = True

# ──────────────────────────────────────────────
# MEDIA FILES — For product images
# ──────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

---

## 5️⃣ Database Models (The Tables)

> 💡 **What is a Model?** A model is a Python class that maps to a database table. Each attribute = a column.

---

### `users/models.py` — Custom User + Address

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    We extend Django's built-in User model.
    AbstractUser already gives us: username, email, password,
    first_name, last_name, is_staff, is_active, date_joined
    We add our own fields below.
    """
    email = models.EmailField(unique=True)   # Override to make email unique
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Make email the login field instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Still required for createsuperuser

    def __str__(self):
        return self.email


class Address(models.Model):
    """Shipping/billing addresses belonging to a user."""
    ADDRESS_TYPES = [
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='shipping')
    full_name = models.CharField(max_length=100)
    street_line1 = models.CharField(max_length=255)
    street_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} — {self.city}, {self.country}"
```

---

### `products/models.py` — Category, Product, ProductImage

```python
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Product categories (e.g., Electronics, Clothing).
    Supports sub-categories via the parent field (self-referential).
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)            # URL-friendly name: "electronics"
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey(
        'self',                                     # Points to itself = sub-category
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Main product table."""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='products'
    )
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)    # Stock Keeping Unit
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        """Return discount price if available, otherwise regular price."""
        return self.discount_price if self.discount_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """A product can have multiple images."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"
```

---

### `cart/models.py` — Cart & CartItem

```python
from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """
    Each logged-in user gets one cart.
    OneToOneField means: one user = one cart (not multiple).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        """Sum up all items in the cart."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    """One row per product in the cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')   # Can't add same product twice

    @property
    def subtotal(self):
        return self.product.effective_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
```

---

### `orders/models.py` — Order, OrderItem, Payment

```python
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """
    Represents a placed order. Once placed, it goes through
    these statuses in sequence.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),           # Just placed
        ('confirmed', 'Confirmed'),       # Payment received
        ('processing', 'Processing'),     # Being prepared
        ('shipped', 'Shipped'),           # On its way
        ('delivered', 'Delivered'),       # Received by customer
        ('cancelled', 'Cancelled'),       # Cancelled
        ('refunded', 'Refunded'),         # Money returned
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Snapshot of address at time of order (address may change later)
    shipping_address = models.JSONField()

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    """Each product line in an order — snapshot of price at purchase time."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)    # Snapshot: product name may change
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Snapshot: price may change
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class Payment(models.Model):
    """Payment record linked to an order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True)  # From Stripe/PayPal
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} — {self.status}"
```

---

### `reviews/models.py` — Product Review

```python
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product


class Review(models.Model):
    """Customer review for a product. One review per user per product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')    # One review per product per user
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.product.name} ({self.rating}★)"
```

---

## 6️⃣ Serializers (Convert Models ↔ JSON)

> 💡 **What is a Serializer?** It converts your Python model instances into JSON (for API responses) and validates JSON coming IN (for API requests).

---

### `users/serializers.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Address

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        """Check that both passwords match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        # Use create_user so password gets hashed (never store plain text!)
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Used to display/update user profile."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'avatar']
        read_only_fields = ['id', 'email']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']
```

---

### `products/serializers.py`

```python
from rest_framework import serializers
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product lists (less data = faster response)."""
    primary_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'discount_price',
            'effective_price', 'in_stock', 'category_name', 'primary_image'
        ]

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image:
            request = self.context.get('request')
            return request.build_absolute_uri(image.image.url) if request else image.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full details for a single product page."""
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'discount_price',
            'effective_price', 'stock', 'in_stock', 'sku', 'category',
            'images', 'average_rating', 'review_count', 'created_at'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def get_review_count(self, obj):
        return obj.reviews.count()
```

---

### `cart/serializers.py`

```python
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'subtotal']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'updated_at']
```

---

### `orders/serializers.py`

```python
from rest_framework import serializers
from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'unit_price', 'quantity', 'subtotal']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method', 'status', 'transaction_id', 'amount', 'paid_at']
        read_only_fields = ['status', 'paid_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_amount', 'shipping_address',
            'notes', 'items', 'payment', 'created_at'
        ]
        read_only_fields = ['status', 'total_amount']


class PlaceOrderSerializer(serializers.Serializer):
    """
    Used ONLY when placing a new order.
    Validates the input before we process the cart.
    """
    shipping_address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=[
        'credit_card', 'paypal', 'stripe', 'bank_transfer'
    ])
    notes = serializers.CharField(required=False, allow_blank=True)
```

---

### `reviews/serializers.py`

```python
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'title', 'body', 'created_at']
        read_only_fields = ['user', 'created_at']
```

---

## 7️⃣ Authentication — How It Works

We use **JWT (JSON Web Tokens)**. Here's the flow:

```
1. User registers → POST /api/auth/register/
2. User logs in   → POST /api/auth/login/
                     ← Server returns: { access: "...", refresh: "..." }
3. User makes any request:
   → Adds header: Authorization: Bearer <access_token>
4. Access token expires after 1 hour
   → User calls POST /api/auth/token/refresh/ with refresh token
   ← Gets new access token
5. User logs out → POST /api/auth/logout/ (blacklists refresh token)
```

---

### `users/views.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer
from .models import Address

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — Anyone can register."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # No auth needed to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Auto-generate JWT tokens on registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """POST /api/auth/logout/ — Blacklist the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()       # Makes this token unusable
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/profile/ — View and update own profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user   # Always returns the logged-in user


class AddressListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/auth/addresses/ — List or add addresses."""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/auth/addresses/<id>/ — Manage a single address."""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
```

---

### `users/urls.py`

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),       # Built-in JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('addresses/', views.AddressListCreateView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
]
```

---

## 8️⃣ Product Views & Filters

### `products/filters.py`

```python
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
```

### `products/views.py`

```python
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter


class CategoryListView(generics.ListAPIView):
    """GET /api/products/categories/ — List all categories."""
    queryset = Category.objects.filter(parent=None)   # Top-level only
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Supports: ?search=laptop&category=1&min_price=100&max_price=500&ordering=price
    """
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/products/<slug>/ — Single product full details."""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'   # Use slug in URL instead of ID
```

### `products/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
]
```

---

## 9️⃣ Cart Views

### `cart/views.py`

```python
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


def get_or_create_cart(user):
    """Helper: get user's cart or create it if it doesn't exist."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    """GET /api/cart/ — View the current user's cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemView(APIView):
    """POST /api/cart/items/ — Add or update item in cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        # Validate product exists
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check stock
        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} items available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity   # Add to existing quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        """DELETE /api/cart/items/<item_id>/ — Remove item from cart."""
        cart = get_or_create_cart(request.user)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            return Response({'message': 'Item removed.'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        """PATCH /api/cart/items/<item_id>/ — Update quantity."""
        cart = get_or_create_cart(request.user)
        quantity = request.data.get('quantity')

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        if int(quantity) < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)
```

### `cart/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('items/', views.CartItemView.as_view(), name='cart-add-item'),
    path('items/<int:item_id>/', views.CartItemView.as_view(), name='cart-item-detail'),
]
```

---

## 🔟 Order Views (Checkout Logic)

### `orders/views.py`

```python
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PlaceOrderSerializer
from cart.models import Cart
from users.models import Address


class PlaceOrderView(APIView):
    """
    POST /api/orders/
    This is the checkout endpoint. It:
    1. Validates the cart isn't empty
    2. Validates the shipping address exists
    3. Creates an Order from the cart contents
    4. Creates OrderItems (with price snapshots)
    5. Creates a Payment record
    6. Clears the cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate address belongs to this user
        try:
            address = Address.objects.get(
                id=serializer.validated_data['shipping_address_id'],
                user=request.user
            )
        except Address.DoesNotExist:
            return Response({'error': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check all items are still in stock
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'"{item.product.name}" has only {item.product.stock} items in stock.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address={   # Snapshot: save address as JSON
                'full_name': address.full_name,
                'street_line1': address.street_line1,
                'street_line2': address.street_line2,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country,
            },
            notes=serializer.validated_data.get('notes', '')
        )

        # Create order items & reduce stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.effective_price,
                quantity=item.quantity,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Create payment record
        Payment.objects.create(
            order=order,
            method=serializer.validated_data['payment_method'],
            amount=order.total_amount,
        )

        # Clear the cart
        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


class OrderListView(generics.ListAPIView):
    """GET /api/orders/ — List logged-in user's orders."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=request.user).prefetch_related('items', 'payment')


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/<id>/ — Single order details."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
```

### `orders/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlaceOrderView.as_view(), name='place-order'),
    path('list/', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]
```

---

## 1️⃣1️⃣ Reviews Views

### `reviews/views.py`

```python
from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer


class ProductReviewListView(generics.ListCreateAPIView):
    """
    GET  /api/reviews/?product=<id> — List reviews for a product
    POST /api/reviews/              — Submit a review (must be logged in)
    """
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return Review.objects.filter(product_id=product_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/reviews/<id>/ — Manage own review."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)  # Can only edit own reviews
```

### `reviews/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductReviewListView.as_view(), name='review-list'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
```

---

## 1️⃣2️⃣ Admin Registration

Register all models in admin so you can manage them at `/admin/`.

### `products/admin.py`

```python
from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'sku']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}    # Auto-fill slug from name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
```

### `orders/admin.py`

```python
from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]


admin.site.register(Payment)
```

### `users/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

admin.site.register(User, UserAdmin)
admin.site.register(Address)
```

---

## 1️⃣3️⃣ Root URL Configuration

### `core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/auth/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 1️⃣4️⃣ Run Migrations & Start the Server

```bash
# Step 1: Create migration files (Django reads your models and creates SQL)
python manage.py makemigrations

# Step 2: Apply migrations (actually create the tables in the database)
python manage.py migrate

# Step 3: Create an admin user so you can access /admin/
python manage.py createsuperuser
# Enter: email, username, password

# Step 4: Start the development server
python manage.py runserver

# Server is now running at: http://127.0.0.1:8000/
# Admin panel at: http://127.0.0.1:8000/admin/
```

---

## 1️⃣5️⃣ Complete API Endpoint Reference

| Method | Endpoint | Auth? | Description |
|--------|----------|-------|-------------|
| POST | `/api/auth/register/` | ❌ | Register new user |
| POST | `/api/auth/login/` | ❌ | Login, get JWT tokens |
| POST | `/api/auth/token/refresh/` | ❌ | Refresh access token |
| POST | `/api/auth/logout/` | ✅ | Logout (blacklist token) |
| GET/PATCH | `/api/auth/profile/` | ✅ | View/update profile |
| GET/POST | `/api/auth/addresses/` | ✅ | List/add addresses |
| GET/PATCH/DELETE | `/api/auth/addresses/<id>/` | ✅ | Manage address |
| GET | `/api/products/` | ❌ | List products (filterable) |
| GET | `/api/products/<slug>/` | ❌ | Product details |
| GET | `/api/products/categories/` | ❌ | List categories |
| GET | `/api/cart/` | ✅ | View cart |
| POST | `/api/cart/items/` | ✅ | Add item to cart |
| PATCH | `/api/cart/items/<id>/` | ✅ | Update quantity |
| DELETE | `/api/cart/items/<id>/` | ✅ | Remove item |
| POST | `/api/orders/` | ✅ | Place order (checkout) |
| GET | `/api/orders/list/` | ✅ | My orders |
| GET | `/api/orders/<id>/` | ✅ | Order details |
| GET/POST | `/api/reviews/` | ❌/✅ | List/create reviews |
| GET/PATCH/DELETE | `/api/reviews/<id>/` | ✅ | Manage own review |

---

## 1️⃣6️⃣ Testing Your API (with curl or Postman)

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@test.com","password":"pass1234","password2":"pass1234"}'

# Login → copy the "access" token from response
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@test.com","password":"pass1234"}'

# Get products (no auth needed)
curl http://127.0.0.1:8000/api/products/

# View cart (replace TOKEN with your access token)
curl http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Bearer TOKEN"

# Add item to cart
curl -X POST http://127.0.0.1:8000/api/cart/items/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product": 1, "quantity": 2}'
```

---

## 1️⃣7️⃣ Common Beginner Mistakes to Avoid

1. **Never store passwords in plain text** — always use `create_user()`, never `create()`
2. **Never commit your `.env` file** — add it to `.gitignore`
3. **Always snapshot prices in OrderItem** — prices change; never recalculate from product
4. **Run `makemigrations` after every model change** — then `migrate`
5. **Use `select_related` and `prefetch_related`** in querysets that join tables to avoid N+1 query problems
6. **Always filter by `user=request.user`** when returning user-specific data
7. **Use `is_active=True`** filter on products so deleted/hidden products don't appear

---

## 1️⃣8️⃣ What To Build Next (Phase 2)

Once the above is working:

- 🔔 **Email notifications** — use `django-anymail` + SendGrid
- 💳 **Real payments** — integrate Stripe (`stripe` Python SDK)
- 🖼️ **Image optimization** — `django-imagekit`
- 📊 **Admin analytics** — order charts, revenue reports
- 🔍 **Better search** — `django-elasticsearch-dsl`
- 🚀 **Production deploy** — Switch SQLite → PostgreSQL, deploy to Railway or Render
- 🧪 **Tests** — write unit tests with `pytest-django`
- 📄 **API docs** — auto-generate with `drf-spectacular` (OpenAPI/Swagger)

---

## 📁 `.gitignore` File

```
venv/
__pycache__/
*.pyc
db.sqlite3
.env
media/
*.log
.DS_Store
```

---

*Happy coding! When in doubt: read the error message top to bottom, Google the last line of it.*