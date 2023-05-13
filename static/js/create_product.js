var color=null;
function SetColor(color_select,subcategory_name)
{
    if (color_select != "NC")
        color=color_select;
    else 
        color=null;
    EditNombreAlmacenar(subcategory_name)
}
function EditNombreAlmacenar(subcategory_name)
{
    var name=document.getElementById("nameProduct").value;
    var color_="";
    if (color != null)
        color_=color
    var total_name =name+" "+subcategory_name+" "+color_;
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