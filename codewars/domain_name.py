def domain_name(url):
    if url.split('/')[0]=='http:' or url.split('/')[0]=='https:':
        domain = url.split('/')[2];
    else:
        domain = url.split('/')[0];
    if domain.split('.')[0] == 'www':
        domain = domain.split('.')[1]
    else:
        domain=domain.split('.')[0]
    return domain

a=domain_name("github.com/carbonfive/raygun")
print(a)
#== "github"
b=domain_name("http://www.zombie-bites.com")
print(b)
#== "zombie-bites"
c=domain_name("https://www.cnet.com")
#== "cnet"
print(c)




'''  
def domain_name(url):
    return url.split("//")[-1].split("www.")[-1].split(".")[0]

'''