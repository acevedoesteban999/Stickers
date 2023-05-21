from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,HttpResponseNotFound
from .models import MChoise,Product,RegisteCash,Movement,Visits,SummaryDate,UsEr,Category,SubCategory,SubCategoryColor
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormProduc,FormLot,FormImg
from datetime import datetime ,timedelta,timezone
from math import ceil,floor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q,F,Count,Sum,Choices
from django.urls import reverse
#import wifi_qrcode_generator.generator
#import qrcode
import json
"""
Tamplates Functions
"""
#from django import template
#register=template.Library()
#@register.filter
#def aaa(date_to_print):
#    try:
#        return date_to_print.strftime("%d-%m-%y")
#    except:
#        return ""

"""
Internal Functions
"""
replica_id=False

def Summary(movements,days_bool=False,products_bool=False,final_bool=False,only_worker=False,workers_bool=False):
        if movements:
            context={}
            if final_bool==True:
                movements_context=movements.filter(Q(type="VP")|Q(type="rP")|Q(type="RD")|Q(type="AD")|Q(type="CM")).values(
                            'lot',
                            'extra_info_int',
                            'extra_info_int_1',
                            'extra_info_int_2',
                        ).aggregate(
                            sales_money=Sum(
                                    F('lot')* F('extra_info_int'),
                                    default=0,
                                    filter=Q(type="VP"),
                                    ),
                            sales_profit=Sum(
                                    F('lot')* F('extra_info_int_1'),
                                    default=0,
                                    filter=Q(type="VP"),
                                    ),
                            sales_profit_worker=Sum(
                                    F('lot')* F('extra_info_int_2'),
                                    default=0,
                                    filter=Q(type="VP"),
                                    ),
                            refund_lot=Count(
                                    "lot",
                                    filter=Q(type="rP"),
                                ),
                            refund_money=Sum(
                                    F('lot')* F('extra_info_int'),
                                    default=0,
                                    filter=Q(type="rP"),
                                    ),
                            refund_profit=Sum(
                                    F('lot')* F('extra_info_int_1'),
                                    default=0,
                                    filter=Q(type="rP"),
                                    ),
                            refund_profit_worker=Sum(
                                    F('lot')* F('extra_info_int_2'),
                                    default=0,
                                    filter=Q(type="rP"),
                                    ),
                            retire_money=Sum(
                                    'lot',
                                    default=0,
                                    filter=Q(type="RD"),
                                    ),
                            agregate_money=Sum(
                                    'lot',
                                    default=0,
                                    filter=Q(type="AD"),
                                    ),
                            close_month_money=Sum(
                                    'lot',
                                    default=0,
                                    filter=Q(type="CM"),
                                    ),
                        )
                if movements_context:
                    context.update({"movements_exists":True})
                    context.update(movements_context)
                    context.update({"final_money":movements_context["sales_money"]+movements_context["agregate_money"]-movements_context["refund_money"]-movements_context["retire_money"]})
                    context.update({"final_profit":movements_context["sales_profit"]-movements_context["refund_profit"]})
                    context.update({"final_profit_worker":movements_context["sales_profit_worker"]-movements_context["refund_profit_worker"]})
                    context.update({"final_exists":True})
                    
            if products_bool == True:
                context.update({"movements_exists":True})
                products=movements.filter(type="VP").values(
                    'product__name',
                    'product__id',
                    'lot',
                    'extra_info_int',
                    'extra_info_int_1',
                    'extra_info_int_2',
                )
                if products:
                    context.update({"movements_exists":True})
                    context1={}
                    context2={"total_money":0,"total_profit":0,"total_profit_worker":0,"total_lot":0}
                    for product in products:
                        if context1.get(product['product__id']):
                            context1[product['product__id']]['lot']+=product['lot']
                            context1[product['product__id']]['money']+=product['extra_info_int']*product['lot'] 
                            context1[product['product__id']]['profit']+=product['extra_info_int_1']*product['lot'] 
                            context1[product['product__id']]['profit_worker']+=product['extra_info_int_2']*product['lot'] 
                            context2['total_money']+=product['extra_info_int']*product['lot'] 
                            context2['total_profit']+=product['extra_info_int_1']*product['lot'] 
                            context2['total_profit_worker']+=product['extra_info_int_2']*product['lot'] 
                            context2['total_lot']+=product['lot'] 
                        else:
                            context1[product['product__id']]={
                                "name":product['product__name'],
                                "id":product['product__id'],
                                "lot":product['lot'],
                                "money":product['extra_info_int']*product['lot'],
                                'profit':product['extra_info_int_1']*product['lot'],
                                'profit_worker':product['extra_info_int_2']*product['lot'],
                                }
                            context2['total_money']+=product['extra_info_int']*product['lot'] 
                            context2['total_profit']+=product['extra_info_int_1']*product['lot'] 
                            context2['total_profit_worker']+=product['extra_info_int_2']*product['lot']
                            context2['total_lot']+=product['lot'] 
                            
                    refund_products=movements.filter(type="rP").values(
                    'product__name',
                    'product__id',
                    'lot',
                    'extra_info_int',
                    'extra_info_int_1',
                    'extra_info_int_2',
                    )
                    if refund_products:
                        context3={}
                        for product in refund_products:
                            if context3.get(product['product__id']):
                                context3[product['product__id']]['lot']+=product['lot']
                                context3[product['product__id']]['money']+=product['extra_info_int']*product['lot'] 
                                context3[product['product__id']]['profit']+=product['extra_info_int_1']*product['lot'] 
                                context3[product['product__id']]['profit_worker']+=product['extra_info_int_2']*product['lot'] 
                                context2['total_money']-=product['extra_info_int']*product['lot'] 
                                context2['total_profit']-=product['extra_info_int_1']*product['lot'] 
                                context2['total_profit_worker']-=product['extra_info_int_2']*product['lot'] 
                                context2['total_lot']-=product['lot'] 
                            else:
                                context3[product['product__id']]={
                                    "name":product['product__name'],
                                    "id":product['product__id'],
                                    "lot":product['lot'],
                                    "money":product['extra_info_int']*product['lot'],
                                    'profit':product['extra_info_int_1']*product['lot'],
                                    'profit_worker':product['extra_info_int_2']*product['lot'],
                                    }
                                context2['total_money']-=product['extra_info_int']*product['lot'] 
                                context2['total_profit']-=product['extra_info_int_1']*product['lot'] 
                                context2['total_profit_worker']-=product['extra_info_int_2']*product['lot']
                                context2['total_lot']-=product['lot'] 
                        context.update({"refund_products":context3})  
                            
                                
                                
                        context.update({"products":context1}) 
                        context.update({"products_totals":context2}) 
                        context.update({"products_exists":True})   
                    
            if workers_bool == True:
                q=Q(type="VP")
                if only_worker!=False:
                    q=q&Q(user__id=only_worker)
                    
                products=movements.filter(q).values(
                    'product__name',
                    'product__id',
                    'lot',
                    'extra_info_int',
                    'extra_info_int_1',
                    'extra_info_int_2',
                    'extra_info_bool',
                    'user__username',
                )
                if products:
                    context.update({"movements_exists":True})
                    context1={}
                    context2={"total_money":0,"total_profit":0,"total_profit_worker":0,"total_lot":0}
                    for product in products:
                        if context1.get(product['user__username']):
                            if context1[product['user__username']]["products"].get(product['product__id']):
                                context1[product['user__username']]["products"][product['product__id']]['lot']+=product['lot']
                                context1[product['user__username']]["products"][product['product__id']]['money']+=product['extra_info_int']*product['lot']
                                context1[product['user__username']]["products"][product['product__id']]['profit']+=product['extra_info_int_1']*product['lot']
                                context1[product['user__username']]["products"][product['product__id']]['profit_worker']+=product['extra_info_int_2']*product['lot']
                                context1[product['user__username']]["total_money"]+=product['extra_info_int'] *product['lot']
                                context1[product['user__username']]["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context1[product['user__username']]["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context1[product['user__username']]["total_lot"]+=product['lot']
                                context2["total_money"]+=product['extra_info_int'] *product['lot']
                                context2["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context2["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context2["total_lot"]+=product['lot']
                            else:
                                context1[product['user__username']]["products"][product['product__id']]={
                                    "name":product['product__name'],
                                    "id":product['product__id'],
                                    "lot":product['lot'],
                                    "money":product['extra_info_int'] *product['lot'] ,
                                    "profit":product['extra_info_int_1'] *product['lot'] ,
                                    "profit_worker":product['extra_info_int_2'] *product['lot'],
                                }
                                context1[product['user__username']]["total_money"]+=product['extra_info_int'] *product['lot']
                                context1[product['user__username']]["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context1[product['user__username']]["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context1[product['user__username']]["total_lot"]+=product['lot']
                                context2["total_money"]+=product['extra_info_int'] *product['lot']
                                context2["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context2["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context2["total_lot"]+=product['lot']
                                
                        else:
                            context1[product['user__username']]={
                                "products":{
                                    product['product__id']:{
                                        "name":product['product__name'],
                                        "id":product['product__id'],
                                        "lot":product['lot'],
                                        "money":product['extra_info_int'] *product['lot'] ,
                                        "profit":product['extra_info_int_1'] *product['lot'] ,
                                        "profit_worker":product['extra_info_int_2'] *product['lot'] ,
                                    }
                                },
                                "total_money":product['extra_info_int'] *product['lot'],
                                "total_profit":product['extra_info_int_1'] *product['lot'],
                                "total_profit_worker":product['extra_info_int_2'] *product['lot'],
                                "total_lot":product['lot'],
                            }
                            context2["total_money"]+=product['extra_info_int'] *product['lot']
                            context2["total_profit"]+=product['extra_info_int_1'] *product['lot']
                            context2["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                            context2["total_lot"]+=product['lot']
                           
                            q=Q(type="rP")
                            if only_worker!=False:
                                q=q&Q(user__id=only_worker)
                            refund_worker_products=movements.filter(q).values(
                                'id',
                                'product__name',
                                'product__id',
                                'lot',
                                'extra_info_int',
                                'extra_info_int_1',
                                'extra_info_int_2',
                                'extra_info_bool',
                                'user__username',
                            )
                            
                    if refund_worker_products:
                        context3={}
                        for product in refund_worker_products:
                            print("A")
                            print(product)
                            if context3.get(product['user__username']):
                                if context3[product['user__username']]["products"].get(product['product__id']):
                                    context3[product['user__username']]["products"][product['product__id']]['lot']+=product['lot']
                                    context3[product['user__username']]["products"][product['product__id']]['money']+=product['extra_info_int']*product['lot']
                                    context3[product['user__username']]["products"][product['product__id']]['profit']+=product['extra_info_int_1']*product['lot']
                                    context3[product['user__username']]["products"][product['product__id']]['profit_worker']+=product['extra_info_int_2']*product['lot']
                                    context3[product['user__username']]["total_money"]+=product['extra_info_int'] *product['lot']
                                    context3[product['user__username']]["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                    context3[product['user__username']]["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                    context3[product['user__username']]["total_lot"]+=product['lot']
                                    context2["total_money"]-=product['extra_info_int'] *product['lot']
                                    context2["total_profit"]-=product['extra_info_int_1'] *product['lot']
                                    context2["total_profit_worker"]-=product['extra_info_int_2'] *product['lot']
                                    context2["total_lot"]-=product['lot']
                                else:
                                    context3[product['user__username']]["products"][product['product__id']]={
                                        "name":product['product__name'],
                                        "id":product['product__id'],
                                        "lot":product['lot'],
                                        "money":product['extra_info_int'] *product['lot'] ,
                                        "profit":product['extra_info_int_1'] *product['lot'] ,
                                        "profit_worker":product['extra_info_int_2'] *product['lot'],
                                    }
                                    context3[product['user__username']]["total_money"]+=product['extra_info_int'] *product['lot']
                                    context3[product['user__username']]["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                    context3[product['user__username']]["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                    context3[product['user__username']]["total_lot"]+=product['lot']
                                    context2["total_money"]-=product['extra_info_int'] *product['lot']
                                    context2["total_profit"]-=product['extra_info_int_1'] *product['lot']
                                    context2["total_profit_worker"]-=product['extra_info_int_2'] *product['lot']
                                    context2["total_lot"]-=product['lot']
                                    
                            else:
                                context3[product['user__username']]={
                                    "products":{
                                        product['product__id']:{
                                            "name":product['product__name'],
                                            "id":product['product__id'],
                                            "lot":product['lot'],
                                            "money":product['extra_info_int'] *product['lot'] ,
                                            "profit":product['extra_info_int_1'] *product['lot'] ,
                                            "profit_worker":product['extra_info_int_2'] *product['lot'] ,
                                        }
                                    },
                                    "total_money":product['extra_info_int'] *product['lot'],
                                    "total_profit":product['extra_info_int_1'] *product['lot'],
                                    "total_profit_worker":product['extra_info_int_2'] *product['lot'],
                                    "total_lot":product['lot'],
                                }
                                context2["total_money"]-=product['extra_info_int'] *product['lot']
                                context2["total_profit"]-=product['extra_info_int_1'] *product['lot']
                                context2["total_profit_worker"]-=product['extra_info_int_2'] *product['lot']
                                context2["total_lot"]-=product['lot']
                                
                        context.update({"refund_worker_products":context3})

                    context.update({"workers":context1})
                    context.update({"workers_totals":context2}) 
                    context.update({"workers_exists":True})
        else:
            context={"final_money":0,"final_profit":0,"final_profit_worker":0}
        return context
    
# def create_product(request):
#     crear_form=request.POST.dict()
#     files=FormImg(request.POST,request.FILES)
#     files.is_valid()
#     image=files.cleaned_data.get("imagen")
#     #name=crear_form.get("name").__str__().capitalize()
#     name=crear_form.get("NombreAlmacenar").__str__().capitalize()
#     pair=crear_form.get("VentasPares")
#     if pair == "1":
#         pair=True
#     else:
#         pair=False
    
#     unit_price=int(crear_form.get("precio unitario") )
#     unit_profit=int(crear_form.get("ganancia unitaria") )
#     unit_profit_worker=int(crear_form.get("ganancia unitaria trabajador") )
#     pair_price=0
#     pair_profit=0
#     pair_profit_worker=0
#     if pair == True:
#         pair_price=int(crear_form.get("precio pares"))
#         pair_profit=int(crear_form.get("ganancia pares") )
#         pair_profit_worker=int(crear_form.get("ganancia pares trabajador")) 
    
#     color_id=crear_form.get("SelectColor")
#     if color_id and color_id!="NC":
#         color=SubCategoryColor.objects.get(id=color_id)
#     else:
#         color=None
#     description=crear_form.get("descripción")
#     purchase_price=int(crear_form.get("precio compra"))
#     subcategoryID=int(crear_form.get("subcategoryid"))
#     subcategory=SubCategory.objects.get(id=subcategoryID)
#     user=request.user
#     result=Movement.Create_Product(purchase_price=purchase_price,color=color,subcategory=subcategory,user=user,name=name,pair=pair,unit_price=unit_price,pair_profit=pair_profit,unit_profit=unit_profit,unit_profit_worker=unit_profit_worker,pair_price=pair_price,pair_profit_worker=pair_profit_worker,description=description,image=image)
#     if result==True:
#         crear_form=FormProduc()
#         product=Product.objects.exclude(removed=True).get(name=name)
#         messages.success(request,"Se ha creado  el objeto {} correctamente".format(name))
#         #return redirect("/Producto/{}".format(product.id))
#         return redirect('producto',product.id)
#         #return True
#     elif result=="E0":
#         messages.error(request,"No se ha podido  crear, ya existe un objeto de nombre {}".format(name))
#     else:
#         messages.error(request,"No se ha podido  crear,ha ocurrido un error  insesperado")
#     return False
"""
View Functions
"""
def RedirectHomeView(request):
    return redirect("home")

def BasePost(request):
    try:
        if request.method == "POST":
            if "Inicar_Sesion" in request.POST:
                formlogin=AuthenticationForm(request,data=request.POST)
                if formlogin.is_valid():
                    nombre=formlogin.cleaned_data.get("username")
                    contra=formlogin.cleaned_data.get("password")
                    
                    usuario=authenticate(username=nombre,password=contra)
                    if usuario is not None:
                        login(request,usuario)
                        messages.success(request ,"Se ha iniciado sesión en la cuenta {} correctamente".format(nombre))    
                    else:
                        raise Exception()
                else:
                    formlogin=request.POST.dict()
                    nombre=formlogin.get("username")
                    username=UsEr.objects.filter(username=nombre).exists()
                    if username:
                        messages.error(request,"El usuario {} no está activo".format(nombre))
                    else:
                        messages.error(request,"Usuario o Contraseña incorrecto")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            elif "CerrarSesion" in request.POST:
                user=request.user.username
                logout(request)
                messages.success(request,"La cuenta %s se ha cerrado correctamente" % user)    
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            
            #is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest': #if is_ajax
                data = json.load(request)
                if 'SearchValue' in data:
                    search_value = data.get('SearchValue')  
                    try:
                        if search_value:
                            q=Q(removed=False) & (Q(name__contains=search_value) | Q(id__contains=search_value))
                            products=Product.objects.exclude(removed=True).filter(q)[:5]
                            if products:
                                return render(None,"BaseSearchProducts.html",{"products": products})
                    except Exception as e:
                        pass
                    return HttpResponse("NoProducts")
                elif 'VerifRefundIdMovement' in data:
                    id_refund = data.get('VerifRefundIdMovement') 
                    id_prouct=data.get("product_id")
                    if id_refund:
                        try:
                            movement=Movement.objects.filter(id=id_refund).values(
                                "id",
                                "type",
                                "lot",
                                "product__name",
                                "product__id",
                                "product__id",
                                "user__username",
                                "extra_info_bool",
                                "extra_info_int",
                                "extra_info_str",
                                #"extra_info_int_1",
                                #"extra_info_int_2",
                            )
                            if movement:
                                if movement[0].get('product__id')==id_prouct:
                                    if "<br><div class='text-danger'>Reembolsado</div>" not in movement[0].get('extra_info_str'):
                                        if movement[0].get('type') =="VP":
                                            return render(None,"BaseVerifRefundMovement.html",{"movement": movement[0]})
                                        return HttpResponse("E2")
                                    return HttpResponse("E4")
                                return HttpResponse("E3")
                            return HttpResponse("E1")
                        except Exception as e:
                            pass
                    return HttpResponse("E0")
                elif 'FilterResumeValue' in data:
                    filter_resume=int(data.get('FilterResumeValue'))
                    context={}
                    q=Q()
                    if filter_resume == 1:
                        day_resume=data.get('day_resume')
                        if not day_resume:
                            return HttpResponseNotFound("<div>Error,Fecha Invalida<div>")
                        
                        context.update({"start_date":datetime.strptime(day_resume,"%Y-%m-%d").date().strftime("%d-%m-%y")})
                        q=Q(date__date=day_resume)
                    elif filter_resume == 2:
                        summary_date=SummaryDate.objects.first()
                        if not summary_date:
                            raise Exception()   
                        week_resume=int(data.get('week_resume'))
                        if week_resume<0:
                            return HttpResponseNotFound("<div>Error,la Semana no puede ser Negativa<div>")
                        start_date=summary_date.start_date-timedelta(days=summary_date.start_date.weekday())+timedelta(days=7*week_resume)
                        end_date=start_date+timedelta(days=6)
                        context.update({"week":week_resume})
                        context.update({"start_date":start_date.strftime("%d-%m-%y")})
                        context.update({"end_date":end_date.strftime("%d-%m-%y")})
                        q=Q(date__range=(start_date,end_date+timedelta(days=1)))
                    elif filter_resume == 3:
                        start_date_resume=data.get("start_date_resume")
                        end_date_resume=data.get("end_date_resume")
                        if not start_date_resume or not end_date_resume:
                            return HttpResponseNotFound("<div>Error,Fecha Invalida<div>")
                        start_date=datetime.strptime(start_date_resume,"%Y-%m-%d")
                        end_date=datetime.strptime(end_date_resume,"%Y-%m-%d")
                        context.update({"start_date":start_date.strftime("%d-%m-%y")})
                        context.update({"end_date":end_date.strftime("%d-%m-%y")})
                        q=Q(date__range=(start_date,end_date+timedelta(days=1)))
                    else:
                        summary_date=SummaryDate.objects.first()
                        if not summary_date:
                            raise Exception()   
                        context.update({"start_date":summary_date.start_date.strftime("%d-%m-%y  %H:%M")})
                        context.update({"end_date":summary_date.end_date.strftime("%d-%m-%y")})
                        q=Q(date__range=(summary_date.start_date,datetime.now()))
                    
                    only_worker=False
                    if request.user.is_admin:
                        products_bool=data.get("filter_product")
                        workers_bool= data.get("filter_worker")
                        final_bool=True
                    elif request.user.is_worker:
                        only_worker=request.user.id
                        products_bool=False
                        workers_bool=True
                        final_bool=False
                        
                    q=q&(Q(type="VP")|Q(type="rP")|Q(type="RD")|Q(type="AD")|Q(type="CM"))
                    movements=Movement.objects.filter(q)
                    context.update(Summary(movements=movements,final_bool=final_bool,only_worker=only_worker,workers_bool=workers_bool,products_bool=products_bool ))
                    return render(None,"BaseResumeInfo.html",{"context":context})
                elif  "TodayInfo" in data:  
                    context={}
                    context.update(Summary(final_bool=True,movements=Movement.objects.filter(date__day=datetime.today().day)))
                    return render(None,"BaseHomeInfo.html",{"context":context,"user":request.user})
                return HttpResponse("Error")
        return render(request,"Home.html")
    except Exception as e:
        messages.error(request,"Algo ha salido mal")    
        return HttpResponseNotFound("Error, Algo Salio mal<br>Error:"+e.__str__())
    
def ResumeView(request):
    try:
        if request.method == "POST":
            if "CloseMonth" in request.POST:
                pass
                close_month=request.POST.dict()
                #next_date_start=close_month.get("NextDateStart")
                next_date_end=close_month.get("NextDateEnd")
                note=close_month.get("nota")
                context={}
                if not next_date_end:
                    messages.error(request,"Fecha del Proximo Mes Invalida")
                    return render(request,"Resume.html",{'context':context})
                summary_date=SummaryDate.objects.first()
                if not summary_date:
                    raise Exception()
                 
                context=Summary(
                    movements=Movement.objects.filter(type="VP",date__range=(summary_date.start_date,datetime.now())),
                    final_bool=True,
                )
                
                result=Movement.CloseMonth(
                    user=request.user,
                    #start_money=summary_date.start_money,
                    note=note,
                    date_start=summary_date.start_date,
                    date_end=summary_date.end_date,
                    next_date_end=datetime.strptime(next_date_end,"%Y-%m-%d").replace(hour=23,minute=59,second=59),
                    total_money=context["final_money"],
                    total_profit=context["final_profit"],
                    total_profit_worker=context["final_profit_worker"]
                    )
                if result==True:
                    messages.success(request,"Se ha Realizado el Cierre Correctamente")
                    return redirect("resumen")
                messages.error(request,"No se ha Podido Hacer el Resumen")
                return redirect("resumen")
            raise Exception()
        context={'context_global':{},'context_today':{},'context_this_week':{},'context_this_month':{}}
        summary_date=SummaryDate.objects.first()
        if not summary_date:
            raise Exception()
        today=datetime.now(timezone.utc)
            
        context['context_today'].update({"today":today.strftime("%d-%m-%y")})
        context['context_today'].update({"today_w_f":today.strftime("%Y-%m-%d")})
        if summary_date.active:
            context['context_global'].update({"SumaryDate":True})
            
            this_monday=today - timedelta(days=today.weekday())
            this_sunday=today + timedelta(days=6-today.weekday())
            this_week=ceil((this_sunday-summary_date.start_date).days/7)
            total_weeks=ceil((summary_date.end_date-summary_date.start_date).days/7)
            days_ok=(summary_date.end_date-today).days 
            context['context_this_week'].update({"start_date":this_monday.strftime("%d-%m-%y")})
            context['context_this_week'].update({"end_date":this_sunday.strftime("%d-%m-%y")})
            
            context['context_this_week'].update({"this_week":this_week}) 
            context['context_this_week'].update({"total_weeks":total_weeks})
            context['context_this_month'].update({"next_start_date":today.strftime("%Y-%m-%d")})
            context['context_this_month'].update({"next_end_date":(today+timedelta(days=35)).strftime("%Y-%m-%d")})
            context['context_this_month'].update({"days_ok":days_ok})
            context['context_this_month'].update({"start_date":summary_date.start_date.strftime("%d-%m-%y")})
            context['context_this_month'].update({"end_date":summary_date.end_date.strftime("%d-%m-%y")})
            
        else:
            context['context_global'].update({"SumaryDate":False})
        return render(request,"Resume.html",{'context':context})
    except Exception as e:
        messages.error(request,"Ha ocurrido un error inesperado")
    return redirect('home')
    
def HomeView(request):
    try:
        if request.method=="GET":
            if "QR" in request.GET:
                visits=Visits.objects.first()
                visits.total_visits+=1
                visits.save()
        context={}
        
        if request.user.is_authenticated and (request.user.is_worker or request.user.is_admin):
            products=Product.objects.exclude(removed=True).filter(confirm=False)
            context.update({"confirms":{"products":products},"confirms_count":products.count()})
        return render(request,"Home.html",context)
    
    except KeyError as e:
        pass
    return HttpResponse("Ha ocurrido un error insesperado , contacte con los administradores")

def CajaView(request):
    
    try:
        user=request.user
        if user.is_authenticated and user.is_admin:
            movements=Movement.objects.filter(Q(type="VP") | Q(type="CM") | Q(type="RD") | Q(type="AD") | Q(type="rP")).order_by('-date')[:20]
            if "RetireMoney" in request.POST:
                retire_product=request.POST.dict()
                lot_retire=int(retire_product.get("cantidad"))
                note=retire_product.get("nota")
                if lot_retire > 0:
                    if Movement.RetireMoney(user=user,lot=lot_retire,note=note):
                        messages.success(request,"Se ha retirado {}$ correctamente".format(lot_retire))
                        return render(request,"Caja.html",{"movements":movements})
                    messages.error(request,"No se han podido retirar {}$".format(lot_retire))
                return render(request,"Caja.html",{"movements":movements})
            elif "AgregateMoney" in request.POST:
                agregate_product=request.POST.dict()
                lot_agregate=int(agregate_product.get("cantidad"))
                note=agregate_product.get("nota")
                if lot_agregate > 0:
                    if Movement.AgregateMoney(user=user,lot=lot_agregate,note=note):
                        messages.success(request,"Se ha agregado {}$ correctamente".format(lot_agregate))
                        return render(request,"Caja.html",{"movements":movements})
                    messages.error(request,"No se han podido agregar {}$".format(lot_agregate))
                return render(request,"Caja.html",{"movements":movements})
            return render(request,"Caja.html",{"movements":movements})
        elif user.is_authenticated:
            messages.error(request,"No tiene Permisos para Acceder a este Sitio")    
            return redirect('home') 
        else:
            messages.error(request,"Debe Iniciar Sesión para Aceeder a este Sitio")    
            return redirect('home') 
    except Exception as e:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def TiendaView(request):
    try:
        q=Q(pair_stored__gt=0) | Q(unit_stored__gt=0)
        products = Product.objects.exclude(removed=True).filter(q).order_by('name')
        return render(request,"Tienda.html",{'products':products})
    except Exception as e:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def AdminView(request): 
    try:
        user=request.user
        if user:
            #products = Product.objects.exclude(removed=True).order_by('name')   
            categorys=Category.objects.all()
            colors=SubCategoryColor.objects.all()
            if request.method == "POST":
                if "CrearCategoría" in request.POST:
                    crear_form=request.POST.dict()
                    #files=FormImg(request.POST,request.FILES)
                    #files.is_valid()
                    name=crear_form.get("name").__str__().capitalize()
                    #image=files.cleaned_data.get("imagen")
                    if Movement.create_category(name=name,user=user):
                        messages.success(request,"Se ha creado  la categoría {} correctamente".format(name))
                        #return render(request,"Administracion.html",{"context":{"OkCC":True},"categorys":categorys})
                        category=Category.objects.get(name=name)
                        return redirect('categoria',category.id)
                    else:
                        messages.error(request,"No se ha podido  crear, ya existe una categoría de nombre {}".format(name))
                        return render(request,"Administracion.html",{"categorys":categorys})
                elif "CrearColor" in request.POST:
                    crear_form=request.POST.dict()
                    name=crear_form.get("name").__str__().capitalize()
                    if Movement.create_color(name=name,user=user):
                        messages.success(request,"Se ha creado  el color {} correctamente".format(name))
                    else:
                        messages.error(request,"No se ha podido crear, ya existe una color de nombre {}".format(name))

            return render(request,"Administracion.html",{'categorys':categorys,"colors":colors})
        else:
            messages.error(request,"Debe Iniciar Sesión para Aceeder a estos Recursos")    
            return redirect('home') 
    except Exception as e:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def CategoriaView(request,categoryID):
    try:
        user=request.user
        category=Category.objects.get(id=categoryID)
        if request.method=="POST":
            if "CrearSubCategoría" in request.POST:
                post_form=request.POST.dict()
                name=post_form.get("name").__str__().capitalize()
                if Movement.create_sub_category(name=name,category=category,user=user):
                    messages.success(request,"Se ha creado  la sub categoría {} correctamente".format(name))
                    subcategory=SubCategory.objects.get(name=name)
                    return redirect("subcategoria",category.id,subcategory.id)
                else:
                    messages.error(request,"No se ha podido crear, ya existe una sub categoría de nombre {}".format(name))
            elif "EditCategory" in request.POST:
                post_form=request.POST.dict()
                #files=FormImg(request.POST,request.FILES)
                #files.is_valid()
                name=post_form.get("name").__str__().capitalize()
                #image=files.cleaned_data.get("imagen")
                if Movement.edit_category(name=name,category=category,user=user):
                    messages.success(request,"Se ha editado  la categoría {} correctamente".format(name))
                else:
                    messages.error(request,"No se ha podido editar, ya existe una categoría de nombre {}".format(name))
            elif "EliminateCategory" in  request.POST:
                name=category.name
                if Movement.eliminate_category(name=name,category=category,user=user):
                    messages.success(request,"Se ha eliminado  la categoría: {} correctamente".format(name))
                    return redirect('administracion')
                messages.error(request,"No se ha podido eliminar la categoría: {}".format(name))
        products=Product.objects.exclude(removed=True).filter(sub_category__category__id=categoryID).values("name","id")
        subcategorys=SubCategory.objects.filter(category__id=categoryID)
        return render(request,"Categoria.html",{"category":category,"products":products,"subcategorys":subcategorys})
    except ObjectDoesNotExist:
        messages.error(request,"Error, categoría inexistente")
    #except Exception as e:
    #    messages.error(request,"Error, Algo ha salido mal")  
    return redirect('home')

def SubCategoriaView(request,categoryID,subcategoryID):
    try:
        
        user=request.user
        category=Category.objects.get(id=categoryID)
        subcategory=SubCategory.objects.get(id=subcategoryID)
        # if category!=subcategory.category:
        #     messages.error(request,"Error, categoría y subcategoría desiguales")
        #     return redirect('home')
        global replica_id
        replica=None
        if replica_id != False:
            replica_id_context=replica_id
            replica_id=False
            product=Product.objects.exclude(removed=True).get(id=replica_id_context)
            #product.name=product.name.replace(product.sub_category.name.lower(),"")
            #if product.color:
            #    product.name=product.name.replace(product.color.name.lower(),"")
            replica=product 
        if request.method=="POST":
            if "CrearProducto" in request.POST:
                # cp=create_product(request)
                # if  cp != False:
                #     return cp
                crear_form=request.POST.dict()
                files=FormImg(request.POST,request.FILES)
                files.is_valid()
                image=files.cleaned_data.get("imagen")
                name=crear_form.get("name").__str__().capitalize()
                #name=crear_form.get("NombreAlmacenar").__str__().capitalize()
                pair=crear_form.get("VentasPares")
                if pair == "1":
                    pair=True
                elif pair == "0":
                    pair=False
                else:
                    pair=None
                unit_price=0
                unit_profit=0
                unit_profit_worker=0
                if pair == False or pair== None:
                    unit_price=int(crear_form.get("precio unitario") )
                    unit_profit=int(crear_form.get("ganancia unitaria") )
                    unit_profit_worker=int(crear_form.get("ganancia unitaria trabajador") )
                    
                pair_price=0
                pair_profit=0
                pair_profit_worker=0
                if pair == True or pair == None:
                    pair_price=int(crear_form.get("precio pares"))
                    pair_profit=int(crear_form.get("ganancia pares") )
                    pair_profit_worker=int(crear_form.get("ganancia pares trabajador")) 
                
                color_id=crear_form.get("SelectColor")
                if color_id and color_id!="NC":
                    color=SubCategoryColor.objects.get(id=color_id)
                else:
                    color=None
                description=crear_form.get("descripción")
                purchase_price=int(crear_form.get("precio compra"))
                subcategoryID=int(crear_form.get("subcategoryid"))
                subcategory=SubCategory.objects.get(id=subcategoryID)
                user=request.user
                result=Movement.Create_Product(purchase_price=purchase_price,color=color,subcategory=subcategory,user=user,name=name,pair=pair,unit_price=unit_price,pair_profit=pair_profit,unit_profit=unit_profit,unit_profit_worker=unit_profit_worker,pair_price=pair_price,pair_profit_worker=pair_profit_worker,description=description,image=image)
                if result==True:
                    #crear_form=FormProduc()
                    product=Product.objects.exclude(removed=True).get(name=name)
                    messages.success(request,"Se ha creado  el objeto {} correctamente".format(name))
                    return redirect('producto',product.id)
                elif result=="E0":
                    messages.error(request,"No se ha podido  crear, ya existe un objeto de nombre {}".format(name))
                else:
                    messages.error(request,"No se ha podido  crear,ha ocurrido un error  insesperado")
                
            elif "EditSubCategory" in request.POST:
                post_form=request.POST.dict()
                name=post_form.get("name").__str__().capitalize()
                        
                if Movement.edit_sub_category(name=name,subcategory=subcategory,user=user):
                    messages.success(request,"Se ha editado  la subcategoría {} correctamente".format(name))
                else:
                    messages.error(request,"No se ha podido editar, ya existe una subcategoría de nombre {}".format(name))
            
            elif "EditarPreciosProductos" in request.POST:
                post_form=request.POST.dict()
                unit_price=post_form.get("precio unitario") 
                unit_profit=post_form.get("ganancia unitaria") 
                unit_profit_worker=post_form.get("ganancia unitaria trabajador") 
                pair_price=post_form.get("precio pares")
                pair_profit=post_form.get("ganancia pares") 
                pair_profit_worker=post_form.get("ganancia pares trabajador")
                purchase_price=post_form.get("precio compra")
                user=request.user
                products=Product.objects.exclude(removed=True).filter(sub_category=subcategory)
                result=Movement.edit_price_products(products=products,purchase_price=purchase_price,user=user,unit_price=unit_price,pair_profit=pair_profit,unit_profit=unit_profit,unit_profit_worker=unit_profit_worker,pair_price=pair_price,pair_profit_worker=pair_profit_worker)
                if result==True:
                    #product=Product.objects.exclude(removed=True).get(name=name)
                    messages.success(request,"Se han editado todos los objectos de la sub categoría {} correctamente".format(subcategory.name))
                    return redirect('subcategoria',category.id,subcategory.id)
                elif result=="E0":
                    messages.error(request,"No se ha podido editar")
                else:
                    messages.error(request,"No se ha podido  crear,ha ocurrido un error  insesperado")
            
            elif "EliminateSubCategory" in  request.POST:
                name=subcategory.name
                if Movement.eliminate_subcategory(name=name,subcategory=subcategory,user=user):
                    messages.success(request,"Se ha eliminado  la subcategoría: {} correctamente".format(name))
                    return redirect('administracion')
                messages.error(request,"No se ha podido eliminar la subcategoría: {}".format(name))
        colors=SubCategoryColor.objects.all()
        products=Product.objects.exclude(removed=True).filter(sub_category__id=subcategoryID)
        return render(request,"SubCategoria.html",{"replica":replica,"colors":colors,"category":category,"subcategory":subcategory,"products":products})
    except ObjectDoesNotExist:
        messages.error(request,"Error, categoría o subcategoría inexistente")
    #except Exception as e:
    #    print(e)
    #    messages.error(request,"Error, Algo ha salido mal")
    return redirect('home')
        
def ProductoView(request,productoID):
    try:
        product=Product.objects.exclude(removed=True).get(id=productoID)
        user=request.user
        if user:
            if product :
                movements_confirm=Movement.objects.filter(product_id=product.id,type="EP",extra_info_bool=False).order_by('date')      
                movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:10]
                product_qr_url=request.build_absolute_uri(reverse('producto',args=(product.id,)))
                colors=SubCategoryColor.objects.all()
                def NormalPageProduct():
                    return render(request,"Producto.html",{"colors":colors,'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def ErrorProduct(text):
                    messages.error(request,text)
                    return render(request,"Producto.html",{"colors":colors,'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def SuccessProduct(text,no_redirect=True):
                    if no_redirect != True:
                        try:
                            messages.success(request,text)
                            return redirect(no_redirect)
                        except Exception as e:
                            messages.error(request,"Errror:{}".format(e))
                            return redirect('home')
                    messages.success(request,text)
                    return render(request,"Producto.html",{"colors":colors,'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def WarningProduct(text,no_redirect=False):
                    if no_redirect==True:
                        messages.warning(request,text)
                        return render(request,"Producto.html",{'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                    messages.warning(request,text)
                    return redirect('home') 
                
                if request.method == "POST":
                    #Form Editar
                    if "ReplicaProduct" in request.POST:
                        global replica_id
                        replica_id=productoID
                        return redirect('subcategoria',product.sub_category.category.id,product.sub_category.id)
                    if "EditProduct" in request.POST:
                        edit_product=request.POST.dict()
                        files=FormImg(request.POST,request.FILES)
                        files.is_valid()
                        name=edit_product.get("name")
                        id=edit_product.get("id")
                        pair_price=None
                        pair_profit=None
                        pair_profit_worker=None
                        unit_price=None
                        unit_profit=None
                        unit_profit_worker=None
                        if product.pair == True or product.pair == None:
                            pair_price=int(edit_product.get("precio pares"))
                            pair_profit=int(edit_product.get("ganancia pares"))
                            pair_profit_worker=int(edit_product.get("ganancia pares trabajador"))
                        if product.pair == False or product.pair == None:
                            unit_price=int(edit_product.get("precio unitario"))
                            unit_profit=int(edit_product.get("ganancia unitario"))
                            unit_profit_worker=int(edit_product.get("ganancia unitario trabajador"))
                        description=edit_product.get("descripción")
                        purchase_price=int(edit_product.get("precio compra"))
                        color_id=edit_product.get("SelectColor")
                        color=None
                        if color_id and color_id!="NC":
                            color=SubCategoryColor.objects.get(id=color_id)
                        image=files.cleaned_data.get("imagen")
                        result=Movement.Edit(user=user,color=color,product=product,
                                            name=name,
                                            purchase_price=purchase_price,
                                            pair_price=pair_price,
                                            pair_profit=pair_profit,
                                            pair_profit_worker=pair_profit_worker,
                                            unit_price=unit_price,
                                            unit_profit=unit_profit,
                                            unit_profit_worker=unit_profit_worker,
                                            description=description,
                                            image=image) 
                        if result == True:
                            return SuccessProduct("Se ha editado el producto {} correctamente".format(name))
                        elif result == "E0":
                            return ErrorProduct("No se ha podido editar, ya existe un objeto de nombre {}".format(name))    
                    #Form Vender
                    elif "SellProduct" in request.POST:
                        sell_product=request.POST.dict()
                        lot_sell=int(sell_product.get("cantidad"))
                        accion_par=None
                        if product.pair==None:
                            accion_par=sell_product.get("AccionPar")
                            if accion_par:
                                accion_par=False
                            else:
                                accion_par=True
                        note=sell_product.get("nota")
                        
                        if product.pair == True:
                            result=Movement.Pair_Sell(user=user,product=product,lot=lot_sell,note=note)
                        elif product.pair == False:
                            result=Movement.Unit_Sell(user=user,product=product,lot=lot_sell,note=note)
                        else:
                            if accion_par == True:
                                result=Movement.Pair_Sell(user=user,product=product,lot=lot_sell,note=note)
                            else:
                                result=Movement.Unit_Sell(user=user,product=product,lot=lot_sell,note=note)
                        
                        if result == True or result=="OK0":
                            return SuccessProduct(
                                "Se han vendido {} {} {} {},con un importe de {}$".format(
                                    lot_sell,
                                    "pares de" if product.pair == True or (product.pair==None and accion_par == True)  else "unidades de",
                                    product.name,
                                    ", se ha descontado una unidad de un lote par " if result=="OK0" else "",
                                    product.pair_price*lot_sell if product.pair == True or (product.pair==None and accion_par == True)  else product.unit_price*lot_sell,
                                ),
                                #no_redirect='home',
                                )
                        elif result == 'E2':
                            return ErrorProduct("No se ha podido vender {} productos, solo se admite vender 1 unidad cuando ya no exsisten unidades por separado, esta unidad sera descontada de un par".format(lot_sell))
                        elif result == 'E0':
                            return ErrorProduct("No se ha podido vender {} {}, solo quedan {} de productos almacenados".format(lot_sell,product.name,(product.pair_stored.__str__() +" pares") if product.pair == True or (product.pair==None and accion_par == True)   else product.unit_stored.__str__() +" unidades"))       
                    #Form Eliminar
                    elif "RemoveProduct" in request.POST:
                        name=product.name
                        if Movement.Remove(user=user,product=product):
                            return WarningProduct("Se ha removido el producto {}, contacte con el administrador del proyecto para usar nuevamante este producto".format(name))
                        return ErrorProduct("No se ha podido remover el producto %s"%name)
                    #Form Agregar
                    elif "AddProduct" in request.POST:
                        add_product=request.POST.dict()
                        lot_add=int(add_product.get("cantidad"))
                        pair_action=None
                        pair_action=product.pair
                        if product.pair == None:
                            pair_action=add_product.get("AccionPar")
                            if pair_action:
                                pair_action=True
                            else:
                                pair_action=False
                            # =True
                            # if unit_action:
                            #     lot_add_1=int(add_product.get("cantidad_1"))
                            #     if lot_add==0:
                            #         pair_action=False
                            #         lot_add=lot_add_1
                        #else:             
                        #    pair_action=False
                        note=add_product.get("nota")
                        if Movement.Add(user=user,product=product,lot=lot_add,pair_action=pair_action,note=note):
                            return SuccessProduct("Se ha agregado {} {} {} , esperando a ser confirmado".format(
                                lot_add ,
                                "pares" if pair_action==True else "unidades",
                                " de " + product.name)
                                )
                        return ErrorProduct("No se han podido insertar {} {}".format(lot_add,product.name))
                    #Form Confirmar Agregar
                    elif "ConfirmAddProduct" in request.POST:
                        confirm_product=request.POST.dict()
                        id_movement=int(confirm_product.get("MovimientoID"))
                        note=confirm_product.get("nota")
                        if id_movement:
                            movement_to_confirm=Movement.objects.get(id=id_movement)
                            
                            if movement_to_confirm:
                                if Movement.ConfirmAdd(user=user,movement=movement_to_confirm,note=note):
                                    if movements_confirm.count()==0:
                                        movement_to_confirm.product.confirm=True
                                        movement_to_confirm.product.save()
                                        product=Product.objects.exclude(removed=True).get(id=product.id)
                                        return SuccessProduct("Se han confirmado y agregado {} {} {} {} correctamente".format(movement_to_confirm.lot," Pares" if movement_to_confirm.extra_info_int==1 or movement_to_confirm.extra_info_int==2 else "Unidades",("+ " + movement_to_confirm.extra_info_int_1.__str__()+" Unidades") if movement_to_confirm.extra_info_int==2 else "","de "+ movement_to_confirm.product.name))
                                    else:
                                        product=Product.objects.exclude(removed=True).get(id=product.id)
                                        return WarningProduct(no_redirect=True,text="Se han confirmado y agregado {} {} {} {} correctamente, pero aún quedan confirmaciones".format(movement_to_confirm.lot," Pares" if movement_to_confirm.extra_info_int==1 or movement_to_confirm.extra_info_int==2 else "Unidades","+ " + movement_to_confirm.extra_info_int_1.__str__()+" Unidades" if movement_to_confirm.extra_info_int==2 else "","de "+ movement_to_confirm.product.name))
                                        
                        return ErrorProduct("No se ha podido confirmar")
                    #Form Quitar
                    elif "SubProduct" in request.POST:
                        sub_product=request.POST.dict()
                        lot_sub=int(sub_product.get("cantidad"))
                        accion_par=None
                        if product.pair==None:
                            accion_par=sub_product.get("AccionPar")
                            if accion_par:
                                accion_par=False
                            else:
                                accion_par=True
                        #pair_action=sub_product.get("AccionPar")
                        note=sub_product.get("nota")
                        result=Movement.Sub(user=user,product=product,lot=lot_sub,note=note,pair=accion_par)
                        if result == True:
                            return SuccessProduct("Se han quitado {} {} {} correctamente".format(lot_sub,"Pares de " if product.pair==True or (product.pair==None and accion_par==True) else "Unidades de",product.name))
                        elif result == "E0":
                            return ErrorProduct("No se han podido quitar {} {}".format(lot_sub,product.name))
                    #Form Reembolsar
                    elif "RefundProduct" in request.POST: 
                        refund_product=request.POST.dict()
                        id_movement=int(refund_product.get("RefundIdMovement"))
                        
                        note=refund_product.get("nota")
                        
                        movement=Movement.objects.filter(id=id_movement)[0]
                        if movement:
                            result=Movement.Refund(user=user,product=product,movement=movement,note=note)
                            if result == True:
                                return SuccessProduct("Se han reembolsado {} {} {} con un importe de {}$".format(movement.lot,"Pares de " if movement.extra_info_bool else "Unidades de ",product.name,movement.lot * (product.pair_price if movement.extra_info_bool else product.unit_price)))
                            #elif result == "OK1":
                            #    return WarningProduct(no_redirect=True,text="Se han reembolsado {} {} {} con un importe de {}$, el usuario {} no presentaba el dinero suficiente en la cuenta, se ha retirado todo el dinero del usuario".format(movement.lot,"Pares de " if movement.extra_info_bool else "Unidades de ",product.name,movement.lot * (product.pair_price if movement.extra_info_bool else product.unit_price),user.username))
                            elif result == "E0":
                                return ErrorProduct("No se han podido reembolsar {} {}".format(movement.lot,product.name))
                            elif result == "E1":
                                return ErrorProduct("No hay suficiente dinero en caja para reembolsar {} {}".format(movement.lot,product.name))
                        return ErrorProduct("No exsiste id {}".format(id_movement))
                
                    return ErrorProduct("Ha ocurrido un error inesperado")    
                return NormalPageProduct()
        else:
            messages.error(request,"Debe Iniciar Sesión para Aceeder a estos Recursos")    
            return redirect('home') 
    except ObjectDoesNotExist:
        messages.error(request,"Error, producto inexistente")
    #except Exception as e:
    #    print(e)
    #    messages.error(request,"Error, Algo ha salido mal:{}".format(e))  
    return redirect('administracion')        

def OperacionesView(request):
    try:
        type_filter="NF"
        product_filter="NF"
        date_filter="NF"
        id_filter="NF"
        user_filter="NF"
        date_day_filter=datetime.today().strftime("%Y-%m-%d")
        date_start_filter=date_day_filter
        date_end_filter=date_day_filter
        q=Q()
        if request.method  == "POST":
            if "FilterMovement" in request.POST:
                filter_movement=request.POST.dict()
                id_filter=filter_movement.get("IdOpeartionFilter")
                if id_filter.isdigit():
                    id_filter=int(id_filter)
                    q=Q(id=id_filter)
                else:
                    id_filter=None
                    type_filter=filter_movement.get("TypeFilter")
                    date_filter=filter_movement.get("FilterDate")
                    product_filter=filter_movement.get("ProductFilter")
                    user_filter=filter_movement.get("UserFilter")
                    if product_filter.isdigit() and product_filter.__len__() == 4:
                        product_filter=int(product_filter)
                        q = q & Q(product__id=product_filter)
                    
                    if date_filter ==  "DD":
                        date_day_filter=filter_movement.get("FilterDateDay")
                        if not date_day_filter:
                            messages.error(request,"Error, Fecha Invalida")    
                            return redirect('home')
                        
                        q = q & Q(date__date=date_day_filter)
                    elif date_filter ==  "RD":
                        date_start_filter=filter_movement.get("FilterDateStart")
                        date_end_filter=filter_movement.get("FilterDateEnd")
                        if not date_start_filter or not date_end_filter:
                            messages.error(request,"Error, Fecha Invalida")    
                            return redirect('home')
                        start_date=date_start_filter
                        end_date=datetime.strptime(date_end_filter,"%Y-%m-%d").date()+timedelta(days=1)
                        q = q & Q(date__range=(start_date,end_date))
                    if type_filter != "NF":
                        q = q & Q(type=type_filter)
                    if user_filter != "NF":
                        q = q & Q(user__username=user_filter)
        movements=Movement.objects.filter(q).order_by('-date')[:20] 
        date_today_max =datetime.today() + timedelta(days=1)
        return render(request,"Operaciones.html",{"users":UsEr.objects.values_list("username",flat=True),"MChoise":MChoise,"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"id_filter":id_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"user_filter":user_filter,"date_filter":date_filter})
    except Exception as e:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def UsersView(request):
    try:
        # newUser=UsEr.objects.create_user(
        #     username="Juanito2",
        #     password="JuanitoPassWord",
        #     is_worker=True,
        #     )
        context={}
        admins=UsEr.objects.filter(is_active=True,is_admin=True,is_superuser=False)
        workers=UsEr.objects.filter(is_active=True,is_worker=True,is_superuser=False)
        users_desactivated=UsEr.objects.filter(is_active=False)
        context.update({"admins":admins})
        context.update({"workers":workers})
        if users_desactivated.__len__():
            context.update({"users_desactivated":users_desactivated})
        
    except Exception as e:
        pass
        
    return render(request,"Usuarios.html",{"context":context})

def UserView(request,usuarioID):
    try:
                
        user=UsEr.objects.get(id=usuarioID)
        if request.method=="POST":
            if "ActvateDesactivateUser" in request.POST:
                if Movement.EditUser(user=request.user,user_activ_desact=user):
                    messages.success(request,"Se ha {} el Usuario {} Correctamente".format("Activado" if user.is_active else "Desactivado",user.username))
                else:
                    raise Exception()
            if "EditUser" in request.POST:
                if request.user != user:
                    messages.error(request,"Error, solo se puede editar un usuario desde su propia cuenta")  
                    return redirect("home")
                edit_user=request.POST.dict()
                files=FormImg(request.POST,request.FILES)
                files.is_valid()
                username=edit_user.get("UserName")
                password=edit_user.get("PassWord")
                if not password:
                    password=None
                else:
                    passwordconfirm=edit_user.get("PassWord_Confirm")
                    if password!=passwordconfirm:
                        messages.error(request,"Error, las contraseñas no coinciden")  
                        return redirect("usuario",user.id)
                image=files.cleaned_data.get("imagen")
                result=Movement.EditUser(user=request.user,username=username,password=password,image=image)
                if result==True:
                    messages.success(request,"Se ha editado el Usuario {} Correctamente".format(username))
                    return redirect("usuario",user.id)
                elif result=="E0":    
                    messages.error(request,"Error, Ya existe un Usuario con nombre {}".format(username))
                else:
                    raise Exception()
        return render(request,"Usuario.html",{"UsEr":user})
    except Exception as e:
        messages.error(request,"Ha ocurrido un error inesperado")
    except ObjectDoesNotExist:
        messages.error(request,"Error, Usuario inexistente")  
    return redirect("home")

def QR(request):
    home_qr_url=request.build_absolute_uri(reverse('home'))+"?QR"
    return render(request,"QR.html",{"home_qr_url":home_qr_url})