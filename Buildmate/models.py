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
    unit=models.CharField(max_length=50)
    price=models.FloatField(max_length=20)
    photo = models.FileField()
    brand=models.CharField(max_length=50)
    description=models.CharField(max_length=500)

class order_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    date = models.DateField(max_length=100)
    status = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class order_details_table(models.Model):
    ORDER = models.ForeignKey(order_table, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product_table, on_delete=models.CASCADE)
    Quantity = models.CharField(max_length=100)
    price=models.FloatField(max_length=200)



class offer_table(models.Model):
    PRODUCT = models.ForeignKey(product_table, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    Percentage=models.IntegerField(max_length=20)
    From_date=models.DateField()
    To_date=models.DateField()

class delivery_table(models.Model):
    ORDER = models.ForeignKey(order_table, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    houseNo = models.CharField(max_length=100)
    pin = models.IntegerField()
    phone = models.BigIntegerField()
    landMark = models.CharField(max_length=100)
    Address =models.CharField(max_length=500)



class Feedback(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product_table, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    feedback = models.CharField(max_length=20)
    Rating = models.FloatField()


class Complaints(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE,default='')
    complaints=models.CharField(max_length=400)
    date=models.DateField()
    reply=models.CharField(max_length=400)



class Complaints_product(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE,default='')
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE,default='')
    complaints=models.CharField(max_length=400)
    date=models.DateField()
    reply=models.CharField(max_length=400)