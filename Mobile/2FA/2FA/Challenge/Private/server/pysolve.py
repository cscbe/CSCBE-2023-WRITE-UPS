
import hashlib
def Sha512Hash(pwd):
    return  hashlib.sha512(pwd.encode('utf-8')).hexdigest()

# a + pin + c + hardcoded
hardcoded = "de287e29a4a38788ba96136d6c2f21d0"

a = "fb2cc6e6d852e2511e1a83f6308e8b92"
c = "046cb1151f64c420cfce01208ed915f4"
b = "51c920909204ae2cd675f20b9e7237a651d693ff0fd4955d15e6c6c2a028b70093c793b4b857dc4024fb141bf673f512cd0348be5c8c25c32560de428ad39276"

# sol = Sha512Hash(a + pin + c + hardcoded)
for i in range(100000, 999999):
    if Sha512Hash(a + str(i) + c + hardcoded) == b:
        print(i)