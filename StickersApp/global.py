from .models import RegisteCash,Visits,SummaryDate
#from datetime import datetime

def GlobalElements(request):
    visits=Visits.objects.first()  
    registe_cash_money=RegisteCash.objects.first()
    summary_date=SummaryDate.objects.first()
    #if request.user.is_superuser:
    #    groups=("Admin","Worker","Users")
    #else:
    #    groups=request.user.groups.values_list('name',flat=True)
    
    
    if not visits:
        visits=Visits()
        visits.save()

    if not registe_cash_money:
        registe_cash_money=RegisteCash()
        registe_cash_money.save()
    if not summary_date:
        summary_date=SummaryDate()
        summary_date.save()
    return {"global_context":{"registe_cash_money":registe_cash_money,"visits":visits,"summary_date":summary_date}}
    
