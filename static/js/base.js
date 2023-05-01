var SearchBool=false
var html5QrcodeScanner;
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

function ScanQR()
{
    html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 30, qrbox: 250 });
    html5QrcodeScanner.render(onScanSuccess);
}

function onScanSuccess(decodedText) {
    function isValidHttpUrl(string) {
        let url;
        try {
          url = new URL(string);
        } catch (_) {
          return false;
        }
        return url.protocol === "http:" || url.protocol === "https:";
    }
    if(isValidHttpUrl(decodedText))
    {
        html5QrcodeScanner.clear().then(()=>{
            window.location = decodedText
        });
        
    }
    else
    {

        document.getElementById("buttonCloseScan").click();
        document.getElementById("IdErrorScanDiv").setAttribute("class","text-danger d-block h4 text-center");
        document.getElementById("idSearch").click();
        setTimeout(()=>{ document.getElementById("IdErrorScanDiv").setAttribute("class","d-none");} ,5000) 
    }
        
}
function CloseScanModal()
{
    html5QrcodeScanner.clear().then(()=>{  
    });
}