from .models import RegisteCash
from datetime import datetime
def UserGroups(request):
    groups=[]
    for group  in  request.user.groups.all():
        groups += {group.name}
    return  {"Groups":groups}

def GlobalElements(request):
    registe_cash=RegisteCash.objects.all().first()
    if registe_cash:
        return {"registe_cash":registe_cash,"year":datetime.today().year}
    pass
