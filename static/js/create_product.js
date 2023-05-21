//var color=null;
//var subcategory_name=null;
var ventas_pares=null
// function SetColor(color_select,subcategory_name)
// {
//     if (color_select != "NC")
//         color=color_select;
//     else 
//         color=null;
//     EditNombreAlmacenar()
// }

// function SetSubCategoryName(subcategory_name_)
// {
//     subcategory_name=subcategory_name_;
// }

// function EditNombreAlmacenar()
// {
//      var name=document.getElementById("nameProduct").value;
//      var color_="";
//      if (subcategory_name == null)
//          return;
//      if (color != null)
//          color_=color
//      var total_name =name+" "+subcategory_name
//      if (color_) 
//          total_name+=" "+color_
//      document.getElementById("IdNombreAlmacenar").innerHTML=total_name;
//      document.getElementById("IdNombreAlmacenarHidden").value=total_name;
// }

function VentasParesFunction(VentasParesBool)
{
    paredId=document.getElementById("ParesDivId");
    unidtId=document.getElementById("UnitDivId");
    paresPrecio=document.getElementById("ParesPrecio");
    presGanancia=document.getElementById("ParesGanancia");
    paresGananciaTrabajador=document.getElementById("ParesGananciaTrabajador");
    unitPrecio=document.getElementById("UnidadesPrecio");
    unitGanancia=document.getElementById("UnidadesGanancia");
    unitGananciaTrabajador=document.getElementById("UnidadesGananciaTrabajador");
    paresPrecio.value=null;
    presGanancia.value=null;
    paresGananciaTrabajador.value=null;
    unitPrecio.value=null;
    unitGanancia.value=null;
    unitGananciaTrabajador.value=null   ;
    if (VentasParesBool==null)
    {
        paredId.removeAttribute("style");
        paresPrecio.required=true;
        presGanancia.required=true;
        paresGananciaTrabajador.required=true;

        unidtId.removeAttribute("style");
        unitPrecio.required=true;
        unitGanancia.required=true;
        unitGananciaTrabajador.required=true;
    }
    else if(VentasParesBool==false)
    {
        paredId.setAttribute("style","display: none;"); 
        paresPrecio.required=false;
        presGanancia.required=false;
        paresGananciaTrabajador.required=false;

        unidtId.removeAttribute("style");
        unitPrecio.required=true;
        unitGanancia.required=true;
        unitGananciaTrabajador.required=true;
    }
    else
    {
        paredId.removeAttribute("style");
        paresPrecio.required=true;
        presGanancia.required=true;
        paresGananciaTrabajador.required=true;

        unidtId.setAttribute("style","display: none;"); 
        unitPrecio.required=false;
        unitGanancia.required=false;
        unitGananciaTrabajador.required=false;
    }
}

function CalcGain(pair,write_profit=null)
{
    
    var pair_sells=null;
    
        
    document.getElementsByName("VentasPares").forEach(element => {
        if (element.checked == true)
        {
            pair_sells=element.value;
            return;
        }
    });
    var purchase_price=document.getElementById("PrecioCompra");
    var pair_price=document.getElementById("ParesPrecio");
    var pair_profit=document.getElementById("ParesGanancia");
    var pair_profit_worker=document.getElementById("ParesGananciaTrabajador");
    var unit_price=document.getElementById("UnidadesPrecio");
    var unit_profit=document.getElementById("UnidadesGanancia");
    var unit_profit_worker=document.getElementById("UnidadesGananciaTrabajador");
  
    if ( ! purchase_price.value || (pair==true && !pair_price.value ) || (pair==false && !unit_price.value ) || (pair==null && (!unit_price.value || !pair_price.value ) ) )
        return ;

    var profit=null;
    if (pair_sells=="0")
    {
        profit=unit_price.value-purchase_price.value;
    }
    else if (pair_sells=="1")
    {
        profit=pair_price.value-purchase_price.value;
    }
    else
    {
        if (pair==false)
            profit=unit_price.value-purchase_price.value;
        else
            profit=pair_price.value-purchase_price.value;
    }
    console.log("profit",profit);

    if (profit <= 0)
    {
        purchase_price.setAttribute("class","form-control text-danger");
        if (pair==true)
            pair_price.setAttribute("class","form-control text-danger");
        else
            unit_price.setAttribute("class","form-control text-danger");
        return;
    }
    purchase_price.setAttribute("class","form-control");
    if (pair==true)
        pair_price.setAttribute("class","form-control");
    else
        unit_price.setAttribute("class","form-control");

    if (pair==true)
    {
        

        if (write_profit==true)
        {
            if (!pair_profit.value)
            {
                pair_profit_worker.value=null
                return
            }
            pair_profit_worker.value=profit-pair_profit.value
            if (pair_profit_worker.value<=0)
            {
                pair_profit_worker.setAttribute("class","form-control text-danger");
                pair_profit.setAttribute("class","form-control text-danger");
            }
            else
            {
                pair_profit_worker.setAttribute("class","form-control");
                pair_profit.setAttribute("class","form-control");
            }
        }
        else if (write_profit==false)
        {
            if (!pair_profit_worker.value)
            {
                pair_profit.value=null
                return
            }
            pair_profit.value=profit-pair_profit_worker.value
            if (pair_profit.value<=0)
            {
                pair_profit.setAttribute("class","form-control text-danger");
                pair_profit_worker.setAttribute("class","form-control text-danger");
            }
            else
            {
                pair_profit.setAttribute("class","form-control");
                pair_profit_worker.setAttribute("class","form-control");
            }
        }
    }
    else if (pair==false)
    {
        if (write_profit==true)
        {
            if (!unit_profit.value)
            {
                unit_profit_worker.value=null
                return
            }
            unit_profit_worker.value=profit-unit_profit.value
            if (unit_profit_worker.value<=0)
            {
                unit_profit_worker.setAttribute("class","form-control text-danger");
                unit_profit.setAttribute("class","form-control text-danger");
            }
            else
            {
                unit_profit_worker.setAttribute("class","form-control");
                unit_profit.setAttribute("class","form-control");
            }
        }
        else if (write_profit==false)
        {
            if (!unit_profit_worker.value)
            {
                unit_profit.value=null
                return
            }
            unit_profit.value=profit-unit_profit_worker.value
            if (unit_profit.value<=0)
            {
                unit_profit.setAttribute("class","form-control text-danger");
                unit_profit_worker.setAttribute("class","form-control text-danger");
            }
            else
            {
                unit_profit.setAttribute("class","form-control");
                unit_profit_worker.setAttribute("class","form-control");
            }
        }
    }
}