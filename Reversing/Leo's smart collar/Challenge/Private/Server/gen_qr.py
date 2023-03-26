import pyotp
import time
import io
import qrcode


totp = pyotp.TOTP("TNVZCHWFIKYG553JHZQ5Y2ARPIWDV6NP")
totp_url = totp.provisioning_uri(
    name="http://54.154.248.144/", issuer_name="LEO'S COLLAR"
)
qr = qrcode.QRCode()
qr.add_data(totp_url)
mat = qr.get_matrix()
print(len(mat), len(mat[0]))
new_arr = f"const int s[{len(mat)}][{len(mat[0])}] = " + "{"
for i, x in enumerate(mat):
    new_arr += "{"
    for j, y in enumerate(x):
        new_arr += str(int(y))
        if len(x) - 1 == j:
            new_arr += ""
        else:
            new_arr += ","
    if len(mat) - 1 == i:
        new_arr += "}"
    else:
        new_arr += "},"
new_arr += "};"
print(new_arr)
# qr.print_tty()
# print(totp.now())
# OTP verified for current time
# while True:
#    time.sleep(30)
#    print(totp.now())
