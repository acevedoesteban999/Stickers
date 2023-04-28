var SearchBool=false
var ResumeBool=false
function IputIdOfOperation()
{
    value_id=document.getElementById("IdInputOperation").value
    if (value_id)
    {
        document.getElementById("SelectTypeId").disabled=true;
        document.getElementById("ImputIdProduct").disabled=true;
        document.getElementById("SelectUserId").disabled=true;
        document.getElementById("InputDateID0").disabled=true;
        document.getElementById("InputDateID1").disabled=true;
        document.getElementById("InputDateID2").disabled=true;
        document.getElementById("filter__day").disabled=true;
        document.getElementById("filter__start").disabled=true;
        document.getElementById("filter__end").disabled=true;
    }
    else
    {
        document.getElementById("SelectTypeId").disabled=false;
        document.getElementById("ImputIdProduct").disabled=false;
        document.getElementById("SelectUserId").disabled=false;
        document.getElementById("InputDateID0").disabled=false;
        document.getElementById("InputDateID1").disabled=false;
        document.getElementById("InputDateID2").disabled=false;
        document.getElementById("filter__day").disabled=false;
        document.getElementById("filter__start").disabled=false;
        document.getElementById("filter__end").disabled=false;
    }

}
function LoadTodayInfo(addr)
{
    fetch(addr, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "TodayInfo": true})
    })
    .then(response => response.text())
    .then(data => 
    {
        document.getElementById("IdDivTodayReadyInfo").innerHTML=data
        document.getElementById("IdDivTodayLoadingInfo").setAttribute("class","d-none")
        document.getElementById("IdDivTodayReadyInfo").setAttribute("class","d-block")
    })
    .catch(error => {
        //alert(error)
        console.log("Error:",error);
    });
}

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
    try {
        var filter_worker=document.getElementById("filter_worker").checked
        var filter_product=document.getElementById("filter_product").checked
            
    } catch (error) 
    {
        var filter_worker=null
        var filter_product=null  
    }
    var day_resume=document.getElementById("date_day").value;
    var week_resume=document.getElementById("week_resume_input").value;
    var start_date=document.getElementById("start_date").value
    var end_date=document.getElementById("end_date").value
    
    document.getElementById("idSpinerResume").removeAttribute("style")
    document.getElementById("idInfoResume").setAttribute("style","display: none;")
    fetch(addr, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ 
            "FilterResumeValue": value,
            "start_date_resume":start_date,
            "end_date_resume":end_date,
            "week_resume":week_resume,
            "day_resume":day_resume,
            "filter_worker":filter_worker,
            "filter_product":filter_product,
        })
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
        alert(error)
    });

    ResumeBool=false;

}
function FilterResumeFunct(bool_card=false,day_today=false,this_week=false)
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
        document.getElementById("DivIDDate").setAttribute("style","display: none;");
        document.getElementById("DivIDWeek").setAttribute("style","display: none;");
        document.getElementById("DivIDMonth").setAttribute("style","display: none;");
        document.getElementById("DivIDDay").removeAttribute("style");
        document.getElementById("filter_worker").checked=false;
        document.getElementById("filter_product").checked=false;
    }
    else if(value==2)
    {
        if(this_week != false)
            document.getElementById("week_resume_input").value=this_week;
        document.getElementById("DivIDDay").setAttribute("style","display: none;");
        document.getElementById("DivIDDate").setAttribute("style","display: none;");
        document.getElementById("DivIDMonth").setAttribute("style","display: none;");
        document.getElementById("DivIDWeek").removeAttribute("style");
        document.getElementById("filter_worker").checked=false;
        document.getElementById("filter_product").checked=false;
    }
    else if(value==3)
    {
        document.getElementById("DivIDDay").setAttribute("style","display: none;");
        document.getElementById("DivIDWeek").setAttribute("style","display: none;");
        document.getElementById("DivIDMonth").setAttribute("style","display: none;");
        document.getElementById("DivIDDate").removeAttribute("style");
        document.getElementById("filter_worker").checked=false;
        document.getElementById("filter_product").checked=false;
    }
    else
    {
        document.getElementById("DivIDDay").setAttribute("style","display: none;");
        document.getElementById("DivIDWeek").setAttribute("style","display: none;");
        document.getElementById("DivIDDate").setAttribute("style","display: none;");
        document.getElementById("DivIDMonth").removeAttribute("style");
        document.getElementById("filter_worker").checked=false;
        document.getElementById("filter_product").checked=false;
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
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Ha ocurrido un Error al Verificar";
                alert("Ha ocurrido un Error al Verificar");
            }
            else if (data == "E1" )
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, Id:"+idRefund+" no existente";
                alert("Error, Id:"+idRefund+" no existente");
            }
            else if (data == "E2")
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, Operacion de Id:"+idRefund+" no es de tipo Venta";
                alert("Error, Operacion de Id:"+idRefund+" no es de tipo Venta");
            }
            else if (data == "E3")
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, El Producto de la Operacion de Id:"+idRefund+" no Coincide con el Producto en la Pagina ";
                alert("Error, El Producto de la Operacion de Id:"+idRefund+" no Coincide con el Producto en la Pagina");
            }
            else if (data == "E4")
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, La Operacion de Id:"+idRefund+" ya ha sido Reembolsada";
                alert("Error, La Operacion de Id:"+idRefund+" ya ha sido Reembolsada");
            }
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
            alert(error)
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
            alert(error)
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
