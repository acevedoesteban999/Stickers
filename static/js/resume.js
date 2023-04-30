var ResumeBool=false
function ContiueCloseMoth(){
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