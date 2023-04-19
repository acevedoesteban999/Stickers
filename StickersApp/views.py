from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import MChoise,Product,RegisteCash,Movement,Visits,SummaryDate
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormProduc,FormLot,FormImg
from datetime import datetime ,timedelta,date
from math import ceil
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q,F,Count,Sum
import json
def RedirectHomeView(request):
    return redirect("home")

def BasePost(request):
    try:
        if request.method == "POST":
            if "Inicar_Sesion" in request.POST:
                formlogin=AuthenticationForm(request,data=request.POST)
                print(formlogin)
                if formlogin.is_valid():
                    nombre=formlogin.cleaned_data.get("username")
                    contra=formlogin.cleaned_data.get("password")
                    usuario=authenticate(username=nombre,password=contra)
                    if usuario is not None:
                        login(request,usuario)
                        messages.success(request ,"Se ha iniciado en la cuenta '%s' correctamente"  %  nombre)    
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                    messages.error(request,"No se pudo inicar en la cuenta '%s'" % nombre)
                print(formlogin)    
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
                                #"extra_info_int_1",
                                #"extra_info_int_2",
                            )
                            if movement:
                                if movement[0].get('product__id')==id_prouct:
                                    print(movement[0])
                                    if movement[0].get('type') =="VP":
                                        return render(None,"VerifRefundMovement.html",{"movement": movement[0]})
                                    return HttpResponse("E2")
                                return HttpResponse("E3")
                            return HttpResponse("E1")
                        except Exception as e:
                            print(e)
                    return HttpResponse("E0")
                return HttpResponse("Error")
        return render(request,"Home.html")
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('productos')

def ResumeView(request):
    
    return redirect('home')
    #try:
    def Movement_Resume(movements):
        money_sell_profit=movements.filter(
            Q(type='VP')|Q(type='rP')
                ).annotate(
                    money_sell_worker_profit=Sum(
                        F('lot')* F('extra_info_int_1'),
                        filter=Q(type="VP"),
                        default=0
                        ),
                    money_refund_worker_profit=Sum(
                        F('lot')* F('extra_info_int_1'),
                        filter=Q(type="rP"),
                        default=0
                        ),
                    money_sell=Sum(
                        F('lot')* F('extra_info_int'),
                        filter=Q(type="VP"),
                        default=0
                        ),
                    money_refund=Sum(
                        F('lot')* F('extra_info_int'),
                        filter=Q(type="rP"),
                        default=0
                        )
                ).aggregate(
                    total_money_worker_profit=Sum('money_sell_worker_profit')-Sum('money_refund_worker_profit'),
                    total_sells_money=Sum('money_sell')-Sum('money_refund'),
                )
        
        users_movement=movements.filter(
            Q(type='VP')|Q(type='rP')
            ).annotate(
                money_worker_profit=Sum(F('lot')* F('extra_info_int_1'),filter=Q(type='VP'),default=0)-Sum(F('lot')* F('extra_info_int_1'),filter=Q(type='rP'),default=0),
                money_sells=Sum(F('lot')* F('extra_info_int'),filter=Q(type='VP'),default=0)-Sum(F('lot')* F('extra_info_int'),filter=Q(type='rP'),default=0)
                ).values(
                    'money_worker_profit',
                    'money_sells',
                    'user__username'
                    )
        
        
        users_usernames=set(users_movement.values_list('user__username',flat=True))
        users_usernames.discard(None)
        
        users_profit={}
        for users_username in users_usernames:
            users_profit.update({users_username:users_movement.filter(user__username = users_username).aggregate(total_sells=Sum('money_sells'),total_profit=Sum('money_worker_profit'))})
        #print(users_profit)
        
        proucts_movements=movements.filter(
            Q(type='VP')|Q(type='rP')
            ).values(
                    'product__name',
                    'product__id',
                    )
        #print(proucts_movements)
        products = {}
        for prouct_movement in proucts_movements:
            if prouct_movement['product__id'] not in products:
                products.update({prouct_movement['product__id']:prouct_movement})
      
        context.update({'movements':movements})
        context.update({'money_sell_profit':money_sell_profit})
        context.update({"movements_count":movements.count()})
        context.update({"workers_profit":users_profit})
        context.update({"users_count":users_usernames.__len__()})
        context.update({"products":products})
        context.update({"proucts_count":products.__len__()})
        return context
        #proucts_sell=movements_today.filter(type='VP').values('product__name','product__id').distinct()
        
    date=datetime.now() 
    context={}
    movements_today=Movement.objects.filter(date__day=date.day).order_by('-date')
    #context.update({"movements_today_count":movements_today.count()})
    if movements_today:
        context_today=Movement_Resume(movements_today)
        context.update({"context_today":context_today})
        #print(context)
        #context.update({"movements_today":movements_today})
        #money_sell_profit_today=Movement.objects.filter(date__day=date.day,type='VP').annotate(money_worker_profit=Sum(F('lot')* F('extra_info_int_1')),money_sell=Sum(F('lot')* F('extra_info_int'))).aggregate(total_money_worker_profit=Sum('money_worker_profit'),total_sells_money=Sum('money_sell'),total_sells_count=Count('id'))
        #context.update(money_sell_profit_today)
        
        #users=movements_today.filter(type='VP').annotate(money_worker_profit=Sum(F('lot')* F('extra_info_int_1')),money_sells=Sum(F('lot')* F('extra_info_int'))).values('money_worker_profit','money_sells','user__username')
        #usersnames=set(users.values_list('user__username',flat=True))
        #print(usersnames)
        #context.update({"users_count":usersnames.__len__()})
        #users_profit={}
        #for username in usersnames:
        #    users_profit.update({username:users.filter(user__username = username).aggregate(total_sells=Sum('money_sells'),total_profit=Sum('money_worker_profit'))})
            #print(users_profit)
            #value=movements_today.filter('user__name'== userna me,type="VP").aggregate(total=Sum('money_worker_profit'))
            #print(value)
        #proucts_sell_today=movements_today.filter(type='VP').values('product__name','product__id').distinct()
        #context.update({"proucts_sell_today":proucts_sell_today})
        #context.update({"proucts_count_today":proucts_sell_today.count()})
        #context.update({"workers_profit":users_profit})
        #print(context)
        #contextUser={}
        
    #movements_sell_today=Movement.objects.filter(date__day=date.day,type="VP")
    #ids_today=Movement.objects.filter(date__day=date.day).values_list("product__id",flat=True)
    #print(movements_sell_today)
    
    return render(request,"Resume.html",{'context':context})
    
    #except Exception as e:
    #    print(e)
    return HttpResponse("Ha ocurrido un error insesperado , contacte con los administradores")

def HomeView(request):
    def Summary(movement):
        if movement:
            context=movement.values(
                        'lot',
                        'extra_info_int',
                        'extra_info_int_1',
                        'extra_info_int_2',
                        ).annotate(
                            moNey=Sum(
                                F('lot')* F('extra_info_int'),
                                #filter=Q(type="VP"),
                                default=0
                                ),
                            #money_refund_worker_profit=Sum(
                            #    F('lot')* F('extra_info_int_1'),
                            #    filter=Q(type="rP"),
                            #    default=0
                            #    ),
                            proFit=Sum(
                                F('lot')* F('extra_info_int_1'),
                                #filter=Q(type="VP"),
                                default=0
                                ),
                            worKer_proFit=Sum(
                                F('lot')* F('extra_info_int_2'),
                                #filter=Q(type="VP"),
                                default=0
                                ),
                            #money_refund=Sum(
                            #    F('lot')* F('extra_info_int'),
                            #    filter=Q(type="rP"),
                            #    default=0
                            #    )
                    ).aggregate(
                        #total_money_worker_profit=Sum('money_sell_worker_profit')-Sum('money_refund_worker_profit'),
                        #total_sells_money=Sum('money_sell')-Sum('money_refund'),
                        total_money=Sum('moNey'),
                        total_profit_money=Sum('proFit'),
                        total_worker_profit_money=Sum('worKer_proFit')
                        
        )
            products=movement.values(
                'product__name',
                'product__i_d',
                'lot',
                'product__pair_price',
                'product__unit_price',
                'extra_info_bool',
            )
            context1={}
            for product in products:
                if context1.get(product['product__i_d']):
                    context1[product['product__i_d']]['lot']+=product['lot']
                    context1[product['product__i_d']]['money']+=product['product__pair_price']*product['lot'] if product['extra_info_bool'] else product['product__unit_price']*product['lot']
                else:
                    context1[product['product__i_d']]={"name":product['product__name'],"i_d":product['product__i_d'],"lot":product['lot'],"money":product['product__pair_price'] *product['lot'] if product['extra_info_bool'] else product['product__unit_price'] *product['lot']}
            context.update({"products":context1})    
        else:
            context={"total_money":0,"total_profit_money":0,"total_worker_profit_money":0}
        return context
    try:
        if request.method=="GET":
            if "QR" in request.GET:
                #visits=Visits.objects.update(F("total_visits") + 1)
                visits=Visits.objects.first()
                visits.total_visits+=1
                visits.save()
        context={}
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_worker):
            context.update({"context_today":Summary(Movement.objects.filter(type="VP",date__day=date.today().day))})
            summary_date=SummaryDate.objects.first()
            if not summary_date:
                raise  Exception()
            
            if summary_date.active:       
                context.update({"context_this_week":Summary(Movement.objects.filter(type="VP",date__range=( date.today()-timedelta(days=date.today().weekday() ), date.today()+timedelta(days=1) )))})
                if context['context_this_week']:
                    context['context_this_week'].update({"this_week":ceil((date.today()-summary_date.start_date).days/7) })
                    context['context_this_week'].update({"total_weeks":ceil((summary_date.end_date-summary_date.start_date).days/7) })
                context.update({"context_this_month":Summary(Movement.objects.filter(type="VP",date__range=( summary_date.start_date, date.today()+timedelta(days=1) )))})
                if context['context_this_month']:
                    context['context_this_month'].update({"start_date":summary_date.start_date.strftime("%d-%m-%y"),"end_date":summary_date.end_date.strftime("%d-%m-%y")})
                
        return render(request,"Home.html",{"context":context})
    except Exception as e:
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
                        id_movement=int(refund_product.get("RefundProduct"))
                        
                        note=refund_product.get("nota")
                        movement=Movement.objects.filter(id=id_movement)
                        if movement:
                            result=Movement.Refund(user=user,product=product,movement=movement,note=note)
                            if result == "OK0":
                                return SuccessProduct("Se han reembolsado {} {} {} con un importe de {}$".format(movement.lot,"Pares de " if pair_action else "Unidades de ",product.name,movement.lot * (product.pair_price if pair_action else product.unit_price)))
                            elif result == "OK1":
                                return WarningProduct(no_redirect=True,text="Se han reembolsado {} {} {} con un importe de {}$, el usuario {} no presentaba el dinero suficiente en la cuenta, se ha retirado todo el dinero del usuario".format(movement.lot,"Pares de " if pair_action else "Unidades de ",product.name,movement.lot * (product.pair_price if pair_action else product.unit_price),user.username))
                            elif result == "E0":
                                return ErrorProduct("No se han podido reembolsar {} {}".format(lot_refund,product.name))
                            elif result == "E1":
                                return ErrorProduct("No hay suficiente dinero en caja para reembolsar {} {}".format(lot_refund,product.name))
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
        date_day_filter=datetime.today().strftime("%Y-%m-%d")
        date_start_filter=date_day_filter
        date_end_filter=date_day_filter
        q=Q()
        if request.method  == "POST":
            if "FilterMovement" in request.POST:
                filter_movement=request.POST.dict()
                type_filter=filter_movement.get("TypeFilter")
                product_filter=filter_movement.get("ProductFilter")
                date_filter=filter_movement.get("FilterDate")
                #print(type_filter,product_filter,date_filter)
                if date_filter ==  "DD":
                    date_day_filter=filter_movement.get("FilterDateDay")
                    #print(date_day_filter)
                    q = q & Q(date__date=date_day_filter)
                elif date_filter ==  "RD":
                    date_start_filter=filter_movement.get("FilterDateStart")
                    start_date=date_start_filter
                    date_end_filter=filter_movement.get("FilterDateEnd")
                    end_date=date_end_filter
                    q = q & Q(date__range=(start_date,end_date))
                if product_filter != "NF":
                    q = q & Q(product__id=product_filter)
                    #product_filter=int(product_filter)
                if type_filter != "NF":
                    q = q & Q(type=type_filter)
        movements=Movement.objects.filter(q).order_by('-date')[:20] 
        product_filter_name=None
        if product_filter!="NF":
            product_filter_name=Product.objects.get(id=product_filter)
        #print(product_filter_name,product_filter)
        products=Product.objects.all().exclude(removed=True).values("id","name")
        date_today_max =datetime.today() + timedelta(days=1)
        return render(request,"Operaciones.html",{"product_filter_name":product_filter_name,"MChoise":MChoise,"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"date_filter":date_filter,"products":products})
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')
