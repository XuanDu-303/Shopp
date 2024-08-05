from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('An Giang', 'An Giang'),
    ('Bà Rịa-Vũng Tàu', 'Bà Rịa-Vũng Tàu'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Định', 'Bình Định'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Nội', 'Hà Nội'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hồ Chí Minh', 'Hồ Chí Minh'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên-Huế', 'Thừa Thiên-Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
)

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'categories'

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    brand = models.TextField(default='')
    product_image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Chấp nhận', 'Chấp nhận'),
    ('Đóng gói', 'Đóng gói'),
    ('Đang giao hàng', 'Đang giao hàng'),
    ('Đã giao hàng', 'Đã giao hàng'),
    ('Hủy', 'Hủy'),
    ('Chờ xử lý', 'Chờ xử lý'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Chờ xử lý')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"Order ID: {self.id}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.rating} stars"