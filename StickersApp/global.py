from .models import RegisteCash,Visits,SummaryDate
#from datetime import datetime

version="1.6.3.3"

def GlobalElements(request):
    visits=Visits.objects.first()  
    registe_cash=RegisteCash.objects.first()
    summary_date=SummaryDate.objects.first()
    #if request.user.is_superuser:
    #    groups=("Admin","Worker","Users")
    #else:
    #    groups=request.user.groups.values_list('name',flat=True)
    
    
    if not visits:
        visits=Visits()
        visits.save()

    if not registe_cash:
        registe_cash=RegisteCash()
        registe_cash.save()
    if not summary_date:
        summary_date=SummaryDate()
        summary_date.save()
    return {"global_context":{"registe_cash":registe_cash,"visits":visits,"summary_date":summary_date,"version":version}}
    
