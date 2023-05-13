function SubmitReplica()
{
    document.getElementById("IDFormREplica").submit()
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
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, Operación de Id:"+idRefund+" no es de tipo Venta";
                alert("Error, Operación de Id:"+idRefund+" no es de tipo Venta");
            }
            else if (data == "E3")
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, El Producto de la Operación de Id:"+idRefund+" no Coincide con el Producto en la Pagina ";
                alert("Error, El Producto de la Operación de Id:"+idRefund+" no Coincide con el Producto en la Pagina");
            }
            else if (data == "E4")
            {
                document.getElementById("DivIdInfoRefundAjax").innerHTML="Error, La Operación de Id:"+idRefund+" ya ha sido Reembolsada";
                alert("Error, La Operación de Id:"+idRefund+" ya ha sido Reembolsada");
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