from django.db import models

# Create your models here.



class login_table(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    type=models.CharField(max_length=20)


class user_table(models.Model):
    LOGINID = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    photo=models.FileField()

class seller_table(models.Model):
    LOGINID = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    photo = models.FileField()

class category_table(models.Model):

    category = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

class product_table(models.Model):
    SELLER = models.ForeignKey(seller_table, on_delete=models.CASCADE)
    CATEGORY = models.ForeignKey(category_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stock=models.IntegerField(max_length=20)
    price=models.IntegerField(max_length=20)
    photo = models.FileField()

class order_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class order_details_table(models.Model):
    ORDER = models.ForeignKey(order_table, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product_table, on_delete=models.CASCADE)
    Quantity = models.CharField(max_length=100)
    price=models.IntegerField(max_length=20)


