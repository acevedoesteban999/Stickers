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
    registe_cash=RegisteCash.objects.all().first()
    visits=Visits.objects.first()
    groups=[]
    
    for group  in  request.user.groups.all():
        groups += {group.name}
    
    if not visits:
        visits=Visits()
        visits.save()

    if not registe_cash:
        registe_cash=RegisteCash()
        registe_cash.save()
    return {"registe_cash":registe_cash,"Groups":groups,"visits":visits}
    
