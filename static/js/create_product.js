var color=null;
var subcategory_name=null;
function SetColor(color_select,subcategory_name)
{
    if (color_select != "NC")
        color=color_select;
    else 
        color=null;
    EditNombreAlmacenar()
}
function SetSubCategoryName(subcategory_name_)
{
    subcategory_name=subcategory_name_;
}
function EditNombreAlmacenar()
{
    var name=document.getElementById("nameProduct").value;
    var color_="";
    if (subcategory_name == null)
        return;
    if (color != null)
        color_=color
    var total_name =name+" "+subcategory_name
    if (color_) 
        total_name+=" "+color_
    document.getElementById("IdNombreAlmacenar").innerHTML=total_name;
    document.getElementById("IdNombreAlmacenarHidden").value=total_name;
}

function VentasParesFunction(VentasParesBool)
{
    paredId=document.getElementById("ParesDivId");
    unidtId=document.getElementById("UnitDivId");
    paresPrecio=document.getElementById("ParesPrecio");
    presGanancia=document.getElementById("ParesGanancia");
    paresGananciaTrabajador=document.getElementById("ParesGananciaTrabajador");
    unitPrecio=document.getElementById("UnitPrecio");
    unitGanancia=document.getElementById("UnitGanancia");
    unitGananciaTrabajador=document.getElementById("UnitGananciaTrabajador");
    paresPrecio.value=0;
    presGanancia.value=0;
    paresGananciaTrabajador.value=0;
    unitPrecio.value=0;
    unitGanancia.value=0;
    unitGananciaTrabajador.value=0;
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

function CalcGain(pair)
{
    pair_sells=document.getElementById("VentasPares").value;
    purchase_price=document.getElementById("PrecioCompra").value
    pair_price=document.getElementById("ParesPrecio").value
    pair_profit.getElementById("ParesGanancia")
    pair_profit_worker.getElementById("ParesGananciaTrabajador")
    unit_price.getElementById("UnidadesPrecio").value
    unit_profit.getElementById("UnidadesGanancia")
    unit_profit_worker.getElementById("UnidadesGananciaTrabajador")
    

    // if ( ! purchase_price || (pair_sells=="0" && !pair_price ) || (pair_sells=="1" && !unit_price ) || (pair_sells=="2" && (!unit_price || !pair_price ) ) )
    //     return ;
    
    if ( ! purchase_price || (pair==false && !pair_price ) || (pair==true && !unit_price ) || (pair==null && (!unit_price || !pair_price ) ) )
        return ;

    if (pair==true)
    {
        
    }
    else if (pair==false)
    {

    }
    else
    {

    }
}