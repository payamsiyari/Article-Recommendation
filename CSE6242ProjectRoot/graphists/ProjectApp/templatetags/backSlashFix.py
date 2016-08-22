from django import template

register = template.Library()

@register.filter
def backSlashFix(value):
	if value is None:
		return "None"
	else:
		return value.encode('utf-8').replace("\\","`")