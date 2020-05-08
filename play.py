import re

a = re.match(r'.*(\d{4}).*', 'asdd asdasd (1892) ')
print(a[1])
