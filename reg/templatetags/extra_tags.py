from django.template import Library
from hashids import Hashids

register = Library()
hashvalue = Hashids(salt='2016-08-18 16:27:22 IiTNmll0 ATn1ViSu', alphabet='123456789abdefghijmdncklopqrstuvwxy0', min_length=7)

@register.filter(name='hash_id')
def hash_id(value):
	return hashvalue.encode(int(value))