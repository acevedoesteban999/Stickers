var SearchBool=false
var ResumeBool=false
// function  CalcMoneyNextonth(total_money)
// {
//     money_next=total_money-parseInt(document.getElementById("retire_money_close_month").value);
//     if (money_next<0)
//         document.getElementById("NextMonthInitColor").setAttribute("class","h5 text-danger");   
//     else if( money_next>0)
//         document.getElementById("NextMonthInitColor").setAttribute("class","h5 text-success");
//     else if (money_next==0)
//         document.getElementById("NextMonthInitColor").setAttribute("class","h5 text-dark");
//     else
//     {
//         money_next="";
//         document.getElementById("NextMonthInitColor").setAttribute("class","h5 text-dark");
//     }
//     document.getElementById("NextMonthInit").innerHTML=money_next;
// }
function ContiueCloseMoth()
{
    document.getElementById("idDivMonthOKNo0").setAttribute("class","col-auto d-none")
    document.getElementById("idDivMonthNoOK0").setAttribute("class","col-auto d-block")
    document.getElementById("DivIdRowOKNo0").setAttribute("class","row d-none")
    document.getElementById("DivOdRowNoOk0").setAttribute("class","row d-block")
}
function SolicResumInfo(addr)
{
    if(ResumeBool == true)
        return
    ResumeBool=true;
    var value=0;
    var radios=document.getElementsByName("FilterResume");
    radios.forEach(element => {    
        if (element.checked == true)
            value=element.value;
            return;        
    });
    var date_resume=document.getElementById("date_day").value;
    var week_resume=document.getElementById("week_resume_input").value;
    var start_date_month=document.getElementById("date_month_start_date").value
    var end_date_month=document.getElementById("date_month_end_date").value
    document.getElementById("idSpinerResume").removeAttribute("style")
    document.getElementById("idInfoResume").setAttribute("style","display: none;")
    fetch(addr, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "FilterResumeValue": value,"start_date_month":start_date_month,"end_date_month":end_date_month,"week_resume":week_resume,"date_resume":date_resume})
    })
    .then(response => response.text())
    .then(data => 
    {
        document.getElementById("idSpinerResume").setAttribute("style","display: none;");
        document.getElementById("idInfoResume").removeAttribute("style");
        document.getElementById("idInfoResume").innerHTML=data;
        
    })
    .catch(error => {
        document.getElementById("idSpinerResume").setAttribute("style","display: none;")
        document.getElementById("idInfoResume").removeAttribute("style")
        document.getElementById("idInfoResume").innerHTML="Error, Ha ocurrido un error"
        console.log("Error:",error);
    });

    ResumeBool=false;

}
function FilterResumeFunct(bool_card=false,day_today=false,this_week=false,strat_date=false,end_date=false)
{
    var value=bool_card;
    var radios=document.getElementsByName("FilterResume");
    radios.forEach(element => {
        if (bool_card != false)
            if (bool_card == element.value)
                element.checked=true;
            else
                element.checked=false;
        else
            if (element.checked == true)
                value=element.value;
                return;        
    });
    if(value==1)
    {
        if(day_today != false)
            document.getElementById("date_day").value=day_today;
        document.getElementById("DivIDWeek").setAttribute("style","display: none;");
        document.getElementById("DivIDDay").removeAttribute("style");
        document.getElementById("DivIDMonth").setAttribute("style","display: none;");
        document.getElementById("DivIDDay").required=true;
        document.getElementById("DivIDWeek").required=false;
    }
    else if(value==2)
    {
        if(this_week != false)
            document.getElementById("week_resume_input").value=this_week;
        document.getElementById("DivIDDay").setAttribute("style","display: none;");
        document.getElementById("DivIDMonth").setAttribute("style","display: none;");
        document.getElementById("DivIDWeek").removeAttribute("style");
        document.getElementById("DivIDWeek").required=true;
        document.getElementById("DivIDDay").required=false;
    }
    else
    {
        if (strat_date != false && end_date != false)
        {
            document.getElementById("date_month_start_date").value=strat_date;
            document.getElementById("date_month_end_date").value=end_date;
        }
        document.getElementById("DivIDDay").setAttribute("style","display: none;")
        document.getElementById("DivIDWeek").setAttribute("style","display: none;")
        document.getElementById("DivIDMonth").removeAttribute("style");
        document.getElementById("DivIDWeek").required=false
        document.getElementById("DivIDDay").required=false
    }
}
function VerifRefund(addr,product_id)
{
    idRefund=document.getElementById("inputIdVerifRefund").value;
    document.getElementById("IdSpiner").setAttribute("class","d-block");
    document.getElementById("DivIdInfoRefundAjax").innerHTML="";
    document.getElementById("RefundProductButton").disabled=true;
    fetch(addr, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "VerifRefundIdMovement": idRefund,"product_id":product_id})
        })
        .then(response => response.text())
        .then(data => 
        {
            document.getElementById("IdSpiner").setAttribute("class","d-none");
            if (data == "E0" )
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Ha ocurrido un Error al Verificar";
            else if (data == "E1" )
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, Id:"+idRefund+" no existente";
            else if (data == "E2")
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, Operacion de Id:"+idRefund+" no es de tipo Venta";
            else if (data == "E3")
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, El Producto de la Operacion de Id:"+idRefund+" no Coincide con el Producto en la Pagina ";
            else if (data == "E4")
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, La Operacion de Id:"+idRefund+" ya ha sido Reembolsada";
            else
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML=data;
                document.getElementById("RefundProductButton").disabled=false;       
            }
        })
        .catch(error => {
            document.getElementById("IdSpiner").setAttribute("class","d-none");
            console.log("Error:",error);
            document.getElementById("DivIdInfoRefundAjax").innerHTML="Ha ocurrido un Error al Verificar";
        });
}
function onPairAddUni()
{
    pair_add_unit=document.getElementById("PairAddUni").checked;
    
    if (pair_add_unit)
    {
        document.getElementById("divIdCantUni").removeAttribute("style");
        document.getElementById("PairAddUnitInput").required=true;
        document.getElementById("idPairLotInput").min=0;

    }
    else
    {
        document.getElementById("divIdCantUni").setAttribute("style","display: none") ;
        document.getElementById("PairAddUnitInput").required=false;
        document.getElementById("idPairLotInput").min=1;
    }
    console.log(document.getElementById("PairAddUnitInput").min)
}
function SearchProduct(addr)
{
    if (SearchBool == true)
        return
    SearchBool=true;
    var SearchValue=document.getElementById('SearchProductID').value;
    fetch(addr, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "SearchValue": SearchValue})
        })
        .then(response => response.text())
        .then(data => 
        {
            if( data == "NoProducts")
                if (SearchValue)
                    data="Producto "+SearchValue+" inexistente";
                else   
                    data=""
            document.getElementById('searchProductList').innerHTML=data;
            
        })
        .catch(error => {
        console.log("Error:",error)
        });
    setTimeout(()=>{ SearchBool=false;} ,100)    
    
}
function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}    
function PrevImg()
{
    var [file] = document.getElementById('inputImgPre').files
    var img=document.getElementById("imgPre")
    img.width=200
    img.height=200
    img.src = window.URL.createObjectURL(file)
    document.getElementById("ButtonImgPree").removeAttribute("style")
    
}
function RemImg()
{
    document.getElementById("ButtonImgPree").setAttribute("style","display: none;")
    var img=document.getElementById('imgPre')
    img.src = ""
    img.width=0
    img.height=0
    var div=document.getElementById("ImgDiv")
    var input=document.getElementById("divid")
    div.removeChild(input)
    input=document.createElement("div")
    input.id="divid"
    input.innerHTML="<input onchange=\"PrevImg()\" type=\"file\"  class=\"form-control \" name=\"imagen\" id=\"inputImgPre\" placeholder=\"Imagen\">"
    div.appendChild(input)
}
function PrevImgCat()
{
    var [file] = document.getElementById('inputImgPreCat').files
    var img=document.getElementById("imgPreCat")
    img.width=200
    img.height=200
    img.src = window.URL.createObjectURL(file)
    document.getElementById("ButtonImgPreeCat").removeAttribute("style")
    
}
function RemImgCat()
{
    document.getElementById("ButtonImgPreeCat").setAttribute("style","display: none;")
    var img=document.getElementById('imgPreCat')
    img.src = ""
    img.width=0
    img.height=0
    var div=document.getElementById("ImgDivCat")
    var input=document.getElementById("dividCat")
    div.removeChild(input)
    input=document.createElement("div")
    input.id="dividCat"
    input.innerHTML="<input onchange=\"PrevImgCat()\" type=\"file\"  class=\"form-control \" name=\"imagen\" id=\"inputImgPreCat\" placeholder=\"Imagen\">"
    div.appendChild(input)
}
function FilterTime(choiseFilterTime) 
{
    var RD=document.getElementById("RD")
    var DD=document.getElementById("DD")
    var FD=document.getElementById("filter__day")
    var FS=document.getElementById("filter__start")
    var FE=document.getElementById("filter__end")
    if(choiseFilterTime == "NF")
    {
        
        RD.setAttribute("style","display: none") 
        DD.setAttribute("style","display: none")
        FD.required=false
        FS.required=false
        FE.required=false  
    }
    else if(choiseFilterTime == "DD")
    {
        
        DD.removeAttribute("style")
        FD.setAttribute("required","")
        FD.required=true
        RD.setAttribute("style","display: none")
        FS.required=false
        FE.required=false    
        
    }
    else
    {
        FS.setAttribute("required","")
        FE.setAttribute("required","")
        FS.required=true
        FE.required=true
        DD.setAttribute("style","display: none")
        FD.required=false
        RD.removeAttribute("style")
             
                          
    }
}
function VentasParesFunction(VentasParesBool)
{
    paredId=document.getElementById("ParesDivId");
    paresPrecio=document.getElementById("ParesPrecio");
    presGanancia=document.getElementById("ParesGanancia");
    ParesGananciaTrabajador=document.getElementById("ParesGananciaTrabajador");
    console.log(VentasParesBool)
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
