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
    paresPrecio=document.getElementById("ParesPrecio");
    presGanancia=document.getElementById("ParesGanancia");
    ParesGananciaTrabajador=document.getElementById("ParesGananciaTrabajador");
    if(VentasParesBool==false)
    {
        paredId.setAttribute("style","display:none;");
        paresPrecio.require=false;
        presGanancia.required=false;
        ParesGananciaTrabajador.required=false;
    }
    else
    {
        paredId.removeAttribute("style");
        paresPrecio.require=true;
        presGanancia.required=true;
        ParesGananciaTrabajador.required=true;
    }
}