from .models import RegisteCash
from datetime import datetime
def UserGroups(request):
    groups=[]
    for group  in  request.user.groups.all():
        groups += {group.name}
    if groups:
        return {"Groups":groups}
    return {}

def GlobalElements(request):
    registe_cash=RegisteCash.objects.all().first()
    if registe_cash:
        return {"registe_cash":registe_cash}
    return {}
