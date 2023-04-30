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