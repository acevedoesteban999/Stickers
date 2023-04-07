var SearchBool=false
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
        //body: JSON.stringify({ "SearchValue": SearchValue})
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
    console.log(VentasParesBool)
    if(VentasParesBool==false)
    {
        paredId.setAttribute("style","display:none;");
        paresPrecio.require=false;
        presGanancia.required=false;
    }
    else
    {
        paredId.removeAttribute("style");
        paresPrecio.require=true;
        presGanancia.required=true;
    }
}
