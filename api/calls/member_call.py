from ..models import *
from ..cursor_api import *

def get_all_members():
    all = Member.objects.raw("SELECT * FROM api_member")
    serializeSetOfModels(all)