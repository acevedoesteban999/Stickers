from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import MChoise,Product,RegisteCash,Movement,Category,Visits
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormProduc,FormLot,FormImg
from datetime import datetime ,timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
import json
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
            
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            if is_ajax:
                data = json.load(request)
                search_value = data.get('SearchValue')  
                try:
                    if search_value:
                        q=Q(removed=False) & (Q(name__contains=search_value) | Q(id__contains=search_value))
                        products=Product.objects.filter(q)[:5]
                        if products:
                            return render(None,"SearchProducts.html",{"products": products})
                except Exception as e:
                    print(e)
                return HttpResponse("NoProducts")
             
        return render(request,"Home.html")
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('productos')

def HomeView(request):
    if request.method=="GET":
        if "QR" in request.GET:
            visits=Visits.objects.first()
            visits.total_visits+=1
            visits.save()
        
        
    #try:
    #from django.db import connection
    #print(connection.queries)
    date=datetime.now() 
    #mov=Movement.objects.all()
    #print(mov.query)
    #ids=Movement.objects.select_related('product').values_list("id",flat=True)
    #print(ids)
    #return render(request,"Home.html")
    #movEP=Movement.objects.select_related('product').filter(date__day=date.day,type="EP").values_list('product__id',flat=True)
    #movVP=Movement.objects.select_related('product').filter(date__day=date.day,type="VP").values_list('product__id',flat=True)
    movEP=Movement.objects.filter(date__day=date.day,type="EP").values_list('product__id',flat=True)
    movVP=Movement.objects.filter(date__day=date.day,type="VP").values_list('product__id',flat=True)
    movM=Movement.objects.filter(date__day=date.day).order_by('-date')[:5]
    idsEP=[]
    idsVP=[]
    if movEP:
        for id in movEP:
            idsEP.append(id)
    if movVP:
        for id in movVP:
            idsVP.append(id)
    productsEP=Product.objects.filter(pk__in=idsEP).values('name','id').order_by('name')
    productsVP=Product.objects.filter(pk__in=idsVP).values('name','id').order_by('name')
    return render(request,"Home.html",{"productsEP":productsEP,"productsVP":productsVP,"movM":movM})
    #except :
    #    pass
    return HttpResponse("Ha ocurrido un error insesperado , contacte con los administradores")

def CajaView(request):
    
    try:
        user=request.user
        if user:
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
        else:
            messages.error(request,"Debe Iniciar Sesion para Aceeder a estos Recursos")    
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
        print(user)
        if user:
            products = Product.objects.exclude(removed=True).order_by('name')   

            if request.method == "POST":
                if "CrearProducto" in request.POST:
                    crear_form=request.POST.dict()
                    files=FormImg(request.POST,request.FILES)
                    files.is_valid()
                    name=crear_form.get("name").__str__().capitalize()
                    pair=crear_form.get("VentasPares")
                    if pair == "1":
                        pair=True
                    else:
                        pair=False
                    
                    unit_price=int(crear_form.get("precio unitario") )
                    unit_profit_worker=int(crear_form.get("ganancia unitaria") )
                    pair_price=None
                    pair_profit_worker=None
                    if pair == True:
                        pair_price=int(crear_form.get("precio pares"))
                        pair_profit_worker=int(crear_form.get("ganancia pares")) 
                    image=files.cleaned_data.get("imagen")
                    description=crear_form.get("descripcion")
                    result=Movement.Create(user=user,name=name,pair=pair,unit_price=unit_price,unit_profit_worker=unit_profit_worker,pair_price=pair_price,pair_profit_worker=pair_profit_worker,description=description,image=image)
                    if result==True:
                        crear_form=FormProduc()
                        product=Product.objects.exclude(removed=True).get(name=name)
                        messages.success(request,"Se ha creado  el objeto {} correctamente".format(name))
                        #return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys}) 
                        return redirect("/Producto/{}".format(product.id))
                    elif result=="E0":
                        messages.error(request,"Nose ha podido  crear, ya existe un objeto de nombre %s"% name)
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
        print(user)
        if user:
            if product :
                movements_confirm=Movement.objects.filter(product_id=product.id,type="EP",extra_info_bool=False).order_by('date')
                movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:10]
                categorys=Category.objects.filter(product__id=product.id).order_by("name")
                i=0
                for categ in categorys:
                    if(categ.image):
                        i += 1

                def NormalPageProduct():
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)}) 
                
                def ErrorProduct(text):
                    messages.error(request,text)
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)}) 
                
                def SuccessProduct(text):
                    #Eliminar si se redirecciona a 'home'
                    messages.success(request,text)
                    return render(request,"Producto.html",{'MovementsConfirm':movements_confirm,'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)}) 
                
                def WarningProduct(text):
                    messages.warning(request,text)
                    return redirect('home') 
                
                if request.method == "POST":
                    #Form Editar
                    if "EditProduct" in request.POST:
                        edit_product=request.POST.dict()
                        files=FormImg(request.POST,request.FILES)
                        files.is_valid()
                        name=edit_product.get("name")
                        pair_stored=None
                        pair_sold=None
                        pair_price=None
                        pair_profit_worker=None
                        if product.pair:
                            pair_stored=int(edit_product.get("almacenado pares"))
                            pair_sold=int(edit_product.get("vendido pares"))
                            pair_price=int(edit_product.get("precio pares"))
                            pair_profit_worker=int(edit_product.get("ganancia pares"))
                        unit_stored=int(edit_product.get("almacenado unitario"))
                        unit_sold=int(edit_product.get("vendido unitario"))
                        unit_price=int(edit_product.get("precio unitario"))
                        unit_profit_worker=int(edit_product.get("ganancia unitario"))
                        #price=edit_product.get("precio")
                        description=edit_product.get("descripcion")
                        image=files.cleaned_data.get("imagen")
                        result=Movement.Edit(user=user,product=product,
                                            name=name,
                                            pair_stored=pair_stored,
                                            pair_sold=pair_sold,
                                            pair_price=pair_price,
                                            pair_profit_worker=pair_profit_worker,
                                            unit_stored=unit_stored,
                                            unit_sold=unit_sold,
                                            unit_price=unit_price,
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
                        category_id=sell_product.get("CategorySelect")
                        pair_action=sell_product.get("AccionPar")
                        note=sell_product.get("nota")
                        #if pair_action:
                            #pair_action=True
                        category=None
                        if category_id:
                            category=categorys.get(id=category_id)
                        if pair_action:
                            result=Movement.Pair_Sell(user=user,product=product,lot=lot_sell,category=category,note=note)
                        else:
                            result=Movement.Unit_Sell(user=user,product=product,lot=lot_sell,category=category,note=note)
                        
                        if result == True or result== "OK0":
                            if category_id:
                                categorys=Category.objects.filter(product__id=product.id).order_by("name")
                            return SuccessProduct("Se han vendido {} {} {} {},con un importe de {}$".format(lot_sell,"pares de" if pair_action  else "unidades de",product.name,", se ha descontado una unidad de un lote par " if result=="OK0" else "",product.pair_price*lot_sell if pair_action  else product.unit_price*lot_sell))
                        elif result == 'E1':
                            return ErrorProduct("No se ha podido vender {} productos, en la categoría {} solo quedan {} {} productos almacenados".format(lot_sell,category.name,category.pair_stored.__str__() +" pares de" if pair_action  else category.unit_stored.__str__() +" unidades de"))
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
                        category_id=add_product.get("CategorySelect")
                        pair_action=add_product.get("AccionPar")
                        note=add_product.get("nota")
                        category_add=None
                        if category_id:
                            category_add=Category.objects.get(id=category_id)
                        if Movement.Add(user=user,product=product,lot=lot_add,category=category_add,pair_action=pair_action,note=note):
                            return SuccessProduct("Se ha agregado {} {} {}, esperando a ser confirmado".format(lot_add,"pares de " if pair_action else "unidades de ",product.name))
                        return ErrorProduct("No se han podido insertar {} {}".format(lot_add,product.name))
                    #Form Confirmar Agregar
                    elif "ConfirmAddProduct" in request.POST:
                        confirm_product=request.POST.dict()
                        lot_confirm=int(confirm_product.get("cantidad"))
                        id_movement=int(confirm_product.get("MovimientoID"))
                        note=confirm_product.get("nota")
                        if id_movement:
                            movement_to_confirm=Movement.objects.get(id=id_movement)
                            if movement_to_confirm:
                                if Movement.ConfirmAdd(user=user,movement=movement_to_confirm,lot=lot_confirm,note=note):
                                    try:
                                        for movementConfirm in movements_confirm:
                                            if movementConfirm.extra_info_bool == False:
                                                raise (Exception())
                                        categorys=Category.objects.filter(product__id=product.id).order_by("name")
                                        product=Product.objects.get(id=product.id)
                                        return SuccessProduct("Se han agregado {} {} correctamente".format(lot_confirm,movement_to_confirm.product.name))
                                    except:
                                        movement_to_confirm.product.confirm=False
                                        movement_to_confirm.product.save()
                                        return WarningProduct("Se han agregado {} {} correctamente, pero aun quedan confirmaciones".format(movement_to_confirm.lot,movement_to_confirm.product.name))
                        return ErrorProduct("No se han podido confirmar")
                    #Form Quitar
                    elif "SubProduct" in request.POST:
                        sub_product=request.POST.dict()
                        lot_sub=int(sub_product.get("cantidad"))
                        category_id=sub_product.get("CategorySelect")
                        pair_action=sub_product.get("AccionPar")
                        note=sub_product.get("nota")
                        category=None
                        if category_id:
                            category=Category.objects.get(id=category_id)
                        if pair_action:
                            result=Movement.Pair_Sub(user=user,product=product,lot=lot_sub,category=category,note=note)
                        else:
                            result=Movement.Unit_Sub(user=user,product=product,lot=lot_sub,category=category,note=note)
                        if result == True:
                            if category_id:
                                categorys=Category.objects.filter(product__id=product.id).order_by("name")
                            return SuccessProduct("Se han quitado {} {} {} correctamente".format(lot_sub,"Pares de " if pair_action else "Unidades de",product.name))
                        elif result == "E1":
                            return ErrorProduct("No se han podido quitar, la categoría {} solo tiene {} {} productos almcenados".format(category.name,category.pair_stored if pair_action else category.unit_stored,"Pares de " if pair_action else "Unidades de"))
                        elif result == "E0":
                            return ErrorProduct("No se han podido quitar {} {}".format(lot_sub,product.name))
                    #Form Reembolsar
                    elif "RefundProduct" in request.POST: 
                        refund_product=request.POST.dict()
                        lot_refund=int(refund_product.get("cantidad"))
                        category_id=refund_product.get("CategorySelect")
                        pair_action=refund_product.get("AccionPar")
                        note=refund_product.get("nota")
                        category=None
                        if category_id:
                            category=Category.objects.get(id=category_id)
                        if lot_refund > 0:
                            if pair_action:
                                result=Movement.Pair_Refund(user=user,product=product,lot=lot_refund,category=category,note=note)
                            else:
                                result=Movement.Unit_Refund(user=user,product=product,lot=lot_refund,category=category,note=note)
                            if result == True:
                                if category_id:
                                    categorys=Category.objects.filter(product__id=product.id).order_by("name")  
                                return SuccessProduct("Se han reembolsado {} {} {} con un importe de {}$".format(lot_refund,"Pares de " if pair_action else "Unidades de ",product.name,lot_refund * (product.pair_price if pair_action else product.unit_price)))
                            elif result == "E0":
                                return ErrorProduct("No se han podido reembolsar {} {}".format(lot_refund,product.name))
                            elif result == "E1":
                                return ErrorProduct("No hay suficiente dinero en caja para reembolsar {} {}".format(lot_refund,product.name))
                            elif result == "E2":
                                return ErrorProduct("No se ha podido  reembolsar, la categoría {} solo tiene {} {} productos vendidos".format(category.name,category.pair_sold if pair_action else category.unit_sold,"Pares de " if pair_action else "Unidades de "))                 
                    #Form Agregar Categoría
                    elif "AddCategory" in request.POST: 
                        add_category=request.POST.dict()
                        files=FormImg(request.POST,request.FILES)
                        files.is_valid()
                        name=add_category.get("name").__str__().capitalize()        
                        image=files.cleaned_data.get("imagen")
                        result=Movement.AddCategory(product,name,image)
                        if result == True:
                            categorys=Category.objects.filter(user=user,product__id=product.id).order_by("name")
                            i=0
                            for categ in categorys:
                                if(categ.image):
                                    i+=1
                            return SuccessProduct("Se ha creado la categoría {} correctamente".format(name))
                        elif result == "E0":
                            return ErrorProduct("Ya existe la categoría {}".format(name))
                        #return ErrorProduct("No se ha podido  crear la categoría {}".format(name))     
                    #Form Eliminar Categoría
                    elif "RemoveCategory" in request.POST: 
                        remove_category=request.POST.dict()
                        id=remove_category.get("RemoveCategorySelect")
                        category=Category.objects.get(id=id)
                        rf=Movement.RemoveCategory(id=id,p_id=product.id)
                        if rf == True:
                            categorys=Category.objects.filter(user=user,product__id=product.id).order_by("name")
                            i=0
                            for categ in categorys:
                                if(categ.image):
                                    i+=1
                            return SuccessProduct("Se ha eliminado la categoría {} correctamente".format(category.name))
                        return ErrorProduct("No se ha podido eliminar la categoría {}".format(category.name))
                    
                    return ErrorProduct("Ha ocurrido un error inesperado")    
                return NormalPageProduct()
        else:
            messages.error(request,"Debe Iniciar Sesion para Aceeder a estos Recursos")    
            return redirect('home') 
    except ObjectDoesNotExist:
        messages.error(request,"Error, producto inexistente")
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('productos')        

def TransaccionesView(request):
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
                if date_filter ==  "DD":
                    date_day_filter=filter_movement.get("FilterDateDay")
                    print(date_day_filter)
                    q = q & Q(date__date=date_day_filter)
                elif date_filter ==  "RD":
                    date_start_filter=filter_movement.get("FilterDateStart")
                    start_date=date_start_filter
                    date_end_filter=filter_movement.get("FilterDateEnd")
                    end_date=date_end_filter
                    q = q & Q(date__range=(start_date,end_date))
                if product_filter != "NF":
                    q = q & Q(product__id=product_filter)
                    product_filter=int(product_filter)
                if type_filter != "NF":
                    q = q & Q(type=type_filter)
        movements=Movement.objects.filter(q).order_by('-date')[:20] 
        products=Product.objects.all().exclude(removed=True).values("id","name")
        date_today_max =datetime.today() + timedelta(days=1)
        return render(request,"Transacciones.html",{"MChoise":MChoise,"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"date_filter":date_filter,"products":products})
    except Exception as e:
        print(e)
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')
