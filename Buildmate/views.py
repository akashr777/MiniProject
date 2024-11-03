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


def view_my_ratings(request):
    seller = seller_table.objects.get(LOGINID_id=request.session['lid'])
    products = product_table.objects.filter(SELLER=seller)
    ratings = []
    for product in products:
        product_feedback = Feedback.objects.filter(PRODUCT=product)
        ratings.append({
            'product': product,
            'feedback': product_feedback
        })
    return render(request, 'Seller/view_ratings.html', {'ratings': ratings})


from django.db.models import F
from django.db.models.functions import Now
from datetime import timedelta
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
                ob=order_table.objects.filter(status='cart',USER__LOGINID__id=ob1.id,date__lte=Now() - timedelta(days=5))
                for i in ob:
                    obb=order_details_table.objects.filter(ORDER__id=i.id)
                    for j in obb:
                        a = order_details_table.objects.get(id=j.id)
                        qty = int(a.Quantity)
                        pob = product_table.objects.get(id=a.PRODUCT.id)
                        pob.stock += qty
                        pob.save()
                        oo = order_table.objects.get(id=a.ORDER.id)
                        oo.amount = float(oo.amount) - a.price
                        oo.save()

                        a.delete()
                    a=order_table.objects.get(id=i.id)
                    a.delete()
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


from django.db.models import Avg
from django.db.models import Sum
from datetime import datetime, timedelta


def get_dates_in_current_month():
    # Get the current date
    today = datetime.now()

    # Get the first day of the current month
    first_day = today.replace(day=1)

    # Get the last day of the current month
    if today.month == 12:
        last_day = first_day.replace(year=today.year + 1, month=1) - timedelta(days=1)
    else:
        last_day = first_day.replace(month=today.month + 1) - timedelta(days=1)

    # Generate all dates in the current month
    current_month_dates = []
    for day in range(first_day.day, last_day.day + 1):
        current_month_dates.append(first_day.replace(day=day))

    # Return the list of dates
    return [date.strftime("%Y-%m-%d") for date in current_month_dates]


def adminhome(request):
    totalorder=order_details_table.objects.all()
    cnt_totalorder=len(totalorder)

    totalusers=user_table.objects.all()
    cnt_totalusers=len(totalusers)

    totalsellers=user_table.objects.all()
    cnt_totalsellers=len(totalsellers)

    order=order_table.objects.filter(status='paid')
    d=get_dates_in_current_month()
    sumlist=[]
    daylist=[]
    minv=-1
    maxv=0
    for i in d:
        orderm=order_table.objects.filter(status='paid',date=i)
        sum=0
        daylist.append(int(str(i).split("-")[2]))
        for j in orderm:
            sum+=int(j.amount)
        sumlist.append(sum)
        if minv == -1 or minv > sum:
            minv = sum
        if sum > maxv:
            maxv = sum


    totalam=0
    for i in order:
        totalam=totalam+int(i.amount)

    total_feedbacks = Feedback.objects.aggregate(Sum('Rating'))['Rating__sum'] or 0
    feedback_count = Feedback.objects.count() or 1  # To avoid division by zero
    avg_rating = total_feedbacks / feedback_count
    #
    # feedback=Feedback.objects.all().order_by('-id')

    prducts=[]
    pr=product_table.objects.all()
    for i in pr:
        feedback_queryset=Feedback.objects.filter(PRODUCT=i.id)
        average_rating = feedback_queryset.aggregate(Avg('Rating'))['Rating__avg'] or 0
        # Default to 0 if no ratings
        r={"id":i.id,"pname":i.name,"pimg":str(i.photo.url),"avgrate":average_rating}
        prducts.append(r)
    return render(request,"admin/ADMINHOMEINDEX.html",{"totalorder":cnt_totalorder,'avg_rating':avg_rating,"totalusers":cnt_totalusers,"totalsellers":cnt_totalsellers,"totalam":totalam,"val":prducts,"s":sumlist,"d":daylist,"mv":minv,"mx":maxv})

def admin_view_rating(request,id):
    feedbacks = Feedback.objects.filter(PRODUCT=id)


    return render(request,"admin/ViewRating.html",{"feedback":feedbacks})



def adminhome_product_search(request):
    pname=request.POST["name"]
    # feedback = Feedback.objects.filter(PRODUCT__name__icontains=pname).order_by('-id')
    # totalorder = order_details_table.objects.all()
    # cnt_totalorder = len(totalorder)
    #
    # totalusers = user_table.objects.all()
    # cnt_totalusers = len(totalusers)
    #
    # totalsellers = user_table.objects.all()
    # cnt_totalsellers = len(totalsellers)
    #
    # order = order_table.objects.filter(status='paid')
    #
    # totalam = 0
    # for i in order:
    #     totalam = totalam + int(i.amount)
    # d = get_dates_in_current_month()
    # sumlist = []
    # daylist = []
    # minv=-1
    # maxv=0
    # for i in d:
    #     orderm = order_table.objects.filter(status='paid', date=i)
    #     sum = 0
    #     daylist.append(int(str(i).split("-")[2]))
    #     for j in orderm:
    #         sum += int(j.amount)
    #     sumlist.append(sum)
    #     if minv==-1 or minv>sum:
    #         minv=sum
    #     if sum>maxv:
    #         maxv=sum
    #
    # return render(request, "admin/ADMINHOMEINDEX.html",
    #               {"totalorder": cnt_totalorder, "totalusers": cnt_totalusers, "totalsellers": cnt_totalsellers,
    #                "totalam": totalam, "val": feedback,"s":sumlist,"d":daylist,"mv":minv,"mx":maxv})
    totalorder=order_details_table.objects.all()
    cnt_totalorder=len(totalorder)

    totalusers=user_table.objects.all()
    cnt_totalusers=len(totalusers)

    totalsellers=user_table.objects.all()
    cnt_totalsellers=len(totalsellers)

    order=order_table.objects.filter(status='paid')
    d=get_dates_in_current_month()
    sumlist=[]
    daylist=[]
    minv=-1
    maxv=0
    for i in d:
        orderm=order_table.objects.filter(status='paid',date=i)
        sum=0
        daylist.append(int(str(i).split("-")[2]))
        for j in orderm:
            sum+=int(j.amount)
        sumlist.append(sum)
        if minv == -1 or minv > sum:
            minv = sum
        if sum > maxv:
            maxv = sum


    totalam=0
    for i in order:
        totalam=totalam+int(i.amount)

    total_feedbacks = Feedback.objects.aggregate(Sum('Rating'))['Rating__sum'] or 0
    feedback_count = Feedback.objects.count() or 1  # To avoid division by zero
    avg_rating = total_feedbacks / feedback_count
    #
    # feedback=Feedback.objects.all().order_by('-id')

    prducts=[]
    pr=product_table.objects.filter(name__icontains=pname)
    for i in pr:
        feedback_queryset=Feedback.objects.filter(PRODUCT=i.id)
        average_rating = feedback_queryset.aggregate(Avg('Rating'))['Rating__avg'] or 0
        # Default to 0 if no ratings
        r={"id":i.id,"pname":i.name,"pimg":str(i.photo.url),"avgrate":average_rating}
        prducts.append(r)
    return render(request,"admin/ADMINHOMEINDEX.html",{"totalorder":cnt_totalorder,'avg_rating':avg_rating,"totalusers":cnt_totalusers,"totalsellers":cnt_totalsellers,"totalam":totalam,"val":prducts,"s":sumlist,"d":daylist,"mv":minv,"mx":maxv,"pn":pname})


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
    request.session['st'] = "2"

    # Fetch all products and categories
    ob = product_table.objects.all()
    ob1 = category_table.objects.all()
    ob2 = []

    for product in ob:
        # Get feedback for each product
        feedbacks = Feedback.objects.filter(PRODUCT__id=product.id)
        rating_sum = 0
        count = 0

        if feedbacks.exists():
            count = feedbacks.count()
            for feedback in feedbacks:
                rating_sum += feedback.Rating
            # Calculate the average rating, rounding to 2 decimal places
            average_rating = round(rating_sum / count, 2)
            product.r = average_rating  # Store the average rating
        else:
            product.r = None  # No rating available

        ob2.append(product)  # Append product to the list

    # Render the products page with product and category data
    return render(request, "User/products.html", {"val": ob2, "cat": ob1})


def uvproducts_post(request):
    ob1=category_table.objects.all()
    cat=request.POST['cat']
    s=request.POST['s']
    if cat == '0':
        ob2=[]
        ob=product_table.objects.filter(name__istartswith=s)
        for product in ob:
            # Get feedback for each product
            feedbacks = Feedback.objects.filter(PRODUCT__id=product.id)
            rating_sum = 0
            count = 0

            if feedbacks.exists():
                count = feedbacks.count()
                for feedback in feedbacks:
                    rating_sum += feedback.Rating
                # Calculate the average rating, rounding to 2 decimal places
                average_rating = round(rating_sum / count, 2)
                product.r = average_rating  # Store the average rating
            else:
                product.r = None  # No rating available

            ob2.append(product)  # Append product to the list

        # Render the products page with product and category data


        return render(request, "User/products.html", {"val": ob2, "cat": ob1, "cc": int(cat), "s": s})

    else:
        ob = product_table.objects.filter( name__istartswith=s,CATEGORY__id=cat)
        ob2 = []
        for product in ob:
            # Get feedback for each product
            feedbacks = Feedback.objects.filter(PRODUCT__id=product.id)
            rating_sum = 0
            count = 0

            if feedbacks.exists():
                count = feedbacks.count()
                for feedback in feedbacks:
                    rating_sum += feedback.Rating
                # Calculate the average rating, rounding to 2 decimal places
                average_rating = round(rating_sum / count, 2)
                product.r = average_rating  # Store the average rating
            else:
                product.r = None  # No rating available

            ob2.append(product)
    return render(request, "User/products.html", {"val": ob2, "cat": ob1,"cc":int(cat),"s":s})

#
#
# def showMore_Product(request,id):
#     a=product_table.objects.get(id=id)
#     return  render(request,"User/showMore_Product.html",{'data':a})


from django.db.models import Avg


def showMore_Product(request, id):
    a = product_table.objects.get(id=id)
    feedbacks = Feedback.objects.filter(PRODUCT=a)
    avg_rating = feedbacks.aggregate(Avg('Rating'))['Rating__avg'] or 0
    feedback_count = feedbacks.count()  # Count the number of feedback entries

    return render(request, 'User/showMore_Product.html', {
        'data': a,
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 1),
        'feedback_count': feedback_count
    })



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
    brand =request.POST["brand"]
    email = request.POST["price"]
    unit = request.POST["unit"]
    status = request.POST["select"]

    ob1 = product_table.objects.get(id=request.session['pid'])
    ob1.name = name
    ob1.stock = phone
    ob1.brand = brand
    ob1.price = email
    ob1.unit = unit
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
    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'],ORDER__status="cart")
    ccart=cart.count()
    request.session['ccart']=ccart

    for item in offer:
        item.discounted_price = item.PRODUCT.price - (item.PRODUCT.price * item.Percentage / 100)

        # Get feedback for each product
        feedbacks = Feedback.objects.filter(PRODUCT__id=item.PRODUCT.id)
        rating_sum = 0
        count = 0

        if feedbacks.exists():
            count = feedbacks.count()
            for feedback in feedbacks:
                rating_sum += feedback.Rating
            # Calculate the average rating, rounding to 2 decimal places
            average_rating = round(rating_sum / count, 2)
            item.r = average_rating  # Store the average rating
        else:
            item.r = None  # No rating available




    return render(request, "homeindex1.html", {'offer': offer,"cat":cat,'ccart':ccart})



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

            feedbacks = Feedback.objects.filter(PRODUCT__id=item.PRODUCT.id)
            rating_sum = 0
            count = 0

            if feedbacks.exists():
                count = feedbacks.count()
                for feedback in feedbacks:
                    rating_sum += feedback.Rating
                # Calculate the average rating, rounding to 2 decimal places
                average_rating = round(rating_sum / count, 2)
                item.r = average_rating  # Store the average rating
            else:
                item.r = None  # No rating available

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

            feedbacks = Feedback.objects.filter(PRODUCT__id=item.PRODUCT.id)
            rating_sum = 0
            count = 0

            if feedbacks.exists():
                count = feedbacks.count()
                for feedback in feedbacks:
                    rating_sum += feedback.Rating
                # Calculate the average rating, rounding to 2 decimal places
                average_rating = round(rating_sum / count, 2)
                item.r = average_rating  # Store the average rating
            else:
                item.r = None  # No rating available

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

from django.shortcuts import get_object_or_404
from django.db.models import Avg

def Show_More_Offer(request, id):
    # Use get_object_or_404 for better error handling
    offer = get_object_or_404(offer_table, id=id)

    # Calculate discounted price
    discounted_price = offer.PRODUCT.price * (1 - (offer.Percentage / 100))

    # Retrieve feedbacks and calculate average rating and count
    feedbacks = Feedback.objects.filter(PRODUCT=offer.PRODUCT)
    avg_rating = feedbacks.aggregate(Avg('Rating'))['Rating__avg'] or 0
    feedback_count = feedbacks.count()

    # Prepare context for rendering the template
    context = {
        'data': offer,
        'discounted_price': round(discounted_price, 2),  # Round for currency display
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 1),
        'feedback_count': feedback_count
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

    qty = int(request.POST['qty'])
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
        cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'], ORDER__status="cart")
        ccart = cart.count()
        request.session['ccart'] = ccart
        if request.session['st'] == "2":
            return redirect("/uvproducts")
        else:
            return redirect("/userhome")
    elif cc.stock == qty:
        cc.stock -= qty
        cc.save()
        oo = order_table.objects.filter(USER__LOGINID_id=request.session['lid'], status='cart')
        if len(oo) == 0:
            oo = order_table()
            oo.USER = user_table.objects.get(LOGINID_id=request.session['lid'])
            oo.date = datetime.now().today().date()
            oo.status = 'cart'
            oo.amount = round((pr * qty) - (pr * qty * ofr / 100), 2)  # Ensure precision by rounding to 2 decimal places
            oo.save()

            a = order_details_table()
            a.PRODUCT = cc  # No need to fetch again, use cc directly
            a.Quantity = qty
            a.ORDER = oo
            a.price = round((float(pr) * qty) - (pr * qty * ofr / 100), 2)  # Rounding to 2 decimal places for consistency
            a.save()
        else:
            oo = oo[0]

            a = order_details_table.objects.filter(ORDER__id=oo.id, PRODUCT__id=cc.id)
            if len(a) == 0:
                a = order_details_table()
                a.PRODUCT = cc  # No need to fetch again, use cc directly
                a.Quantity = qty
                a.ORDER = oo
                a.price = round((float(pr) * qty) - (pr * qty * ofr / 100),
                                2)  # Rounding to 2 decimal places for consistency
                a.save()
            else:
                a = a[0]
                a.Quantity = int(a.Quantity) + qty
                a.price += round((float(pr) * qty) - (pr * qty * ofr / 100), 2)
                a.save()
            oo.amount = float(oo.amount) + round((pr * qty) - (pr * qty * ofr / 100), 2)
            oo.save()
        cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'], ORDER__status="cart")
        ccart = cart.count()
        request.session['ccart'] = ccart
        if request.session['st'] == "2":
            return redirect("/uvproducts")
        else:
            return redirect("/userhome")
    else:
        print("jhhhhhhhhhhhhhhhhhhhhhhhhh")
        # error_message = "only "+str(cc.stock)+" units available"
        return HttpResponse(f'''
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    Swal.fire({{
                        icon: 'error',
                        title: 'Stock Information!',
                        text: 'Only {cc.stock} units available.',
                        showConfirmButton: false,  // Hides the confirm button
                        cancelButtonText: 'Close', // Label for the cancel button
                        showCancelButton: true,
                        reverseButtons: true
                    }}).then((result) => {{
                        if (result.dismiss === Swal.DismissReason.cancel) {{
                            window.location = '/userhome';  // Redirect when 'Close' is clicked
                        }}
                    }});
                }});
            </script>
        ''')

        # return render(request, 'User/add_to_cart2.html', {'error_message': error_message,"data":id})











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


    # else:
    #
    #     obb = product_table.objects.get(id=id)
    #
    #     qty = request.POST['qty']
    #     if obb.stock < int(qty):
    #         return redirect('/uvproducts')
    #     obb.stock -= int(qty)
    #     obb.save()
    #     ob2 = order_table.objects.filter(status='cart', USER__LOGINID=request.session['lid'])
    #     if len(ob2) == 0:
    #         qty = request.POST['qty']
    #         ob = order_table()
    #         ob.USER = user_table.objects.get(LOGINID__id=request.session['lid'])
    #         ob.date = datetime.today()
    #         ob.status = 'cart'
    #         ob.amount = 0
    #         ob.save()
    #
    #         ob1 = order_details_table()
    #         ob1.ORDER = ob
    #         ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
    #         ob1.Quantity = qty
    #         ob1.price = int(obb.price) * int(qty)
    #         ob1.save()
    #         ob.amount = int(obb.price) * int(qty)
    #         ob.save()
    #         return redirect('/uvproducts#profile')
    #
    #
    #     else:
    #
    #         ob = ob2[0]
    #         ob1 = order_details_table.objects.filter(PRODUCT__id=request.session['pid'], ORDER__id=ob.id)
    #         if len(ob1) == 0:
    #             ob1 = order_details_table()
    #
    #             ob1.ORDER = ob
    #             ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
    #             ob1.Quantity = qty
    #             ob1.price = int(obb.price) * int(qty)
    #             ob1.save()
    #
    #             ob.amount = int(ob.amount) + (int(obb.price) * int(qty))
    #             ob.save()
    #             return redirect('/uvproducts#profile')
    #         else:
    #             ob1 = ob1[0]
    #
    #             ob1.Quantity = int(ob1.Quantity) + int(qty)
    #             ob1.price += int(obb.price) * int(qty)
    #             ob1.save()
    #
    #             ob.amount = int(ob.amount) + (float(obb.price) * int(qty))
    #             ob.save()
    #             return redirect('/uvproducts#profile')



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
    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'], ORDER__status="cart")
    ccart = cart.count()
    request.session['ccart'] = ccart
    return redirect('/view_cart')


def view_cart(request):
    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'],ORDER__status="cart")
    sum=0
    for item in cart:
        item.subtotal = item.price
        # Calculate subtotal
        sum=sum+item.price
    s="0"
    if len(cart)>0:
        s="1"
    for item in cart:
        item.price = format(item.price, '.2f')
        item.save()
    return render(request, "User/view_cart.html", {'cart': cart,"s":s,"sum":sum})






def UpdateQuantity(request):
    id=request.GET['id']
    qty=request.GET['cv']
    print(id,qty)
    ob=order_details_table.objects.get(id=id)
    obp=product_table.objects.get(id=ob.PRODUCT.id)
    dif=int(qty)-int(ob.Quantity)
    np=0
    if dif>0:
        if obp.stock>=dif:
            obp.stock-=dif
            obp.save()
            nq=int(ob.Quantity)+1
            ob.Quantity=nq

            ob.price=nq*obp.price
            np=int(ob.Quantity)*obp.price
            ob.save()
        else:
            return JsonResponse({"is_taken": False, "m": obp.stock, "pc": ob.Quantity})
    else:
        obp.stock += dif
        obp.save()
        nq=int(ob.Quantity) - 1
        ob.Quantity = nq
        ob.price = nq * obp.price
        np=int(ob.Quantity) * obp.price
        ob.save()
    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'], ORDER__status="cart")
    sum = 0
    for item in cart:
        item.subtotal = item.price
        # Calculate subtotal
        sum = sum + item.price
    obo=order_table.objects.get(id=ob.ORDER.id)
    obo.amount=sum
    obo.save()
    np=str(round(float(np),2))
    npp=np.split(".")
    if len(npp[1])<2:
        np=str(np)+"0"
    sum=str(round(float(sum),2))
    npp=sum.split(".")
    if len(npp[1])<2:
        sum=str(sum)+"0"
    return JsonResponse({"is_taken":True,"np":str(np),"sum":str(sum)})




def UpdateQuantity1(request):
    id=request.GET['id'].split("-")[1]
    qty=request.GET['cv']
    print(id,qty)
    ob=order_details_table.objects.get(id=id)
    obp=product_table.objects.get(id=ob.PRODUCT.id)
    dif=int(qty)-int(ob.Quantity)
    print("dif",dif)
    np=0
    if dif>0:
        if obp.stock>=dif:
            obp.stock-=dif
            obp.save()
            nq=int(ob.Quantity)+dif
            print("nq", nq)
            ob.Quantity=nq

            ob.price=nq*obp.price
            np=int(nq)*obp.price
            ob.save()
        else:
            return JsonResponse({"is_taken": False,"m":obp.stock,"pc":ob.Quantity,"id":id})
    else:
        dif=abs(dif)
        obp.stock += dif
        obp.save()
        nq=int(ob.Quantity) - dif

        print("nq",nq)
        ob.Quantity = nq
        ob.price = nq * obp.price
        np=int(nq) * obp.price
        ob.save()

    cart = order_details_table.objects.filter(ORDER__USER__LOGINID_id=request.session['lid'], ORDER__status="cart")
    sum = 0
    for item in cart:
        item.subtotal = item.price
        # Calculate subtotal
        sum = sum + item.price
    obo=order_table.objects.get(id=ob.ORDER.id)
    obo.amount=sum
    obo.save()
    np=str(round(float(np),2))
    npp=np.split(".")
    if len(npp[1])<2:
        np=str(np)+"0"
    sum=str(round(float(sum),2))
    npp=sum.split(".")
    if len(npp[1])<2:
        sum=str(sum)+"0"
    return JsonResponse({"is_taken":True,"np":str(np),"sum":str(sum),"id":id})




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



import  razorpay
from razorpay.errors import ServerError


def user_pay_proceed(request):
    amt=request.session['pay_amount']
    # client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))

    # payment = client.order.create({'amount': str(amt), 'currency': "INR", 'payment_capture': '1'})
    # client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    # print(client)
    try:
        # payment = client.order.create({'amount': "11000", 'currency': "INR", 'payment_capture': '1'})
        res=user_table.objects.get(LOGINID__id=request.session['lid'])
        client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
        print(client)
        payment = client.order.create({'amount': str(amt), 'currency': "INR", 'payment_capture': '1'})

        # ob=order_table.objects.get(id=request.session['rid'])
        # ob.status='paid'
        # ob.save()
        return render(request,'User/UserPayProceed.html',{'p':payment,'val':res,"lid":request.session['lid'],"id":request.session['rid']})
    except ServerError as e:
        print(type(e))
        print(f"Razorpay Server Error: {e}")  # Log the error for further analysis
        return HttpResponse('''<script>alert("Payment failed due to server error. Please try again.");window.location="/userhome"</script>''')


def on_payment_success(request):
    print(request.GET,"-=====================================")
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']

    payment_id = request.GET.get('razorpay_payment_id')
    order_id = request.GET.get('razorpay_order_id')
    signature = request.GET.get('razorpay_signature')

    # Verify payment signature
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        # Verify signature using Razorpay's utility function
        razorpay.client.utility.verify_payment_signature(params_dict)
        # var = auth.authenticate(username='admin', password='admin')
        # if var is not None:
        #     auth.login(request, var)
        # amt = request.session['pay_amount']
        ob=order_table.objects.get(id=request.session['rid'])
        ob.status='paid'
        ob.save()


        return HttpResponse('''<script>alert("Success! Thank you for your Contribution");window.location="/userhome"</script>''')
    except:
        ob = order_table.objects.get(id=request.session['rid'])
        ob.status = 'failed'
        ob.save()
        return HttpResponse(
            '''<script>alert("Invalid! Thank you for your Contribution");window.location="/userhome"</script>''')


def buy_quantity(request,id):
    request.session['pid']=id
    return render(request, "User/buy_quantity.html")



def buy_now_post(request):
    # if request.session['t']=="buy":
    print(request.session['pid'],"kkkkkkkkkkk")
    obb = product_table.objects.get(id=request.session['pid'])
    print(obb,"jjjjjjjj")
    qty=request.POST['qty']
    if obb.stock < int(qty):
        error = True
        # return render(request, 'User/add_to_cart2.html',{'error':error,'qty':qty})
        # error_message = "only "+str(obb.stock)+" units available"
        return HttpResponse(f'''
                  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                  <script>
                      document.addEventListener("DOMContentLoaded", function() {{
                          Swal.fire({{
                              icon: 'error',  // You can use a built-in icon such as 'info' or 'warning'. Custom icons are not directly supported, but you can style them.
                              title: 'Stock Information!',
                              text: 'Only {obb.stock} units available.',
                              confirmButtonText: 'Proceed',
                              cancelButtonText: 'Close',
                              showCancelButton: true,
                              reverseButtons: true
                          }}).then((result) => {{
                              if (result.isConfirmed) {{
                                  window.location = '/userhome';
                              }} else {{
                                  window.location = '/userhome';
                              }}
                          }});
                      }});
                  </script>
              ''')

    obb.stock -= int(qty)
    obb.save()
    ob=order_table()
    ob.USER = user_table.objects.get(LOGINID__id=request.session['lid'])
    ob.date=datetime.now().strftime("%Y-%m-%d")
    ob.status='pending'
    ob.amount=str(int(obb.price)*int(qty)+(int(obb.price)*int(qty)*.10)).split(".")[0]
    ob.save()
    ob1=order_details_table()
    ob1.ORDER = ob
    ob1.PRODUCT = product_table.objects.get(id=request.session['pid'])
    ob1.Quantity=qty
    ob1.price=int(obb.price)*int(qty)
    ob1.save()
    request.session['pay_amount']=str((int(obb.price)*int(qty))+(int(obb.price)*int(qty)*.10)).split(".")[0]+"00"
    print("request.session['pay_amount']",request.session['pay_amount'])
    request.session['rid'] = ob.id
    # return redirect('/user_pay_proceed')

    return render(request,'User/delivery_details.html',{"t":int(obb.price)*int(qty),"gst":int(obb.price)*int(qty)*.10,"tamt":int(obb.price)*int(qty)+(int(obb.price)*int(qty)*.10)})



def buy_now_cart(request):


    ob=order_table.objects.get(USER__LOGINID__id=request.session['lid'],status='cart')

    # ob.status='cart'


    amt=0
    ob1=order_details_table.objects.filter(ORDER__id=ob.id)
    for i in ob1:
        amt=amt+float(i.price)

    tamt=amt+(amt*.1)

    request.session['pay_amount']=str(tamt).split(".")[0]+"00"
    print("request.session['pay_amount']",request.session['pay_amount'])
    request.session['rid'] = ob.id
    ob.amount=str(tamt).split(".")[0]
    ob.date=datetime.today()
    ob.save()
    # return redirect('/user_pay_proceed')

    return render(request,'User/delivery_details.html',{"t":amt,"gst":amt*.1,"tamt":tamt})






def useradd_delivery_address(request):
    fname=request.POST["fname"]
    lname=request.POST["lname"]
    houseno = request.POST["houseno"]
    pin = request.POST["pin"]
    phone=request.POST["phone"]
    landmark=request.POST["landmark"]
    address=request.POST["address"]
    oid=request.session['rid']

    ob=delivery_table()
    ob.ORDER = order_table.objects.get(id=oid)
    ob.firstName = fname
    ob.lastName = lname
    ob.houseNo = houseno
    ob.pin = pin
    ob.phone =phone
    ob.landMark = landmark
    ob.Address =address
    ob.save()

    return redirect('/user_pay_proceed')



def order(request,id):
    aa=product_table.objects.get(id=id)
    return render(request,"User/order_qty.html",{'data':aa})


from django.shortcuts import redirect
from datetime import datetime
from .models import product_table, order_table, order_details_table, user_table

def order_post(request):
    id = request.POST["id"]
    qty = float(request.POST["qty"])  # Order quantity

    # Fetch the product
    product = product_table.objects.get(id=id)

    # Check if enough stock is available
    if product.stock >= qty:
        # Calculate the total price for the order
        price = float(product.price)
        amount = qty * price

        # Create a new order
        ot = order_table()
        ot.USER = user_table.objects.get(LOGINID_id=request.session['lid'])
        ot.date = datetime.now().strftime("%Y-%m-%d")
        ot.status = 'ordered'
        ot.amount = amount
        ot.save()

        # Create a new order detail record
        op = order_details_table()
        op.PRODUCT = product
        op.Quantity = qty
        op.price = amount
        op.ORDER = ot
        op.save()

        # Decrement the product stock
        product.stock -= qty
        product.save()

        return redirect('/uvproducts')
    else:
        # Handle case where there is not enough stock
        return redirect('/stock_unavailable')


# def staff_view_orders(request):
#     ob=order_table.objects.exclude(status='cart')
#     return render(request,"Seller/StaffView_Order.html",{"val":ob})

def staff_view_order(request,id):
    ob=order_details_table.objects.filter(ORDER__id=id)
    return render(request,"Seller/StaffView_Order.html",{"val":ob})



def view_more(request,id):
    ob=order_details_table.objects.filter(ORDER__id=id)
    s="fff"
    try:
        s=ob[0].ORDER.status
    except:
        pass
    return render(request,"User/vieew_more.html",{"val":ob,"s":s})



def seller_view_cart(request):
    cart = order_details_table.objects.filter(PRODUCT__SELLER__LOGINID_id=request.session['lid']).exclude( ORDER__status="cart")
    r=[]
    for i in cart:
        r.append(i.ORDER.id)
    ll=order_table.objects.filter(id__in=r)
    return render(request, "Seller/view cart.html", {'cart': ll,})


def admin_view_order(request):
    ob = None
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')

        if from_date and to_date:
            # Convert strings to datetime objects
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
            ob = order_table.objects.filter(status='paid', date__range=(from_date, to_date))
            return render(request, "admin/Admin_View_Order.html", {"val": ob})
    ob = order_table.objects.filter(status='paid')

    return render(request, "admin/Admin_View_Order.html", {"val": ob})


def admin_view_more(request,id):
    ob=order_details_table.objects.filter(ORDER__id=id)
    return render(request,"admin/Admin_view_more.html",{"val":ob})




def updatecartqty(request,id,qty):

    ob=order_details_table.objects.get(id=id)
    ob.Quantity=qty
    ob.save()
    # need to incres amount from order and order details


    return HttpResponse('''<script>alert("Seccesfully Updated!");</script>''')


def update_order_status(request,id):
    request.session['odid']=id
    return render(request, "Seller/Update_status.html")



def update_order_status_post(request):
    print(request.POST,request.session['odid'])
    id=request.session['odid']
    status=request.POST['status']
    ob=order_details_table.objects.get(id=id)

    ob=ob.ORDER
    ob.status = status
    ob.save()
    return redirect("/seller_view_cart")



def view_order(request):
    ob=order_table.objects.filter(USER__LOGINID__id=request.session['lid']).exclude(status='cart').order_by("-date").order_by("-id")
    return render(request, "User/View_Order.html",{"val":ob})



def view_reciept(request,id):
    ob=order_details_table.objects.filter(ORDER__id=id)
    tamt=0
    for i in ob:
        i.amt=float(i.Quantity)*i.PRODUCT.price
        tamt+=float(i.Quantity)*i.PRODUCT.price
    gst=tamt*.1
    f=tamt+gst
    ob1=None
    try:
        ob1=delivery_table.objects.get(ORDER__id=id)
    except:
        pass

    return render(request, "User/View_reciept.html",{"val":ob,"gst":gst,"amt":tamt,"tamt":f,"ud":ob1})





def send_complaint(request):
    ob=Complaints.objects.filter(USER__LOGINID__id=request.session['lid'])

    return render(request, 'User/Send_complaint.html',{"val":ob})

from datetime import date  # Import date from datetime

def send_complaint_post(request):
    # request.session['lid']
    complaint = request.POST['complaint_details']
    complaint_details = Complaints()
    complaint_details.complaints = complaint
    complaint_details.date = date.today()  # Use date.today() after importing
    complaint_details.reply = 'pending'
    complaint_details.USER = user_table.objects.get(LOGINID=request.session['lid'])
    complaint_details.save()
    return HttpResponse('''<script>alert("Complaint sent successfully");window.location='/userhome'</script>''')



def view_complaints(request):
    ob=Complaints.objects.all()

    return render(request, 'admin/View_complaints.html',{"val":ob})



def send_reply_post(request):
    reply=request.POST['reply']
    c=request.POST['cid']
    ob=Complaints.objects.get(id=c)
    ob.reply=reply
    ob.save()

    return HttpResponse('''<script>window.location='/view_complaints'</script>''')

def feedback(request,id):
    request.session['pid']=id
    return render(request,"User/Feedback.html")


def add_rating(request):
    product_id=request.session['pid']
    ratings=request.POST['rating']
    feedback=request.POST["feedback"]
    c=Feedback()
    c.feedback = feedback
    c.Rating=ratings
    c.PRODUCT=product_table.objects.get(id=product_id)
    c.USER=user_table.objects.get(LOGINID__id=request.session["lid"])
    c.save()
    return redirect("/view_order")

def user_send_product_complaint(request,id):
    a=product_table.objects.get(id=id)
    return render(request,'user/product complaint.html',{'data':a})

def user_send_product_complaint_post(request):
    id=request.POST['id']
    com=request.POST['com']
    a=Complaints_product()
    a.PRODUCT=product_table.objects.get(id=id)
    a.USER=user_table.objects.get(LOGINID_id=request.session['lid'])
    a.date=datetime.now().today().date()
    a.complaints=com
    a.reply='pending'
    a.save()
    return redirect("/userhome")

def seller_view_reply(request):
    a=Complaints_product.objects.filter(PRODUCT__SELLER__LOGINID_id=request.session['lid'])
    return render(request,"Seller/ViewProduct_Complaint.html",{'data':a})


def seller_send_reply(request,id):
    a=Complaints_product.objects.get(id=id)
    return render(request,"Seller/product complainT REPLY.html",{'data':a})

def seller_send_reply_post(request):
    id=request.POST['id']
    com=request.POST['com']
    a=Complaints_product.objects.get(id=id)
    a.reply=com
    a.save()
    return redirect("/seller_view_reply")


def user_view_product_complaints(request):
    a=Complaints_product.objects.filter(USER__LOGINID_id=request.session['lid'])
    print(a)
    return render(request,'User/product complaints.html',{'data':a})