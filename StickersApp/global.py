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
    visits=Visits.objects.values_list('total_visits',flat=True).first()  
    registe_cash=RegisteCash.objects.values_list('money',flat=True).first()
    if request.user.is_superuser:
        groups=("Admin","Worker","Users")
    else:
        groups=request.user.groups.values_list('name',flat=True)
    
    if not visits:
        visits=Visits()
        visits.save()

    if not registe_cash:
        registe_cash=RegisteCash()
        registe_cash.save()
    
    return {"registe_cash":registe_cash,"Groups":groups,"visits":visits}
    
