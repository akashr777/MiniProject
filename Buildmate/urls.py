from django.urls import path,include

from Buildmate import views

urlpatterns = [
    path('',views.newindex),

    path('login/',views.login),
    path('checkemail',views.checkemail),
    path('logincode',views.logincode),
    path('adminhome',views.adminhome),
    path('registration',views.registration),
    path('registrationPost',views.registrationPost),

    path('userhome', views.userhome),
    path('userhome_post', views.userhome_post),

    path('view_profile', views.view_profile),
    path('Sellerhome', views.Sellerhome),
    path('about', views.about),
    path('services', views.services),
    path('contact', views.contact),
    path('viewuser', views.viewuser),
    path('viewuserSearch', views.viewuserSearch),
    path('sellerSearch', views.sellerSearch),
    path('manageSeller', views.manageseller),
    path('addSeller', views.addseller),
    path('addsellerCode',views.addsellerCode),
    path('editsellerCode',views.editsellerCode),
    path('UpdateProductpost',views.UpdateProductpost),
    path('EditSeller/<int:id>',views.EditSeller),
    path('edit_product/<int:id>',views.edit_product),
    path('deleteSeller/<int:id>',views.deleteSeller),
    path('deletecategory/<int:id>',views.deletecategory),
    path('delete_product/<int:id>',views.delete_product),

    path('ProductList', views.PrductList),
    path('ProductList_post', views.ProductList_post),
    path('uvproducts', views.uvproducts),
    path('uvproducts_post', views.uvproducts_post),

    path('AddPrduct', views.AddPrduct),
    path('AddProductpost',views.AddProductpost),
    path('managecategory',views.managecategory),
    path('Addcategory',views.Addcategory),
    path('Addcategorypost',views.Addcategorypost),
    path('userProfile',views.view_profile),
    path('sellerProfile',views.sellerProfile),
    path('userProfilecode',views.userProfilecode),
    path('sellerProfilecode',views.sellerProfilecode),
    path('EditSeller1',views.EditSeller1),
    path('edit',views.edit),
    path('buy_now_post',views.buy_now_post),
    path('add_to_cart_post',views.add_to_cart_post),
    path('view_product/<id>/<t>',views.view_product),
    path('view_product1',views.view_product1),
    path('buy_now/<id>',views.buy_now),
    path('add_to_cart/<id>',views.add_to_cart),
    path('add_offers/<id>',views.add_offers),
    path('view_promotions',views.view_promotions),
    path('add_offer1',views.add_offer1),
    path('add_offer2',views.add_offer2),
    path('view_cart',views.view_cart),
    path('editProduct/<id>',views.editProduct),
    path('editproduct_post',views.editproduct_post),
    path('deleteProduct/<id>',views.deleteProduct),
    path('showMore_Product/<id>',views.showMore_Product),
    path('Show_More_Offer/<id>',views.Show_More_Offer),
    path('add_cart2/<id>',views.add_cart2),
    path('add_cart/<id>',views.add_cart),
    path('delete_cart/<id>',views.delete_cart),
    path('add_cart_post',views.add_cart_post),
    path('add_cart_post2',views.add_cart_post2),



    path('sellerhomepage',views.sellerhomepage),
    # path('edit_profile/<id>',views.edit_profile),


]