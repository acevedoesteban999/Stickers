from .models import RegisteCash,Visits
from datetime import datetime
def UserGroups(request):
    # groups=[]
    # for group  in  request.user.groups.all():
    #     groups += {group.name}
    # if groups:
    #     return {"Groups":groups}
    return {}

def GlobalElements(request):
    visits=Visits.objects.first()  
    registe_cash_money=RegisteCash.objects.first()
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
        
    return {"registe_cash_money":registe_cash_money,"visits":visits}
    
