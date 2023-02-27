
function AA()
{
    console.log("AA")
    const img=document.getElementById('imgPre')
    img.src = window.URL.createObjectURL(this.files[0])
}

    
function FilterTime1(choiseFilterTime) 
{
    const RD=document.getElementById("RD")
    const DD=document.getElementById("DD")
    const FD=document.getElementById("filter__day")
    const FS=document.getElementById("filter__start")
    const FE=document.getElementById("filter__end")
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

   