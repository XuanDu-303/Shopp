import csv
import pickle
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from . models import Category, Customer, OrderPlaced, Product, Cart, Wishlist, Review
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg
from django.http import HttpResponse
from .knn_model import recommend_products

def home(request):
    products = Product.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user_item_matrix_file = 'D:/XuanDu/DaiHoc/Django/ProjectCuoiKi/Ecommerce/ec/Notebooks/user_item_matrix.pkl'
        
        # Tải dữ liệu từ tệp pickle
        with open(user_item_matrix_file, 'rb') as f:
            user_item_matrix = pickle.load(f)
        
        # Lấy user_id của người dùng hiện tại
        user_id = request.user.id
        # Đề xuất sản phẩm cho người dùng hiện tại
        recommended_products = recommend_products(6, user_item_matrix)
        print(recommended_products)
        # Trả về trang web hiển thị danh sách sản phẩm được đề xuất
        return render(request, "app/home.html", locals())

    return render(request, "app/home.html", locals())

@login_required
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())

@method_decorator(login_required, name="dispatch")
class CategoryView(ListView):
    template_name = 'app/category.html'  # Tên template để hiển thị danh sách sản phẩm
    context_object_name = 'products'  # Tên biến context chứa danh sách sản phẩm

    def get_queryset(self):
        val = self.kwargs['val']  # Lấy giá trị slug từ URL
        return Product.objects.filter(category__name=val)  # Lấy danh sách sản phẩm của danh mục val

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['val']  # Truyền tên danh mục vào context để sử dụng trong template
        context['totalitem'] = len(Cart.objects.filter(user=self.request.user)) if self.request.user.is_authenticated else 0
        return context

@method_decorator(login_required, name="dispatch")
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name="dispatch")
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = None
        totalitem = 0

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            totalitem = Cart.objects.filter(user=request.user).count()

        # Tính toán thông tin đánh giá trung bình và số lượng đánh giá
        reviews = Review.objects.filter(product=product)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        num_reviews = reviews.count()

        return render(request, "app/product_detail.html", {
            'product': product,
            'wishlist': wishlist,
            'totalitem': totalitem,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'num_reviews': num_reviews,
        })

# @method_decorator(login_required, name="dispatch")
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()  # Initialize form object
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)  # Initialize form object
        if form.is_valid():
            form.save()
            messages.success(request, "Chúc mừng! Người dùng đã đăng ký thành công")
        else:   
            messages.warning(request, "Dữ liệu đầu vào không hợp lệ")
        return render(request, 'app/customerregistration.html',  locals())
    
@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile Save successfully')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', {'form': form, 'add': add})

    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, "Chúc mừng! Hồ sơ đã được cập nhật thành công")
            return redirect("address")
        else:
            messages.warning(request, "Dữ liệu đầu vào không hợp lệ")
            return redirect("address")

@method_decorator(login_required, name="dispatch")
class Checkout(View):
    def get(self, request):
        users = Customer.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/checkout.html', {'users': users, 'cart_items': cart_items, 'totalamount': totalamount})
    
    def post(self, request):
        if request.method == 'POST' and request.user.is_authenticated:
            # Lấy thông tin sản phẩm từ POST request
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            totamount = request.POST.get('totamount')
            
            current_user = request.user

            # Tìm kiếm thông tin Customer tương ứng với User
            customer = get_object_or_404(Customer, user=current_user)
            print("Product ID:", product_id)
            print("Quantity:", quantity)
            print("Totamount:", totamount)
            # Kiểm tra xem thông tin sản phẩm và số lượng có hợp lệ không 
            if product_id and quantity:
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                except Product.DoesNotExist:
                    # Xử lý khi sản phẩm không tồn tại
                    return redirect('home')  # Điều hướng về trang chủ hoặc trang thông báo lỗi

                # Tạo đơn hàng và cập nhật trạng thái
                order = OrderPlaced.objects.create(
                    user=request.user,
                    customer=request.user.customer,
                    product=product,
                    quantity=quantity,
                    status='Đã Chấp Nhận'  # Cập nhật trạng thái
                )
                # Cập nhật số lượng sản phẩm sau khi đặt hàng
                product.quantity -= quantity
                product.save()
                
                # Xóa các sản phẩm trong giỏ hàng sau khi đặt hàng
                user = request.user
                Cart.objects.filter(user=user).delete()
                # Redirect hoặc render trang thành công
                return redirect('orders')  # Điều hướng đến trang đơn hàng hoặc trang thành công

        # Xử lý khi không phải POST request hoặc người dùng không đăng nhập
        return redirect('home')  # Điều hướng về trang chủ hoặc trang thông báo lỗi

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    # Kiểm tra xem người dùng đã có địa chỉ chưa
    customer = Customer.objects.filter(user=user)
    if not customer:
        messages.warning(request, "Vui lòng thêm địa chỉ giao hàng trước khi đặt hàng.")
    
    return render(request, 'app/addtocart.html', {
        'cart': cart,
        'amount': amount,
        'totalamount': totalamount,
        'totalitem': totalitem,
        'customer_exists': bool(customer),
    })

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        carts = Cart.objects.filter(Q(product=prod_id) & Q(user=user))
        
        # Lấy hoặc tạo mới một giỏ hàng nếu không tồn tại
        if carts.exists():
            cart = carts.first()
        else:
            cart = Cart.objects.create(user=user, product_id=prod_id, quantity=1)
        
        cart.quantity += 1
        cart.save()
        
        # Tính toán lại thông tin giỏ hàng
        cart.refresh_from_db()  # Cập nhật thông tin từ cơ sở dữ liệu
        cart_total = cart.quantity * cart.product.discounted_price
        total_amount = cart_total + 40  # Tổng giá hàng + phí vận chuyển
        
        data = {
            'quantity': cart.quantity,
            'amount': cart_total,
            'totalamount': total_amount
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid Request'})

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        carts = Cart.objects.filter(Q(product=prod_id) & Q(user=user))
        
        # Lấy hoặc tạo mới một giỏ hàng nếu không tồn tại
        if carts.exists():
            cart = carts.first()
        else:
            cart = Cart.objects.create(user=user, product_id=prod_id, quantity=1)
        
        cart.quantity -= 1
        cart.save()
        
        # Tính toán lại thông tin giỏ hàng
        cart.refresh_from_db()  # Cập nhật thông tin từ cơ sở dữ liệu
        cart_total = cart.quantity * cart.product.discounted_price
        total_amount = cart_total + 40  # Tổng giá hàng + phí vận chuyển
        
        data = {
            'quantity': cart.quantity,
            'amount': cart_total,
            'totalamount': total_amount
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ'})
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))
            for cart_item in cart_items:
                cart_item.delete()
        except Cart.DoesNotExist:
            pass
        
        # Tính toán lại tổng giá trị của giỏ hàng sau khi xóa
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for item in cart_items:
            value = item.quantity * item.product.discounted_price
            amount += value
        total_amount = amount + 40
        
        data = {
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'yêu cầu không hợp lệ'})

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html', locals())
    
@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # Xử lý query để loại bỏ khoảng trắng ở cả hai đầu
    query = query.strip() if query else ''
    # Tìm kiếm không phân biệt chữ thường và chữ hoa
    products = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())
    

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Danh sách yêu thích đã được thêm thành công',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Danh sách yêu thích đã được xóa thành công',
        }
        return JsonResponse(data)
    

@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    existing_review = Review.objects.filter(product=product, user=user).first()
    if existing_review:
        return HttpResponse("Bạn đã đánh giá sản phẩm này rồi.")
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review = Review.objects.create(product=product, user=user, rating=rating, comment=comment)
        review.save()
        return redirect('product_detail', pk=product_id)
    return redirect('product_detail', pk=product_id)
    

def export_reviews_to_csv(request):
    reviews = Review.objects.all()  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ratings.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['user', 'product', 'rating', 'timestamp'])

    for review in reviews:
        writer.writerow([review.user.id, review.product.id, review.rating, review.created_at])

    return response


with open('D:/XuanDu/DaiHoc/Django/ProjectCuoiKi/Ecommerce/ec/Notebooks/user_item_matrix.pkl', 'rb') as f:
    user_item_matrix = pickle.load(f)


# def recommend_products_for_user(user_id, user_item_matrix, recommendation_model, top_n=10):
#     # Lấy chỉ mục của người dùng trong ma trận người dùng-sản phẩm
#     user_index = user_item_matrix.index.get_loc(user_id)
#     # Lấy đánh giá của người dùng cho tất cả các sản phẩm
#     user_ratings = user_item_matrix.iloc[user_index]
#     # Lấy danh sách các sản phẩm chưa được người dùng đánh giá (có giá trị là 0)
#     unrated_products = user_ratings[user_ratings == 0].index.tolist()
    
#     # Tạo danh sách đề xuất sản phẩm
#     recommendations = []
#     for item_id in unrated_products:
#         # Dự đoán đánh giá của người dùng cho sản phẩm này
#         predicted_rating = recommendation_model.predict(user_id, item_id)
#         # Thêm sản phẩm và điểm dự đoán vào danh sách đề xuất
#         recommendations.append((item_id, predicted_rating.est))
    
#     # Sắp xếp danh sách đề xuất theo điểm dự đoán giảm dần và chọn top_n sản phẩm
#     recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]
#     return recommendations

# def main():
#     with open('D:/XuanDu/DaiHoc/Django/ProjectCuoiKi/Ecommerce/ec/Notebooks/recommendation_model.pkl', 'rb') as f:
#         recommendation_model = pickle.load(f)
#         return recommendation_model

# if __name__ == "__main__":
#     main()