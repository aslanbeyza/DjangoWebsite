from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Color
from django.db.models import Q
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator #Paginator kütüphanesi
from django.contrib.auth.decorators import login_required



def ProductQuantity(request):
    if request.user.is_authenticated:
        return BasketProduct.objects.filter(user=request.user)
    else:
        return None
    

def index (request):
    products = Product.objects.all()
    comments = Comment.objects.all().order_by('-create_date')  # Yorumları en son tarihe göre sıralar

    context=  {
    "products" : products,
     "comments": comments,
    "productquantity":ProductQuantity(request)
    
    }
    
    return render(request, "index.html",context)

def category(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    genders = Gender.objects.all()
    colors = Color.objects.all()
    materials = Material.objects.all()
    gemstones = Gemstone.objects.all()
    categories = Category.objects.all()
    styles = Style.objects.all()

    filters = Q()  # Filtreler burada birikiyor.

    # Marka filtresi
    if "marka" in request.GET:
        markalar = request.GET.getlist("marka")
        if markalar:
            filters &= Q(brand__in=markalar)

    # Materyal filtresi
    if "materyal" in request.GET:
        materyaller = request.GET.getlist("materyal")
        if materyaller:
            filters &= Q(material__in=materyaller)

    # Değerli taş filtresi
    if "degerli_tas" in request.GET:
        degerli_taslar = request.GET.getlist("degerli_tas")
        if degerli_taslar:
            filters &= Q(gemstone__in=degerli_taslar)

    # Tarz filtresi
    if "tarz" in request.GET:
        tarzlar = request.GET.getlist("tarz")
        if tarzlar:
            filters &= Q(style__in=tarzlar)

    # Fiyat filtresi
    if "fiyat_min" in request.GET and "fiyat_max" in request.GET:
        fiyat_min = request.GET.get("fiyat_min")
        fiyat_max = request.GET.get("fiyat_max")
        fiyat_min = float(fiyat_min) if fiyat_min else None
        fiyat_max = float(fiyat_max) if fiyat_max else None

        if fiyat_min is not None:
            filters &= Q(price__gte=fiyat_min)
        if fiyat_max is not None:
            filters &= Q(price__lte=fiyat_max)

    # Filtrelenmiş ürünleri getir
    products = Product.objects.filter(filters)

    # Paginator ekliyoruz
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    # Sepete ekleme işlemi
    if request.method == "POST":
        productid = request.POST.get("product_id")
        product = Product.objects.get(id=productid)

        if BasketProduct.objects.filter(product=product, user=request.user).exists():
            basket_product = BasketProduct.objects.get(product=product, user=request.user)
            basket_product.quantity += 1
            basket_product.save()
        else:
            basketproduct = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
            basketproduct.save()
            return redirect("category")

    context = {
        "products": products,
        "brands": brands,
        "genders": genders,
        "materials": materials,
        "gemstones": gemstones,
        "categories": categories,
        "styles": styles,
        "color": colors,
        "productquantity": ProductQuantity(request),
    }

    return render(request, "category.html",context)

def basket(request):
    # Kullanıcıya ait ürünleri getir
    basket_products = BasketProduct.objects.filter(user=request.user)

    # Toplam fiyat hesaplama
    kargo = 29.99
    product_total_price = sum(product.product.price * product.quantity for product in basket_products)
    total_price = kargo + product_total_price

    if request.method == "POST":
        # Sepeti onaylama işlemi
        if request.POST.get("btncheck") == "checkbtn":
            messages.success(request, "Ödeme Alındı. Teşekkür Ederiz!")
            return redirect("basket")  # Sayfayı yenile

        # Ürün işlemleri (artırma, azaltma, silme)
        product_id = request.POST.get("product_id")  # POST verisinden product_id al
        action = request.POST.get("action")  # POST verisinden action al

        # Eğer `product_id` varsa işlem yap
        if product_id:
            basket_product = get_object_or_404(BasketProduct, id=product_id, user=request.user)

            if action == "delete":  # Ürünü tamamen sil
                basket_product.delete()
            elif action == "increase":  # Ürün miktarını artır
                basket_product.quantity += 1
                basket_product.save()
            elif action == "decrease":  # Ürün miktarını azalt
                if basket_product.quantity > 1:
                    basket_product.quantity -= 1
                    basket_product.save()
                else:
                    basket_product.delete()  # Miktar 1'e düşerse ürünü sil

        return redirect("basket")  # İşlemden sonra sepet sayfasına yönlendir

    context = {
        "basket_products": basket_products,
        "product_total_price": product_total_price,
        "total_price": total_price,
        "kargo": kargo,
        "productquantity": ProductQuantity(request),
    }

    return render(request, "basket.html", context)

@login_required(login_url='/login/')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product)
    comment_user = None

    # Kullanıcı daha önce yorum yapmış mı kontrol et
    for comment in comments:
            if comment.user == request.user:
                comment_user = comment.user

    if request.method == "POST":
            if request.POST.get("submit") == "btnbasket":
                productid = request.POST.get("productid")
                quantity = int(request.POST.get("quantity", 1))  # Varsayılan olarak 1 al
                product = Product.objects.get(id=productid)

                # Sepette ürün varsa miktarı artır
                if BasketProduct.objects.filter(product=product, user=request.user).exists():
                    basket_product = BasketProduct.objects.get(product=product, user=request.user)
                    basket_product.quantity += quantity
                    basket_product.save()
                else:
                    # Yeni ürün ekle
                    basketproduct = BasketProduct.objects.create(
                        user=request.user, product=product, quantity=quantity
                    )
                    basketproduct.save()
                return redirect(f"/product-detail/{product_id}")


            elif request.POST.get("submit") == "btncomment":
                # Yeni yorum ekleme işlemi
                comment = request.POST.get("comment")

                new_comment = Comment.objects.create(
                    user=request.user,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    product=product,
                    comment=comment
                )
                new_comment.save()
                return redirect(f"/product-detail/{product_id}")

            elif request.POST.get("submit") == "commentupdate":
                # Mevcut yorumu güncelleme işlemi
                comment_id = request.POST.get("comment_id")
                comment = request.POST.get("comment")

                update_comment = Comment.objects.get(id=comment_id, user=request.user)
                update_comment.comment = comment
                update_comment.save()
                return redirect(f"/product-detail/{product_id}")

            context = {
            "product": product,
            "comments": comments,
            "comment_user": comment_user,
            "productquantity": ProductQuantity(request)
        }

            return render(request, "product_detail.html",context)
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product)
    comment_user = None

    # Kullanıcı daha önce yorum yapmış mı kontrol et
    for comment in comments:
        if comment.user == request.user:
            comment_user = comment.user

    if request.method == "POST":
        if request.POST.get("submit") == "btnbasket":
            # Sepete ekleme işlemi
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)

            if BasketProduct.objects.filter(product=product, user=request.user).exists():
                basket_product = BasketProduct.objects.get(product=product, user=request.user)
                basket_product.quantity += 1
                basket_product.save()
            else:
                basketproduct = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basketproduct.save()
                return redirect(f"/product-detail/{product_id}")

        elif request.POST.get("submit") == "btncomment":
            # Yeni yorum ekleme işlemi
            comment = request.POST.get("comment")

            new_comment = Comment.objects.create(
                user=request.user,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                product=product,
                comment=comment
            )
            new_comment.save()
            return redirect(f"/product-detail/{product_id}")

        elif request.POST.get("submit") == "commentupdate":
            # Mevcut yorumu güncelleme işlemi
            comment_id = request.POST.get("comment_id")
            comment = request.POST.get("comment")

            update_comment = Comment.objects.get(id=comment_id, user=request.user)
            update_comment.comment = comment
            update_comment.save()
            return redirect(f"/product-detail/{product_id}")

    context = {
        "product": product,
        "comments": comments,
        "comment_user": comment_user,
        "productquantity": ProductQuantity(request)
    }

    return render(request, "product_detail.html", context)


def profil (request):
    profil = Profil.objects.get(user=request.user) #Bu ikisi eklendi
    adres = Adres.objects.get(user=request.user)

    context = {
        "profil": profil, #bunlar eklendi
        "adres": adres,
        "productquantity": ProductQuantity(request)
    }

    return render(request, "user/profil.html",context)


def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Kullanıcıyı e-posta adresi ile kontrol et
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)  # Kullanıcı nesnesini al
            if user.check_password(password):  # Şifreyi kontrol et
                if user is not None:  # Kullanıcı nesnesi mevcutsa giriş yap
                    login(request, user)
                    return redirect("index")
            else:
                messages.error(request, "Şifreniz Hatalıdır. Lütfen tekrar deneyiniz")
        else:
            messages.error(request, "E-Postanız Hatalıdır. Lütfen tekrar deneyiniz")    

    return render(request, "user/login.html")



def Register(request):
    if request.method == "POST":
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():  # Email zaten var mı kontrolü
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)  # Şifreyi hashle
            user.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Bu eposta adresi başka kullanıcı tarafından kullanılıyor.")
    return render(request, "user/register.html")



def Logout (request):
    logout(request)
    return redirect('index')



def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response