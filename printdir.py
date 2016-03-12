from app.models import *
from app.forms import *

p = Post.objects.all()

print p.taged.tags