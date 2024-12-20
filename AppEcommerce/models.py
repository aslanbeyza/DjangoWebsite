from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    brand = models.CharField(max_length=250)
    image = models.ImageField(upload_to="Brand Image")

    def __str__(self):
        return self.brand
    
    # class Meta:
    #     verbose_name_plural = "Markalar"




class Gender(models.Model):
    gender = models.CharField(max_length=250)

    def __str__(self):
        return self.gender
    
    # class Meta:
    #     verbose_name_plural = "Cinsiyetler"



class Material(models.Model):
    material = models.CharField(max_length=250)

    def __str__(self):
        return self.material
    
    # class Meta:
    #     verbose_name_plural = "Malzemeler"



class Gemstone(models.Model):
    gemstone = models.CharField(max_length=250)

    def __str__(self):
        return self.gemstone

    # class Meta:
    #     verbose_name_plural = "Değerli Taşlar"



class Category(models.Model):
    category = models.CharField(max_length=250)

    def __str__(self):
        return self.category
    
        # class Meta:
        # verbose_name_plural = "Kategoriler"
 


class Style(models.Model):
    style = models.CharField(max_length=250)

    def __str__(self):
        return self.style
    
    # class Meta:
    #     verbose_name_plural = "Stiller"
class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=250)  # Takı model veya adı
    description = models.TextField()
    image = models.ImageField(upload_to="ProductImage")
    price = models.FloatField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    gemstone = models.ForeignKey(Gemstone, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.model

    # class Meta:
    #     verbose_name_plural = "Ürünler"

class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Pozitif değerler ve varsayılan 1

    class Meta:
        unique_together = ('user', 'product')  # Aynı kullanıcı-ürün kombinasyonuna izin verme

    def _str_(self):
        return f"{self.user.username} - {self.product.model} ({self.quantity} adet)"
        
# Profil için eklenen classlar -> makemigraionts ve migrate yapılmalı
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, null = True, blank=True)
    birtdate = models.DateField(null = True, blank=True)

    def _str_(self):
        return self.user.username

class Adres(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    adress = models.TextField()
    il_province = models.CharField(max_length=100, null = True, blank=True)
    ilce_district = models.CharField(max_length=100, null = True, blank=True)
    mahalle_neighbour = models.CharField(max_length=100, null = True, blank=True)   

    def _str_(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Yorumlar"