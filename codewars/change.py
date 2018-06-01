import re
def change(s, prog, version):
    s = s.split('\n')
    ls=len(s)
    ss =[]
    for j in s:
        i=j.split(':')
        if i[0] == 'Program title':
            i[0] = 'Program'
            i[1] = prog
            ss.append(i)
            continue
        if i[0] == 'Author':
            i[1] = 'g964'
            ss.append(i)
            continue
        # if i[0] == 'Corporation' or i[0] == 'Level':
        #     s.remove(j)
        if i[0] == 'Phone':
            i[1]=i[1].lstrip()
            if i[1] == '+1-503-555-0090':
                i[1] == '+1-503-555-0090'
                ss.append(i)
                continue
            if re.match(r'^\+1-[0-9]{3}-[0-9]{3}-[0-9]{4}$',i[1] , flags=0):
                i[1] = '+1-503-555-0090'
                ss.append(i)
                continue
            else:
                return "ERROR: VERSION or PHONE"
        if  i[0] == 'Date':
            i[1]="2019-01-01"
            ss.append(i)
            continue
        if i[0] == 'Version':
            if re.match(r'^\d(\.\d)?$',version,flags=0):
                i[1] = version##
                ss.append(i)
                continue
            elif re.match(r'^\d(\.\d)+',version,flags=0):
                i[1] = '2.0'
                ss.append(i)
                continue
            else:
                return "ERROR: VERSION or PHONE"
    cs = ''
    for i in ss:
        s3=i[0]+': '+i[1]+' '
        cs = cs +s3
    return cs.rstrip()


s1 = 'Program title: Primes\nAuthor: Kern\nCorporation: Gold\nPhone: +1-503-555-0091\nDate: Tues April 9, 2005\nVersion: 1.1\nLevel: Alpha'
s11 = 'Program title: Hammer\nAuthor: Tolkien\nCorporation: IB\nPhone: +1-503-555-0090\nDate: Tues March 29, 2017\nVersion: 2.0\nLevel: Release'
s12 = 'Program title: Primes\nAuthor: Kern\nCorporation: Gold\nPhone: +1-503-555-009\nDate: Tues April 9, 2005\nVersion: 6.7\nLevel: Alpha'


s1=change(s1, 'Ladder', '0')
print(s1)
#'Program: Ladder Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 1.1'
s2=change(s11, 'Balance', '1.5.6')
print(s2)
#'Program: Balance Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0'
s3=change(s12, 'Ladder', '1.1')
print(s3)
#'ERROR: VERSION or PHONE'



'Program: F Author: g964 Phone: +1-503-555-0090 Date:2019-01-01 Version:2 '
'Program: F Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2'
'Program: B Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2'



'Program: B Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 4 '
'Program: B Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 4'


'Program: P Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 0 '
'Program: P Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0'

'Program: C Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 3 '  'ERROR: VERSION or PHONE'


'Program: B Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2 '
'Program: B Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2'


'Program: L Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 6 '
'Program: L Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0'



'Program: Hammer Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 1.5'
'Program: Hammer Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0'


'Program: Balance Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0' \
'Program: Balance Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 1.5.6'



'Program: C Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 1' \
'Program: C Author: g964 Phone: +1-503-555-0090 Date: 2019-01-01 Version: 2.0'