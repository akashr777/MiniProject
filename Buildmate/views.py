from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from Buildmate.models import *

# Create your views here.
def  home(request):
    return render(request,"index.html")

def login(request):
    return render(request,"loginindex.html")

def logincode(request):
    print(request.POST)
    username=request.POST['mail']
    pwd=request.POST['Password']
    ob=login_table.objects.filter(username=username,password=pwd)
    if ob.exists():
        try:
            ob1 = login_table.objects.get(username=username, password=pwd)
            request.session['lid']=ob1.id
            if ob1.type == 'admin':
                return redirect('/adminhome')
            elif ob1.type == 'user':
                return redirect('/userhome')
            elif ob1.type == 'seller':
                request.session['lid'] = ob1.id
                return redirect('/Sellerhome')

            else:
                return redirect('/login')
        except:
            return redirect('/login')

    else:
        # return HttpResponse('''<script>alert("Invalid Username and Password");window.location='/login'</script>''')
        error_message = "Invalid Username or Password"
        return render(request, 'loginindex.html', {'error_message': error_message})





def adminhome(request):
    return render(request,"admin/ADMINHOMEINDEX.html")

def managecategory(request):
    ob=category_table.objects.all()
    return render(request,'admin/Category.html',{"val":ob})


def deletecategory(request,id):
    ob = category_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>window.location='/managecategory'</script>''')

def Sellerhome(request):
    return render(request,'Sellerhome.html')




def Addcategory(request):
    return render(request,'admin/AddCategory.html')

def Addcategorypost(request):
    try:
        name = request.POST["name"]
        details = request.POST["details"]
        ob=category_table()
        ob.category=name
        ob.details=details
        ob.save()
        return HttpResponse('''<script>window.location='/managecategory'</script>''')
    except:
        return render(request, 'admin/AddCategory.html',{"c":name,"d":details,"s":"0"})



def viewuser(request):
    ob=user_table.objects.all()
    return render(request,"admin/view user.html",{"val":ob})

def viewuserSearch(request):
    name=request.POST['textfield']
    ob=user_table.objects.filter(name__icontains=name)
    return render(request,"admin/view user.html",{"val":ob})

def manageseller(request):
    ob=seller_table.objects.all()
    return render(request,"admin/manageseller.html",{"val":ob})

def sellerSearch(request):
    name=request.POST['textfield']
    ob=seller_table.objects.filter(name__icontains=name)
    return render(request,"admin/manageseller.html",{"val":ob})


def addseller(request):
    return render(request,"admin/AddSeller.html")

def addsellerCode(request):
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    passw = request.POST["pass"]
    status = request.POST["status"]
    image = request.FILES["file"]
    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    ob=login_table()
    ob.username=email
    ob.password=passw
    ob.type="seller"
    ob.save()
    ob1=seller_table()
    ob1.name=name
    ob1.phone=phone
    ob1.email=email
    ob1.photo=fsave
    ob1.status=status
    ob1.LOGINID=ob
    ob1.save()
    return redirect('/manageseller')




def EditSeller(request,id):
    request.session['sid']=id
    return redirect('/EditSeller1')

def EditSeller1(request):
    ob=seller_table.objects.get(id=request.session['sid'])
    return render(request,"admin/EditSeller.html",{"val":ob})

def editsellerCode(request):
    try:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        status = request.POST["status"]
        image = request.FILES["file"]
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)
        ob1=seller_table.objects.get(id= request.session['sid'])
        ob1.name=name
        ob1.phone=phone
        ob1.email=email
        ob1.photo=fsave
        ob1.status=status
        ob1.save()
        return HttpResponse('''<script>window.location='/manageSeller'</script>''')
    except:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        status = request.POST["status"]
        ob1 = seller_table.objects.get(id=request.session['sid'])
        ob1.name = name
        ob1.phone = phone
        ob1.email = email
        ob1.status = status
        ob1.save()
        return HttpResponse('''<script>window.location='/manageSeller'</script>''')

def deleteSeller(request,id):
    ob = seller_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>window.location='/manageSeller'</script>''')


def PrductList(request):
    ob1=category_table.objects.all()
    ob=product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'])
    return render(request,"Seller/ManageProduct.html",{"val":ob,"cat":ob1})


def delete_product(request,id):

    ob=product_table.objects.get(id=id)
    ob.delete()
    return redirect("/ProductList")


def edit_product(request,id):
    request.session['pid']=id
    ob1=category_table.objects.all()
    ob=product_table.objects.get(id=id)

    return render(request, "Seller/updateProduct.html", {"val": ob, "cat": ob1})


def ProductList_post(request):
    ob1=category_table.objects.all()
    cat=request.POST['cat']
    s=request.POST['s']
    if cat == 0:
        ob=product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'],name__startswith=s)
        return render(request,"Seller/ManageProduct.html",{"val":ob,"cat":ob1})
    else:
        ob = product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'], name__startswith=s,CATEGORY__id=cat)
        return render(request, "Seller/ManageProduct.html", {"val": ob, "cat": ob1,"cc":int(cat),"s":s})


def AddPrduct(request):
    ob=category_table.objects.all()
    return render(request,"Seller/AddProduct.html",{"val":ob})


def AddProductpost(request):
    name = request.POST["name"]
    phone = request.POST["stock"]
    email = request.POST["price"]
    status = request.POST["select"]
    image = request.FILES["file"]
    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    ob1 = product_table.objects.filter(name__iexact = name,CATEGORY__id=status,SELLER__LOGINID__id=request.session['lid'])
    if len(ob1)>0:
        ob = category_table.objects.all()
        return render(request, "Seller/AddProduct.html", {"val": ob,"n":name,"s":phone,"p":email,"st":status,"f":"0"})

    ob1 = product_table()
    ob1.name = name
    ob1.stock = phone
    ob1.price = email
    ob1.photo = fsave
    ob1.CATEGORY = category_table.objects.get(id=status)
    ob1.SELLER = seller_table.objects.get(LOGINID__id=request.session['lid'])
    ob1.save()
    return redirect('/Sellerhome')


def UpdateProductpost(request):
    name = request.POST["name"]
    phone = request.POST["stock"]
    email = request.POST["price"]
    status = request.POST["select"]

    ob1 = product_table.objects.get(id=request.session['pid'])
    ob1.name = name
    ob1.stock = phone
    ob1.price = email
    if 'file' in request.FILES:
        image = request.FILES["file"]
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)
        ob1.photo = fsave
    ob1.CATEGORY = category_table.objects.get(id=status)
    ob1.SELLER = seller_table.objects.get(LOGINID__id=request.session['lid'])
    ob1.save()
    return redirect('/Sellerhome')


def sellerProfile(request):
    ob=seller_table.objects.get(LOGINID__id=request.session['lid'])
    return render(request,"Seller/sellerProfile.html",{'i':ob})
def sellerProfilecode(request):
    if "file" in request.FILES:
        name=request.POST['name']
        phone=request.POST['phone']
        photo=request.FILES['file']
        fn=FileSystemStorage()
        fs=fn.save(photo.name,photo)
        ob=seller_table.objects.get(LOGINID__id=request.session['lid'])
        ob.photo=fs
        ob.name=name
        ob.phone=phone
        ob.save()
        return redirect('/sellerProfile')
    else:
        name = request.POST['name']
        phone = request.POST['phone']
        ob = seller_table.objects.get(LOGINID__id=request.session['lid'])
        ob.name = name
        ob.phone = phone
        ob.save()
        return redirect('/sellerProfile')

# def userProfile(request):
#     ob=user_table.objects.get(LOGINID__id=request.session['lid'])
#     return render(request,"User/userProfile.html",{"i":ob})

def view_profile(request):
    ob=user_table.objects.get(LOGINID__id=request.session['lid'])
    return render(request,"User/view_profile.html",{"i":ob})

def edit(request):
    ob=user_table.objects.get(LOGINID__id=request.session['lid'])
    return render(request,"User/userProfile.html",{"i":ob})

def userProfilecode(request):
    if "file" in request.FILES:
        name=request.POST['name']
        phone=request.POST['phone']
        photo=request.FILES['file']
        fn=FileSystemStorage()
        fs=fn.save(photo.name,photo)
        ob=user_table.objects.get(LOGINID__id=request.session['lid'])
        ob.photo=fs
        ob.name=name
        ob.phone=phone
        ob.save()
        return redirect('/userProfile#profile')
    else:
        name = request.POST['name']
        phone = request.POST['phone']
        ob = user_table.objects.get(LOGINID__id=request.session['lid'])
        ob.name = name
        ob.phone = phone
        ob.save()
        return redirect('/userProfile#profile')






def userhome(request):
    return render(request,"homeindex.html")




def registration(request):
    return render(request,'registerindex.html')


def checkemail(request):
    # if request.method == 'GET':
    #     post_id = request.GET['post_id']
    #     likedpost = Post.objects.get(pk=post_id)  # getting the liked posts
    #     m = Like(post=likedpost)  # Creating Like Object
    #     m.save()  # saving it to store in database
    #     return HttpResponse("Success!")  # Sending an success response
    # else:
    #     return HttpResponse("Request method is not a GET")


    username  = request.GET['email']
    print(username)
    data = {
        'is_taken': login_table.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this email already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)


def registrationPost(request):
    name=request.POST["name"]
    phone=request.POST["phone"]
    email=request.POST["email"]
    image=request.FILES["file"]
    passw=request.POST["pass"]

    fs=FileSystemStorage()
    fsave=fs.save(image.name,image)

    lg=login_table()
    lg.username=email
    lg.password=passw
    lg.type="user"
    lg.save()

    kk=user_table()
    kk.name=name
    kk.phone=phone
    kk.email=email
    kk.photo=fsave
    kk.LOGINID=lg
    kk.save()
    return HttpResponse('''<script>window.location='/'</script>''')


def about(request):
    return render(request,"about.html")
def services(request):
    return render(request,"services.html")
def contact(request):
    return render(request,"contact.html")

def uvproducts(request):
    ob=product_table.objects.all()
    return render(request,"User/products.html",{"val":ob})


def view_product(request,id):
    request.session['pid']=id
    ob = product_table.objects.filter(id=id)
    return render(request,"User/view_product.html",{"val":ob})



def buy_now(request,id):
    request.session['pid']=id
    ob = product_table.objects.filter(id=id)
    return render(request,"User/buy_now.html",{"val":ob})


def buy_now_post(request):

    id=request.session['pid']
    obb = product_table.objects.get(id=id)

    qty=request.POST['qty']
    ob=order_table()
    ob.USER = user_table.objects.get(LOGINID__id=request.session['lid'])
    ob.date=datetime.today()
    ob.status='pending'
    ob.amount=int(obb.price)*int(qty)
    ob.save()
    ob1=order_details_table()
    ob1.ORDER = ob
    ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
    ob1.Quantity=qty
    ob1.price=int(obb.price)*int(qty)
    ob1.save()
    return redirect('/uvproducts#profile')





def view_cart(request):
    return render(request,"User/view_cart.html")



def add_to_cart(request,id):
    request.session['pid'] = id
    ob = product_table.objects.filter(id=id)
    return render(request, "User/add_to_cart.html", {"val": ob})
def add_to_cart_post(request):
    qty = request.POST['qty']
    id = request.session['pid']
    obb = product_table.objects.get(id=id)
    ob2 = order_table.objects.filter(status='cart', USER__LOGINID=request.session['lid'])
    if len(ob2) == 0:
        qty = request.POST['qty']
        ob = order_table()
        ob.USER = user_table.objects.get(LOGINID__id=request.session['lid'])
        ob.date = datetime.today()
        ob.status = 'cart'
        ob.amount = 0
        ob.save()
        ob1 = order_details_table()
        ob1.ORDER = ob
        ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
        ob1.Quantity = qty
        ob1.price = int(obb.price) * int(qty)
        ob1.save()
        ob.amount = int(obb.price) * int(qty)
        ob.save()
        return redirect('/uvproducts#profile')


    else:
        ob = order_table.objects.get(status='pending', USER__LOGINID=request.session['lid'])
        ob1 = order_details_table()
        ob1.ORDER = ob
        ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
        ob1.Quantity = qty
        ob1.price = int(obb.price) * int(qty)
        ob1.save()
        ob.amount += (int(obb.price) * int(qty))
        ob.save()
        return redirect('/uvproducts#profile')



