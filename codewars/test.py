import re
s = '+1-503-555-00910'
if re.match(r'^\+1-\d{3}-\d{3}-\d{4}$',s,flags=0):
    print(s)
