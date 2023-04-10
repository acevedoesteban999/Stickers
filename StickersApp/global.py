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
    visits=Visits.objects.values_list('total_visits').first()  
    registe_cash=RegisteCash.objects.values_list('money').first()
    groups=request.user.groups.values_list('name',flat=True)
    
    if not visits:
        visits=Visits()
        visits.save()

    if not registe_cash:
        registe_cash=RegisteCash()
        registe_cash.save()
    
    return {"registe_cash":registe_cash,"Groups":groups,"visits":visits}
    
