from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,HttpResponseNotFound
from .models import MChoise,Product,RegisteCash,Movement,Visits,SummaryDate,UsEr
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
                    'product__i_d',
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
                        if context1.get(product['product__i_d']):
                            context1[product['product__i_d']]['lot']+=product['lot']
                            context1[product['product__i_d']]['money']+=product['extra_info_int']*product['lot'] 
                            context1[product['product__i_d']]['profit']+=product['extra_info_int_1']*product['lot'] 
                            context1[product['product__i_d']]['profit_worker']+=product['extra_info_int_2']*product['lot'] 
                            context2['total_money']+=product['extra_info_int']*product['lot'] 
                            context2['total_profit']+=product['extra_info_int_1']*product['lot'] 
                            context2['total_profit_worker']+=product['extra_info_int_2']*product['lot'] 
                            context2['total_lot']+=product['lot'] 
                        else:
                            context1[product['product__i_d']]={
                                "name":product['product__name'],
                                "i_d":product['product__i_d'],
                                "lot":product['lot'],
                                "money":product['extra_info_int']*product['lot'],
                                'profit':product['extra_info_int_1']*product['lot'],
                                'profit_worker':product['extra_info_int_2']*product['lot'],
                                }
                            context2['total_money']+=product['extra_info_int']*product['lot'] 
                            context2['total_profit']+=product['extra_info_int_1']*product['lot'] 
                            context2['total_profit_worker']+=product['extra_info_int_2']*product['lot'] 
                    context.update({"products":context1}) 
                    context.update({"products_totals":context2}) 
                    context.update({"products_exists":True})   
            
            if workers_bool == True:
                q=Q(type="VP")
                if only_worker!=False:
                    q=q&Q(user__id=only_worker)
                    
                products=movements.filter(q).values(
                    'product__name',
                    'product__i_d',
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
                            if context1[product['user__username']]["products"].get(product['product__i_d']):
                                context1[product['user__username']]["products"][product['product__i_d']]['lot']+=product['lot']
                                context1[product['user__username']]["products"][product['product__i_d']]['money']+=product['extra_info_int']*product['lot']
                                context1[product['user__username']]["products"][product['product__i_d']]['profit']+=product['extra_info_int_1']*product['lot']
                                context1[product['user__username']]["products"][product['product__i_d']]['profit_worker']+=product['extra_info_int_2']*product['lot']
                                context1[product['user__username']]["total_money"]+=product['extra_info_int'] *product['lot']
                                context1[product['user__username']]["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context1[product['user__username']]["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context1[product['user__username']]["total_lot"]+=product['lot']
                                context2["total_money"]+=product['extra_info_int'] *product['lot']
                                context2["total_profit"]+=product['extra_info_int_1'] *product['lot']
                                context2["total_profit_worker"]+=product['extra_info_int_2'] *product['lot']
                                context2["total_lot"]+=product['lot']
                            else:
                                context1[product['user__username']]["products"][product['product__i_d']]={
                                    "name":product['product__name'],
                                    "i_d":product['product__i_d'],
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
                                    product['product__i_d']:{
                                        "name":product['product__name'],
                                        "i_d":product['product__i_d'],
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
                    context.update({"workers":context1})
                    context.update({"workers_totals":context2}) 
                    context.update({"workers_exists":True})
        else:
            context={"final_money":0,"final_profit":0,"final_profit_worker":0}
        return context
    
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
                            q=Q(removed=False) & (Q(name__contains=search_value) | Q(i_d__contains=search_value))
                            products=Product.objects.filter(q)[:5]
                            if products:
                                return render(None,"BaseSearchProducts.html",{"products": products})
                    except Exception as e:
                        print(e)
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
                                "product__i_d",
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
                                        print(movement[0])
                                        if movement[0].get('type') =="VP":
                                            return render(None,"BaseVerifRefundMovement.html",{"movement": movement[0]})
                                        return HttpResponse("E2")
                                    return HttpResponse("E4")
                                return HttpResponse("E3")
                            return HttpResponse("E1")
                        except Exception as e:
                            print(e)
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
        print(e)
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
            this_week=floor((this_sunday-summary_date.start_date).days/7)
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
        print(e)
        messages.error(request,"Ha ocurrido un error inesperado")
    return redirect('home')
    
def HomeView(request):
    try:
        if request.method=="GET":
            if "QR" in request.GET:
                #visits=Visits.objects.update(F("total_visits") + 1)
                visits=Visits.objects.first()
                visits.total_visits+=1
                visits.save()
        context={}
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_worker):
            pass
            #context.update({"context_today":Summary(products_bool=True,operations_bool=True,movements=Movement.objects.filter(type="VP",date__day=date.today().day))})
            #context.update({'context_today':{"today":date.today().strftime("%d-%m-%y")}})
                 
            # summary_date=SummaryDate.objects.first()
            # if not summary_date:
            #     raise  Exception()
            
            # if summary_date.active:       
            #     context.update({"context_this_week":Summary(Movement.objects.filter(Q(type="VP")|Q(type="rP"),date__range=( date.today()-timedelta(days=date.today().weekday() ), date.today()+timedelta(days=1) )))})
            #     if context['context_this_week']:
            #         context['context_this_week'].update({"this_week":ceil((date.today()-summary_date.start_date).days/7) })
            #         context['context_this_week'].update({"total_weeks":ceil((summary_date.end_date-summary_date.start_date).days/7) })
            #     context.update({"context_this_month":Summary(Movement.objects.filter(Q(type="VP")|Q(type="rP"),date__range=( summary_date.start_date, date.today()+timedelta(days=1) )))})
            #     if context['context_this_month']:
            #         context['context_this_month'].update({"start_date":summary_date.start_date.strftime("%d-%m-%y"),"end_date":summary_date.end_date.strftime("%d-%m-%y")})
                
        return render(request,"Home.html",{"context":context})
    
    except KeyError as e:
        print(e)
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
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def TiendaView(request):
    try:
        q=Q(pair_stored__gt=0) | Q(unit_stored__gt=0)
        products = Product.objects.exclude(removed=True).filter(q).order_by('name')
        return render(request,"Tienda.html",{'products':products})
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def ProductosView(request): 
    try:
        user=request.user
        if user:
            products = Product.objects.exclude(removed=True).order_by('name')   

            if request.method == "POST":
                if "CrearProducto" in request.POST:
                    crear_form=request.POST.dict()
                    files=FormImg(request.POST,request.FILES)
                    files.is_valid()
                    name=crear_form.get("name").__str__().capitalize()
                    i_d=crear_form.get("i_d")
                    pair=crear_form.get("VentasPares")
                    if pair == "1":
                        pair=True
                    else:
                        pair=False
                    
                    unit_price=int(crear_form.get("precio unitario") )
                    unit_profit=int(crear_form.get("ganancia unitaria") )
                    unit_profit_worker=int(crear_form.get("ganancia unitaria trabajador") )
                    pair_price=0
                    pair_profit=0
                    pair_profit_worker=0
                    if pair == True:
                        pair_price=int(crear_form.get("precio pares"))
                        pair_profit=int(crear_form.get("ganancia pares") )
                        pair_profit_worker=int(crear_form.get("ganancia pares trabajador")) 
                    image=files.cleaned_data.get("imagen")
                    description=crear_form.get("descripción")
                    result=Movement.Create(i_d=i_d,user=user,name=name,pair=pair,unit_price=unit_price,pair_profit=pair_profit,unit_profit=unit_profit,unit_profit_worker=unit_profit_worker,pair_price=pair_price,pair_profit_worker=pair_profit_worker,description=description,image=image)
                    if result==True:
                        crear_form=FormProduc()
                        product=Product.objects.exclude(removed=True).get(name=name)
                        messages.success(request,"Se ha creado  el objeto {} correctamente".format(name))
                        return redirect("/Producto/{}".format(product.id))
                    elif result=="E0":
                        messages.error(request,"No se ha podido  crear, ya existe un objeto de nombre %s"% name)
                        return render(request,"Productos.html",{'products':products})
                messages.error(request,"Ha ocurrido un error  insesperado")
                return render(request,"Productos.html",{'products':products})
            return render(request,"Productos.html",{'products':products})
        else:
            messages.error(request,"Debe Iniciar Sesión para Aceeder a estos Recursos")    
            return redirect('home') 
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def ProductoView(request,productoID):
    try:
        product=Product.objects.exclude(removed=True).get(id=productoID)
        user=request.user
        #print(user)
        if user:
            if product :
                movements_confirm=Movement.objects.filter(product_id=product.id,type="EP",extra_info_bool=False).order_by('date')      
                movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:10]
                product_qr_url=request.build_absolute_uri(reverse('producto',args=(product.id,)))
                
                def NormalPageProduct():
                    return render(request,"Producto.html",{'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def ErrorProduct(text):
                    messages.error(request,text)
                    return render(request,"Producto.html",{'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def SuccessProduct(text):
                    #Eliminar si se redirecciona a 'home'
                    messages.success(request,text)
                    return render(request,"Producto.html",{'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def WarningProduct(text,no_redirect=False):
                    if no_redirect==True:
                        messages.warning(request,text)
                        return render(request,"Producto.html",{'product_qr_url':product_qr_url,'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                    messages.warning(request,text)
                    return redirect('home') 
                
                if request.method == "POST":
                    #Form Editar
                    if "EditProduct" in request.POST:
                        edit_product=request.POST.dict()
                        files=FormImg(request.POST,request.FILES)
                        files.is_valid()
                        name=edit_product.get("name")
                        i_d=edit_product.get("i_d")
                        pair_price=None
                        pair_profit_worker=None
                        if product.pair:
                            pair_price=int(edit_product.get("precio pares"))
                            pair_profit=int(edit_product.get("ganancia pares"))
                            pair_profit_worker=int(edit_product.get("ganancia pares trabajador"))
                        unit_price=int(edit_product.get("precio unitario"))
                        unit_profit=int(edit_product.get("ganancia unitario"))
                        unit_profit_worker=int(edit_product.get("ganancia unitario trabajador"))
                        description=edit_product.get("descripción")
                        image=files.cleaned_data.get("imagen")
                        result=Movement.Edit(user=user,product=product,
                                            name=name,
                                            i_d=i_d,
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
                        
                        pair_action=sell_product.get("AccionPar")
                        note=sell_product.get("nota")
                        #if pair_action:
                            #pair_action=True
                        
                        if pair_action:
                            result=Movement.Pair_Sell(user=user,product=product,lot=lot_sell,note=note)
                        else:
                            result=Movement.Unit_Sell(user=user,product=product,lot=lot_sell,note=note)
                        
                        if result == True or result== "OK0":
                            return SuccessProduct("Se han vendido {} {} {} {},con un importe de {}$".format(lot_sell,"pares de" if pair_action  else "unidades de",product.name,", se ha descontado una unidad de un lote par " if result=="OK0" else "",product.pair_price*lot_sell if pair_action  else product.unit_price*lot_sell))
                        elif result == 'E2':
                            return ErrorProduct("No se ha podido vender {} productos, solo se admite vender 1 unidad cuando ya no exsisten unidades por separado, esta unidad sera descontada de un par".format(lot_sell))
                        elif result == 'E0':
                            return ErrorProduct("No se ha podido vender {} {}, solo quedan {} productos almacenados".format(lot_sell,product.name,product.pair_stored.__str__() +" pares de" if pair_action  else product.unit_stored.__str__() +" unidades de"))       
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
                        lot_add_1=None
                        if product.pair:
                            unit_action=add_product.get("AccionPar")
                            pair_action=True
                            if unit_action:
                                lot_add_1=int(add_product.get("cantidad_1"))
                                if lot_add==0:
                                    pair_action=False
                                    lot_add=lot_add_1
                        else:             
                            pair_action=False
                        note=add_product.get("nota")
                        if Movement.Add(user=user,product=product,lot=lot_add,pair_action=pair_action,lot_1=lot_add_1,note=note):
                            return SuccessProduct("Se ha agregado {} {} {} {}, esperando a ser confirmado".format(lot_add ,"pares" if pair_action==True else "unidades",(" + " + lot_add_1.__str__()+" unidades de") if pair_action==True and lot_add_1!=None and lot_add_1>0  else "de" ,product.name))
                        return ErrorProduct("No se han podido insertar {} {}".format(lot_add,product.name))
                    #Form Confirmar Agregar
                    elif "ConfirmAddProduct" in request.POST:
                        confirm_product=request.POST.dict()
                        id_movement=int(confirm_product.get("MovimientoID"))
                        note=confirm_product.get("nota")
                        if id_movement:
                            movement_to_confirm=Movement.objects.get(id=id_movement)
                            print(movements_confirm)
                            
                            if movement_to_confirm:
                                if Movement.ConfirmAdd(user=user,movement=movement_to_confirm,note=note):
                                    if movements_confirm.count()==0:
                                        movement_to_confirm.product.confirm=True
                                        movement_to_confirm.product.save()
                                        product=Product.objects.get(id=product.id)
                                        return SuccessProduct("Se han confirmado y agregado {} {} {} {} correctamente".format(movement_to_confirm.lot," Pares" if movement_to_confirm.extra_info_int==1 or movement_to_confirm.extra_info_int==2 else "Unidades",("+ " + movement_to_confirm.extra_info_int_1.__str__()+" Unidades") if movement_to_confirm.extra_info_int==2 else "","de "+ movement_to_confirm.product.name))
                                    else:
                                        product=Product.objects.get(id=product.id)
                                        return WarningProduct(no_redirect=True,text="Se han confirmado y agregado {} {} {} {} correctamente, pero aún quedan confirmaciones".format(movement_to_confirm.lot," Pares" if movement_to_confirm.extra_info_int==1 or movement_to_confirm.extra_info_int==2 else "Unidades","+ " + movement_to_confirm.extra_info_int_1.__str__()+" Unidades" if movement_to_confirm.extra_info_int==2 else "","de "+ movement_to_confirm.product.name))
                                        
                        return ErrorProduct("No se ha podido confirmar")
                    #Form Quitar
                    elif "SubProduct" in request.POST:
                        sub_product=request.POST.dict()
                        lot_sub=int(sub_product.get("cantidad"))
                        
                        pair_action=sub_product.get("AccionPar")
                        note=sub_product.get("nota")
                        result=Movement.Sub(user=user,product=product,lot=lot_sub,note=note,pair=True if pair_action else False)
                        if result == True:
                            return SuccessProduct("Se han quitado {} {} {} correctamente".format(lot_sub,"Pares de " if pair_action else "Unidades de",product.name))
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
                            if result == "OK0":
                                return SuccessProduct("Se han reembolsado {} {} {} con un importe de {}$".format(movement.lot,"Pares de " if movement.extra_info_bool else "Unidades de ",product.name,movement.lot * (product.pair_price if movement.extra_info_bool else product.unit_price)))
                            elif result == "OK1":
                                return WarningProduct(no_redirect=True,text="Se han reembolsado {} {} {} con un importe de {}$, el usuario {} no presentaba el dinero suficiente en la cuenta, se ha retirado todo el dinero del usuario".format(movement.lot,"Pares de " if movement.extra_info_bool else "Unidades de ",product.name,movement.lot * (product.pair_price if movement.extra_info_bool else product.unit_price),user.username))
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
    except Exception as e:
        print(e)
        messages.error(request,"Error, Algo ha salido mal")  
    return redirect('productos')        

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
                        q = q & Q(product__i_d=product_filter)
                    
                    #print(type_filter,product_filter,date_filter)
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
        print(e)
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
        print(e)
        
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
                edit_user=request.POST.dict()
                files=FormImg(request.POST,request.FILES)
                files.is_valid()
                username=edit_user.get("UserName")
                image=files.cleaned_data.get("imagen")
                result=Movement.EditUser(user=request.user,user_edit=user,username=username,image=image)
                if result==True:
                    messages.success(request,"Se ha editado el Usuario {} Correctamente".format(username))
                elif result=="E0":    
                    messages.error(request,"Error, Ya existe un Usuario con nombre {}".format(username))
                else:
                    raise Exception()
        context={}
        return render(request,"Usuario.html",{"UsEr":user,"context":context})
    except Exception as e:
        print(e)
        messages.error(request,"Ha ocurrido un error inesperado")
    except ObjectDoesNotExist:
        messages.error(request,"Error, Usuario inexistente")  
    return redirect("usuarios")

def QRWIFI(request):
    return render(request,"QRWIFI.html")