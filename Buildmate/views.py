from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from Buildmate.models import *

# # Create your views here.
def  newindex(request):
    return render(request,"NewIndex.html")






def  sellerhomepage(request):
    return render(request,"Seller/SELLERHOME.html")




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
                obb=seller_table.objects.get(LOGINID__id=ob1.id)
                if obb.status == "active":
                    request.session['lid'] = ob1.id
                    return redirect('/sellerhomepage')
                else:
                    error_message = "Admin Blocked"
                    return render(request, 'loginindex.html', {'error_message': error_message})


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
    return HttpResponse('''<script>window.location='/managecategory#get-started'</script>''')

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
        return HttpResponse('''<script>window.location='/managecategory#get-started'</script>''')
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
    return redirect('/manageSeller')




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
        return HttpResponse('''<script>window.location='/manageSeller#get-started'</script>''')
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
        return HttpResponse('''<script>window.location='/manageSeller#get-started'</script>''')

def deleteSeller(request,id):
    ob = seller_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>window.location='/manageSeller#get-started'</script>''')


def PrductList(request):
    ob1=category_table.objects.all()
    ob=product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'])
    return render(request,"Seller/ManageProduct.html",{"val":ob,"cat":ob1})

def ProductList_post(request):
    ob1=category_table.objects.all()
    cat=request.POST['cat']
    s=request.POST['s']
    if cat == '0':
        ob=product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'],name__istartswith=s)
        return render(request, "Seller/ManageProduct.html", {"val": ob, "cat": ob1, "cc": int(cat), "s": s})

    else:
        ob = product_table.objects.filter(SELLER__LOGINID__id=request.session['lid'], name__istartswith=s,CATEGORY__id=cat)
        return render(request, "Seller/ManageProduct.html", {"val": ob, "cat": ob1,"cc":int(cat),"s":s})



def uvproducts(request):
    request.session['st']="2"
    ob=product_table.objects.all()
    ob1 = category_table.objects.all()
    return render(request,"User/products.html",{"val":ob,"cat":ob1})


def uvproducts_post(request):
    ob1=category_table.objects.all()
    cat=request.POST['cat']
    s=request.POST['s']
    if cat == '0':
        ob=product_table.objects.filter(name__istartswith=s)
        return render(request, "User/products.html", {"val": ob, "cat": ob1, "cc": int(cat), "s": s})

    else:
        ob = product_table.objects.filter( name__istartswith=s,CATEGORY__id=cat)
        return render(request, "User/products.html", {"val": ob, "cat": ob1,"cc":int(cat),"s":s})



def showMore_Product(request,id):
    a=product_table.objects.get(id=id)
    return  render(request,"User/showMore_Product.html",{'data':a})


def delete_product(request,id):
    ob=product_table.objects.get(id=id)
    ob.delete()
    return redirect("/ProductList")


def edit_product(request,id):
    request.session['pid']=id
    ob1=category_table.objects.all()
    ob=product_table.objects.get(id=id)

    return render(request, "Seller/updateProduct.html", {"val": ob, "cat": ob1})





def AddPrduct(request):
    ob=category_table.objects.all()
    return render(request,"Seller/AddProduct.html",{"val":ob})


def AddProductpost(request):
    name = request.POST["name"]
    phone = request.POST["stock"]
    email = request.POST["price"]
    unit=request.POST["unit"]
    status = request.POST["select"]
    image = request.FILES["file"]
    brand=request.POST["brand"]
    description=request.POST["description"]
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
    ob1.unit = unit
    ob1.brand=brand
    ob1.description=description
    ob1.photo = fsave
    ob1.CATEGORY = category_table.objects.get(id=status)
    ob1.SELLER = seller_table.objects.get(LOGINID__id=request.session['lid'])
    ob1.save()
    return redirect('/ProductList')


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
    return redirect('/ProductList')


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







#
# def uvproducts(request):
#     ob=product_table.objects.all()
#     ob1 = category_table.objects.all()
#     return render(request,"User/products.html",{"val":ob,"cat":ob1})
#
#
# def uvproducts_post(request):
#     ob1=category_table.objects.all()
#     cat=request.POST['cat']
#     s=request.POST['s']
#     if cat == '0':
#         ob=product_table.objects.filter(name__istartswith=s)
#         return render(request, "User/products.html", {"val": ob, "cat": ob1, "cc": int(cat), "s": s})
#
#     else:
#         ob = product_table.objects.filter( name__istartswith=s,CATEGORY__id=cat)
#         return render(request, "User/products.html", {"val": ob, "cat": ob1,"cc":int(cat),"s":s})
#
#

def userhome(request):
    cat=category_table.objects.all()
    request.session['st']="1"
    offer = offer_table.objects.filter(To_date__gte=datetime.today())
    for item in offer:
        item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)

    return render(request, "homeindex1.html", {'offer': offer,"cat":cat})


# def userhome_post(request):
#     pr=request.POST['s']
#     offer = offer_table.objects.filter(To_date__gte=datetime.today(),PRODUCT_id=pr)
#
#     for item in offer:
#         item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)
#
#     return render(request, "homeindex1.html", {'offer': offer})

from django.shortcuts import render
from datetime import datetime
from .models import offer_table, product_table

def userhome_post(request):
    search_term = request.POST.get('search_term', '').strip()  # Get the search term from POST request
    # Get all offers that are currently valid
    sc = request.POST['cat']
    if sc=="0":
        cat=category_table.objects.all()
        offers = offer_table.objects.filter(To_date__gte=datetime.today())

        # If a search term is provided, filter offers based on the product name
        if search_term:
            offers = offers.filter(PRODUCT__name__icontains=search_term)  # Use icontains for case-insensitive search

        # Calculate discounted prices for the filtered offers
        for item in offers:
            item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)

        return render(request, "homeindex1.html", {'offer': offers,"cat":cat})
    else:
        cat = category_table.objects.all()
        offers = offer_table.objects.filter(To_date__gte=datetime.today(),PRODUCT__CATEGORY__id=sc)

        # If a search term is provided, filter offers based on the product name
        if search_term:
            offers = offers.filter(PRODUCT__name__icontains=search_term)  # Use icontains for case-insensitive search

        # Calculate discounted prices for the filtered offers
        for item in offers:
            item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)

        return render(request, "homeindex1.html", {'offer': offers, "cat": cat,"cc":sc})


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


def add_offer1(request):
    return render(request,"Seller/add_offer.html")
#
# def Show_More_Offer(request,id):
#     a=offer_table.objects.get(id=id)
#     for item in a:
#         item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)
#     return render(request,"User/Show_More_Offer.html",{'data':a})


def Show_More_Offer(request, id):
    # Retrieve the specific offer using the provided id
    offer = offer_table.objects.get(id=id)

    # Calculate the discounted price based on the offer percentage
    discounted_price = offer.PRODUCT.price - (offer.PRODUCT.price * offer.Percentage / 100)

    # Prepare the context with the offer and discounted price
    context = {
        'data': offer,
        'discounted_price': discounted_price
    }

    return render(request, "User/Show_More_Offer.html", context)


def add_cart2(request,id):
    a=id
    # try:
    #     a=offer_table.objects.get(PRODUCT_id=id)
    #
    # except:
    #     pass
    return render(request,'User/add_to_cart2.html',{'data':a})


# def add_cart_post2(request):
#     id=request.POST['id']
#
#     cc=product_table.objects.get(id=id)
#     pr=cc.price
#
#     qty=request.POST['qty']
#
#     oo=order_table()
#     oo.USER=user_table.objects.get(LOGINID_id=request.session['lid'])
#     oo.date=datetime.now().today().date()
#     oo.status='cart'
#     oo.amount=pr*qty
#     oo.save()
#
#     a=order_details_table()
#     a.PRODUCT=product_table.objects.get(id=id)
#     a.Quantity=qty
#     a.ORDER=oo
#     a.price=float(pr)*float(qty)
#     a.save()
#     return redirect('/uvproducts')
#



from django.shortcuts import redirect
from datetime import datetime

def add_cart_post2(request):
    id = request.POST['id']
    cc = product_table.objects.get(id=id)
    pr = cc.price
    ofr=0
    obf=offer_table.objects.filter(To_date__gte=datetime.today(),PRODUCT__id=id)
    if len(obf)>0:
        ofr=obf[0].Percentage

    qty = int(request.POST['qty'])  # Ensure qty is an integer
    if qty<=0:
        error_message = "Invalid Qty"
        return render(request, 'User/add_to_cart2.html', {'error_message': error_message})

    if cc.stock>qty:
        cc.stock-=qty
        cc.save()

        oo=order_table.objects.filter(USER__LOGINID_id=request.session['lid'],status='cart')
        if len(oo)==0:
            oo = order_table()
            oo.USER = user_table.objects.get(LOGINID_id=request.session['lid'])
            oo.date = datetime.now().today().date()
            oo.status = 'cart'
            oo.amount = round((pr * qty)-(pr*qty*ofr/100), 2)  # Ensure precision by rounding to 2 decimal places
            oo.save()

            a = order_details_table()
            a.PRODUCT = cc  # No need to fetch again, use cc directly
            a.Quantity = qty
            a.ORDER = oo
            a.price = round((float(pr) * qty)-(pr*qty*ofr/100), 2)  # Rounding to 2 decimal places for consistency
            a.save()
        else:
            oo=oo[0]

            a = order_details_table.objects.filter(ORDER__id=oo.id,PRODUCT__id=cc.id)
            if len(a) == 0:
                a = order_details_table()
                a.PRODUCT = cc  # No need to fetch again, use cc directly
                a.Quantity = qty
                a.ORDER = oo
                a.price = round((float(pr) * qty)-(pr*qty*ofr/100), 2)  # Rounding to 2 decimal places for consistency
                a.save()
            else:
                a=a[0]
                a.Quantity =int(a.Quantity)+ qty
                a.price += round((float(pr) * qty)-(pr*qty*ofr/100), 2)
                a.save()
            oo.amount =float(oo.amount)+ round((pr * qty)-(pr*qty*ofr/100), 2)
            oo.save()

        if request.session['st'] == "2":
            return redirect("/uvproducts")
        else:
            return redirect("/userhome")
    error_message = "only "+str(cc.stock)+" units available"
    return render(request, 'User/add_to_cart2.html', {'error_message': error_message})




def add_offer2(request):
    title = request.POST["title"]
    description = request.POST["description"]
    percentage = request.POST["percentage"]
    fromdate = request.POST["fromdate"]
    todate = request.POST["todate"]
    ob = offer_table()
    ob.title = title
    ob.description= description
    ob.Percentage= percentage
    ob.From_date = fromdate
    ob.To_date = todate
    ob.PRODUCT=product_table.objects.get(id=request.session['pid'])
    ob.save()

    return redirect('/ProductList')




def add_cart(request,id):
    a=product_table.objects.get(id=id)
    return render(request,'user/add_qty.html',{'data':a})


def add_cart_post(request):
    id=request.POST['id']
    cc=product_table.objects.get(id=id)
    pr=cc.price

    qty=request.POST['qty']

    oo=order_table()
    oo.USER=user_table.objects.get(LOGINID_id=request.session['lid'])
    oo.date=datetime.now().today().date()
    oo.status='cart'
    oo.amount=float(pr)*qty
    oo.save()

    a=order_details_table()
    a.PRODUCT=product_table.objects.get(id=id)
    a.Quantity=qty
    a.ORDER=oo
    a.price=float(pr)*float(qty)
    a.save()
    return redirect('/uvproducts')





def view_product(request,id,t):
    request.session['pid']=id
    request.session['t']=t
    return redirect('/view_product1#get-started')
def view_product1(request):
    id=request.session['pid']
    ob = product_table.objects.filter(id=id)
    return render(request,"User/view_product.html",{"val":ob})



def buy_now(request,id):
    request.session['pid']=id
    ob = product_table.objects.filter(id=id)
    return render(request,"User/buy_now.html",{"val":ob})


def add_offers(request,id):
    request.session['pid']=id
    # products = offer_table.objects.all()
    # # promotions = promotion.objects.all()
    #
    # if request.method == 'POST':
    #     PRODUCT = request.POST['PRODUCT']
    #     SELLER = request.session['lid']  # Assuming seller ID is stored in session
    #     description = request.POST['description']
    #     Percentage = request.POST['Percentage']
    #     From_date = request.POST['From_date']
    #     To_date = request.POST['To_date']
    #
    #     existing_offer = offer_table.objects.filter(PRODUCT=PRODUCT).exists()
    #     if existing_offer:
    #         return render(request, 'Seller/AddOffer.html', {
    #             'products': products,
    #             'f': "0"
    #         })
    #
    #     offers = offer_table(
    #         PRODUCT=product_table.objects.get(id=PRODUCT),
    #         SELLER=seller_table.objects.get(LOGINID=SELLER),
    #         description=description,
    #         Percentage=Percentage,
    #         From_date=From_date,
    #         To_date=To_date
    #     )
    #     offers.save()
    #     return redirect('/ProductList')  # Redirect to product list page after successful save
    # return render(request, 'Seller/AddOffer.html')
    return  redirect("/add_offer1#get-started")


def buy_now_post(request):
    id=request.session['pid']
    if request.session['t']=="buy":
        obb = product_table.objects.get(id=id)

        qty=request.POST['qty']
        if obb.stock < int(qty):
            return redirect('/uvproducts')
        obb.stock -= int(qty)
        obb.save()
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
    else:

        obb = product_table.objects.get(id=id)

        qty = request.POST['qty']
        if obb.stock < int(qty):
            return redirect('/uvproducts')
        obb.stock -= int(qty)
        obb.save()
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

            ob = ob2[0]
            ob1 = order_details_table.objects.filter(PRODUCT__id=request.session['pid'], ORDER__id=ob.id)
            if len(ob1) == 0:
                ob1 = order_details_table()

                ob1.ORDER = ob
                ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
                ob1.Quantity = qty
                ob1.price = int(obb.price) * int(qty)
                ob1.save()

                ob.amount = int(ob.amount) + (int(obb.price) * int(qty))
                ob.save()
                return redirect('/uvproducts#profile')
            else:
                ob1 = ob1[0]

                ob1.Quantity = int(ob1.Quantity) + int(qty)
                ob1.price += int(obb.price) * int(qty)
                ob1.save()

                ob.amount = int(ob.amount) + (int(obb.price) * int(qty))
                ob.save()
                return redirect('/uvproducts#profile')



def delete_cart(request,id):

    a=order_details_table.objects.get(id=id)
    qty=int(a.Quantity)
    pob=product_table.objects.get(id=a.PRODUCT.id)
    pob.stock+=qty
    pob.save()
    oo=order_table.objects.get(id=a.ORDER.id)
    oo.amount = float(oo.amount) - a.price
    oo.save()


    a.delete()

    return redirect('/view_cart')


def view_cart(request):
    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'])
    for item in cart:
        item.subtotal = item.price   # Calculate subtotal
    s="0"
    if len(cart)>0:
        s="1"
    return render(request, "User/view_cart.html", {'cart': cart,"s":s})




def add_to_cart(request,id):
    request.session['pid'] = id
    ob = product_table.objects.filter(id=id)
    return render(request, "User/add_to_cart.html", {"val": ob})

def add_to_cart_post(request):
    qty = request.POST['qty']
    id = request.session['pid']
    obb = product_table.objects.get(id=id)
    if obb.stock <int(qty):
        return redirect('/uvproducts')
    obb.stock-=int(qty)
    obb.save()
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

        ob =ob2[0]
        ob1=order_details_table.objects.filter(PRODUCT__id=request.session['pid'],ORDER__id=ob.id)
        if len(ob1)==0:
            ob1 = order_details_table()

            ob1.ORDER = ob
            ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
            ob1.Quantity = qty
            ob1.price = int(obb.price) * int(qty)
            ob1.save()


            ob.amount =int(ob.amount)+ (int(obb.price) * int(qty))
            ob.save()
            return redirect('/uvproducts#profile')
        else:
            ob1 = ob1[0]


            ob1.Quantity = int(ob1.Quantity )+int(qty)
            ob1.price += int(obb.price) * int(qty)
            ob1.save()

            ob.amount = int(ob.amount) + (int(obb.price) * int(qty))
            ob.save()
            return redirect('/uvproducts#profile')


def view_promotions(request):
    seller = request.session['lid']
    product = offer_table.objects.filter(PRODUCT__SELLER__LOGINID_id=seller)
    return render(request, 'Seller/view_promotions.html',{'product':product})



def editProduct(request,id):
    ob = offer_table.objects.get(id=id)
    return render(request, 'Seller/edit_promotion.html',{'ob':ob})

def editproduct_post(request):
    id = request.POST['id']
    title = request.POST["title"]
    description = request.POST["description"]
    percentage = request.POST["percentage"]
    fromdate = request.POST["fromdate"]
    todate = request.POST["todate"]

    ob = offer_table.objects.get(id=id)

    ob.title = title
    ob.description = description
    ob.Percentage = percentage
    ob.From_date = fromdate
    ob.To_date = todate
    ob.save()
    return redirect('/view_promotions')

def deleteProduct(request,id):
    offer = offer_table.objects.get(id=id)
    offer.delete()
    return redirect('/view_promotions')
