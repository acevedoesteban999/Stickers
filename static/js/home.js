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