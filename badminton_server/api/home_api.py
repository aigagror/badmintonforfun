from .models import *


def get_announcement():
    models.Manager('SELECT * FROM Announcement')