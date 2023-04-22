from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,HttpResponseNotFound
from .models import MChoise,Product,RegisteCash,Movement,Visits,SummaryDate
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormProduc,FormLot,FormImg
from datetime import datetime ,timedelta,date
from math import ceil,floor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q,F,Count,Sum,Choices
import json


"""
Internal Functions
"""

"""
Contiene Reembolso de Producto
"""
def Summary(movements,total_resume_bool=False,products_bool=False,operations_bool=False,worker_bool=False):
        if movements:
            context=movements.filter(type="VP").values(
                        'lot',
                        'extra_info_int',
                        'extra_info_int_1',
                        'extra_info_int_2',
                        ).annotate(
                            lOt=Sum('lot'),
                            moNey=Sum(
                                F('lot')* F('extra_info_int'),
                                default=0
                                ),
                            proFit=Sum(
                                F('lot')* F('extra_info_int_1'),
                                default=0
                                ),
                            worKer_proFit=Sum(
                                F('lot')* F('extra_info_int_2'),
                                default=0
                                ),
                            
                    ).aggregate(
                        total_money=Sum('moNey'),
                        total_profit_money=Sum('proFit'),
                        total_worker_profit_money=Sum('worKer_proFit'),
                        total_lot=Sum('lOt'),
        )
            
            context.update({"total_total_money":context['total_money']})
            context.update({"total_total_profit_money":context['total_profit_money']})
            context.update({"total_total_worker_profit_money":context['total_worker_profit_money']})
            if products_bool == True:
                products=movements.filter(type="VP").values(
                    'product__name',
                    'product__i_d',
                    'lot',
                    'extra_info_int',
                    'extra_info_int_1',
                    'extra_info_int_2',
                    'extra_info_bool',
                )
                context1={}
                for product in products:
                    if context1.get(product['product__i_d']):
                        context1[product['product__i_d']]['lot']+=product['lot']
                        context1[product['product__i_d']]['money']+=product['extra_info_int']*product['lot'] 
                        context1[product['product__i_d']]['profit']+=product['extra_info_int_1']*product['lot'] 
                        context1[product['product__i_d']]['profit_worker']+=product['extra_info_int_2']*product['lot'] 
                    else:
                        context1[product['product__i_d']]={
                            "name":product['product__name'],
                            "i_d":product['product__i_d'],
                            "lot":product['lot'],
                            "money":product['extra_info_int']*product['lot'],
                            'profit':product['extra_info_int_1']*product['lot'],
                            'profit_worker':product['extra_info_int_2']*product['lot'],
                            }
                context.update({"products":context1})   
            if operations_bool == True:
                pass
                # operations=movements.values(
                #     "user__username",
                #     'id',
                #     "type",
                #     "product__name",
                #     "lot",
                # )
                #for operation in operations:
                #    for m in MChoise:
                #        if m[0]== operation["type"]:
                #            operation["type"]=m[1]
                #            break
                
                #context.update({"operations":movements})
            if worker_bool == True:
                products=movements.filter(type="VP").values(
                    'product__name',
                    'product__i_d',
                    'lot',
                    'extra_info_int',
                    'extra_info_int_1',
                    'extra_info_int_2',
                    'extra_info_bool',
                    'user__username',
                )
                context1={}
                for product in products:
                    if context1.get(product['user__username']):
                        if context1[product['user__username']].get(product['product__i_d']):
                            context1[product['user__username']][product['product__i_d']]['lot']+=product['lot']
                            context1[product['user__username']][product['product__i_d']]['money']+=product['extra_info_int']*product['lot']
                            context1[product['user__username']][product['product__i_d']]['profit']+=product['extra_info_int_1']*product['lot']
                            context1[product['user__username']][product['product__i_d']]['profit_worker']+=product['extra_info_int_2']*product['lot']
                        else:
                            context1[product['user__username']][product['product__i_d']]={
                                "name":product['product__name'],
                                "i_d":product['product__i_d'],
                                "lot":product['lot'],
                                "money":product['extra_info_int'] *product['lot'] ,
                                "profit":product['extra_info_int_1'] *product['lot'] ,
                                "profit_worker":product['extra_info_int_2'] *product['lot'] ,
                            }
                    else:
                        context1[product['user__username']]={
                            product['product__i_d']:{
                                "name":product['product__name'],
                                "i_d":product['product__i_d'],
                                "lot":product['lot'],
                                "money":product['extra_info_int'] *product['lot'] ,
                                "profit":product['extra_info_int_1'] *product['lot'] ,
                                "profit_worker":product['extra_info_int_2'] *product['lot'] ,
                            }
                        }
                context.update({"workers":context1})
                context_1=movements.filter(type="rP").values(
                        'lot',
                        'extra_info_int',
                        'extra_info_int_1',
                        'extra_info_int_2',
                        ).annotate(
                            moNey=Sum(
                                F('lot')* F('extra_info_int'),
                                default=0
                                ),
                            proFit=Sum(
                                F('lot')* F('extra_info_int_1'),
                                default=0
                                ),
                            worKer_proFit=Sum(
                                F('lot')* F('extra_info_int_2'),
                                default=0
                                ),
                    ).aggregate(
                        total_money=Sum('moNey'),
                        total_profit_money=Sum('proFit'),
                        total_worker_profit_money=Sum('worKer_proFit'),
                        total_lot=Sum('lot'),
                    )
                if context_1["total_money"]:
                    context['total_lot_refunds']=context_1["total_lot"]
                    context['total_total_money']-=context_1["total_money"]
                    context['total_total_profit_money']-=context_1["total_profit_money"]
                    context['total_total_worker_profit_money']-=context_1["total_worker_profit_money"]
                    context.update({"refunds":context_1})
                context_1=movements.filter(type="RD").values(
                        'lot',
                    ).aggregate(
                        total_money=Sum('lot'),
                    )
                if context_1["total_money"]:
                    context.update({"retires":context_1})
                context_1=movements.filter(type="AD").values(
                        'lot',
                    ).aggregate(
                        total_money=Sum('lot'),
                    )
                if context_1["total_money"]:
                    context.update({"agregates":context_1})
            if total_resume_bool == True:
                pass
                # context_1={}
                # for m in movements:
                #     if context_1.get(m.date.date()):
                #         context_1[m.date.date()]={
                #             'id':m.id,
                #             'product__i_d':m.product.i_d,
                #             'get_type_display':m.get_type_display,
                #             'lot':m.lot,
                #             'money':m.lot*m.extra_info_int,
                #             'profit':m.lot*m.extra_info_int_1,
                #             'profit_worker':m.lot*m.extra_info_int_2,
                #         }
                #     else:
                #         context_1[m.date.date()]={
                #             'm':m
                #         }
                # context.update({"total_resume":context_1})
        else:
            context={"total_money":0,"total_profit_money":0,"total_worker_profit_money":0,"total_lot":0,"no_movements":True}
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
                        messages.success(request ,"Se ha iniciado en la cuenta '%s' correctamente"  %  nombre)    
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                    messages.error(request,"No se pudo inicar en la cuenta '%s'" % nombre)
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
                                return render(None,"SearchProducts.html",{"products": products})
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
                                            return render(None,"VerifRefundMovement.html",{"movement": movement[0]})
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
                        date_resume=data.get('date_resume')
                        if not date_resume:
                            return HttpResponseNotFound("<div>Error,Fecha Invalida<div>")
                        
                        context.update({"start_date":datetime.strptime(date_resume,"%Y-%m-%d").date().strftime("%d-%m-%y")})
                        q=Q(date__date=date_resume)
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
                    else:
                        start_date_month=data.get("start_date_month")
                        end_date_month=data.get("end_date_month")
                        if not start_date_month or not end_date_month:
                            return HttpResponseNotFound("<div>Error,Fecha Invalida<div>")
                        end_date_month=datetime.strptime(end_date_month,"%Y-%m-%d").date()
                        context.update({"start_date":datetime.strptime(start_date_month,"%Y-%m-%d").date().strftime("%d-%m-%y")})
                        context.update({"end_date":end_date_month.strftime("%d-%m-%y")})
                        q=Q(date__range=(start_date_month,end_date_month+timedelta(days=1)))
                    movements=Movement.objects.filter(q)
                    
                    context.update(Summary(movements=movements,worker_bool=True))
                    return render(None,"ResumeInfo.html",{"context":context})
                return HttpResponse("Error")
        return render(request,"Home.html")
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
        return HttpResponseNotFound("Error, Algo Salio mal<br>Error:"+e.__str__())
    
def ResumeView(request):
    #try:
    #s=Summary(movements=Movement.objects.filter(date__date=date.today()),worker_bool=True)
    #return render(request,"ResumeInfo.html",{"context":s})
    context={'context_global':{},'context_today':{},'context_this_week':{},'context_this_month':{}}
    
    summary_date=SummaryDate.objects.first()
    if not summary_date:
        raise Exception()
    context['context_today'].update({"today":date.today().strftime("%d-%m-%y")})
    context['context_today'].update({"today_w_f":date.today().strftime("%Y-%m-%d")})
    if summary_date.active:
        context['context_global'].update({"SumaryDate":True})
        context['context_this_week'].update({"start_date":(date.today()-timedelta(days=date.today().weekday())).strftime("%d-%m-%y")})
        context['context_this_week'].update({"end_date":(date.today()-timedelta(days=date.today().weekday())+timedelta(days=6)).strftime("%d-%m-%y")})
        context['context_this_week'].update({"this_week":floor((date.today()-summary_date.start_date).days/7) }) 
        context['context_this_week'].update({"total_weeks":floor((summary_date.end_date-summary_date.start_date).days/7) })
        context['context_this_month'].update({"OK":True if summary_date.end_date > date.today() else False})
        context['context_this_month'].update({"days_ok":(summary_date.end_date- date.today()) if summary_date.end_date > date.today() else (date.today()-summary_date.end_date )})
        context['context_this_month'].update({"start_date":summary_date.start_date.strftime("%d-%m-%y"),"end_date":summary_date.end_date.strftime("%d-%m-%y")})
        context['context_this_month'].update({"start_date_w_f":summary_date.start_date.strftime("%Y-%m-%d")})
    else:
        context['context_global'].update({"SumaryDate":False})
    #print(context)          
    return render(request,"Resume.html",{'context':context})
    #except Exception as e:
    #    print(e)
    #return redirect('home')
    
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
            context.update({"context_today":Summary(products_bool=True,operations_bool=True,movements=Movement.objects.filter(date__day=date.today().day))})
            context['context_today'].update({"today":date.today().strftime("%d-%m-%y")})
                  
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
            movements=Movement.objects.filter(Q(type="VP") | Q(type="RD") | Q(type="AD") | Q(type="rP")).order_by('-date')[:20]
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
            messages.error(request,"Debe Iniciar Sesion para Aceeder a este Sitio")    
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
                    description=crear_form.get("descripcion")
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
            messages.error(request,"Debe Iniciar Sesion para Aceeder a estos Recursos")    
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
               
                
                def NormalPageProduct():
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def ErrorProduct(text):
                    messages.error(request,text)
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def SuccessProduct(text):
                    #Eliminar si se redirecciona a 'home'
                    messages.success(request,text)
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
                
                def WarningProduct(text,no_redirect=False):
                    if no_redirect==True:
                        messages.warning(request,text)
                        return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements}) 
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
                        pair_stored=None
                        pair_sold=None
                        pair_price=None
                        pair_profit_worker=None
                        if product.pair:
                            pair_stored=int(edit_product.get("almacenado pares"))
                            pair_sold=int(edit_product.get("vendido pares"))
                            pair_price=int(edit_product.get("precio pares"))
                            pair_profit=int(edit_product.get("ganancia pares"))
                            pair_profit_worker=int(edit_product.get("ganancia pares trabajador"))
                        unit_stored=int(edit_product.get("almacenado unitario"))
                        unit_sold=int(edit_product.get("vendido unitario"))
                        unit_price=int(edit_product.get("precio unitario"))
                        unit_profit=int(edit_product.get("ganancia unitario"))
                        unit_profit_worker=int(edit_product.get("ganancia unitario trabajador"))
                        #price=edit_product.get("precio")
                        description=edit_product.get("descripcion")
                        image=files.cleaned_data.get("imagen")
                        result=Movement.Edit(user=user,product=product,
                                            name=name,
                                            i_d=i_d,
                                            pair_stored=pair_stored,
                                            pair_sold=pair_sold,
                                            pair_price=pair_price,
                                            pair_profit=pair_profit,
                                            pair_profit_worker=pair_profit_worker,
                                            unit_stored=unit_stored,
                                            unit_sold=unit_sold,
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
                                        return WarningProduct(no_redirect=True,text="Se han confirmado y agregado {} {} {} {} correctamente, pero aun quedan confirmaciones".format(movement_to_confirm.lot," Pares" if movement_to_confirm.extra_info_int==1 or movement_to_confirm.extra_info_int==2 else "Unidades","+ " + movement_to_confirm.extra_info_int_1.__str__()+" Unidades" if movement_to_confirm.extra_info_int==2 else "","de "+ movement_to_confirm.product.name))
                                        
                        return ErrorProduct("No se ha podido confirmar")
                    #Form Quitar
                    elif "SubProduct" in request.POST:
                        sub_product=request.POST.dict()
                        lot_sub=int(sub_product.get("cantidad"))
                        
                        pair_action=sub_product.get("AccionPar")
                        note=sub_product.get("nota")
                        if pair_action:
                            result=Movement.Pair_Sub(user=user,product=product,lot=lot_sub,note=note)
                        else:
                            result=Movement.Unit_Sub(user=user,product=product,lot=lot_sub,note=note)
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
            messages.error(request,"Debe Iniciar Sesion para Aceeder a estos Recursos")    
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
                    #user_filter=filter_movement.get("UserFilter")
                    
                    if product_filter.isdigit() and product_filter.__len__() == 4:
                        product_filter=int(product_filter)
                        q = q & Q(product__i_d=product_filter)
                    else:
                        product_filter=None
                    
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
        movements=Movement.objects.filter(q).order_by('-date')[:20] 
        date_today_max =datetime.today() + timedelta(days=1)
        return render(request,"Operaciones.html",{"MChoise":MChoise,"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"id_filter":id_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"date_filter":date_filter})
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')
