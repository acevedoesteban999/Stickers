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
var html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 30, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);
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
        html5QrcodeScanner.clear()
        window.location = decodedText
    }
    else
    {
       
        html5QrcodeScanner.clear().then(()=>{
            html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 30, qrbox: 250 });
            html5QrcodeScanner.render(onScanSuccess);
            document.getElementById("IDErrorScan").setAttribute("class","text-danger h3 text-center p-2 m-2 d-block");
        });
        
        
    }
        
}
