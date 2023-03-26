# 2FA

## Category
Mobile

## Estimated difficulty
Medium

## Description
It's an Android app that requires you to enter a 6 digit pincode to get the flag. There's a bunch of crypto going on behind the scenes. Every 30s the pincode changes.

## Scenario
Enter the correct PIN to get the flag. But you better hurry, since you only have 30 seconds!

## Write-up
Every 30 seconds a new vault is downloaded from the backend (http://99.81.5.42:9009/getvault). The return value is first decrypted with AES with the key `ca1111c9f4a92797`, which is hardcoded in the application. You can either create your own Java/python script to get the decrypted value, or we can use Frida to have the application do it for us:

```javascript
Java.perform(function(){

    let MainActivity = Java.use("be.dauntless.twofa.MainActivity");
    MainActivity["decrypt"].implementation = function (str) {
        let result = this["decrypt"](str);
        console.log(`MainActivity.decrypt result=${result}`);
        return result;
    };
});
```

```default
solution frida -U -f be.dauntless.twofa -l decrypt.js
     ____
    / _  |   Frida 16.0.1 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
   . . . .
   . . . .   Connected to SM G950F (id=ce02171255925c1b04)
Spawned `be.dauntless.twofa`. Resuming main thread!                     
[SM G950F::be.dauntless.twofa ]-> MainActivity.decrypt result=ZGV4CjAzNQAlQQBUVdtn6I3dvn+O58fN7M7lRRVrzpfgBwAAcAAAAHhWNBIAAAAAAAAAABwHAAAm
AAAAcAAAAAwAAAAIAQAACwAAADgBAAAEAAAAvAEAAA4AAADcAQAAAQAAAEwCAAB0BQAAbAIAAOoD
AAAMBAAALgQAADYEAAA5BAAAPAQAAEAEAABFBAAASQQAAGUEAACBBAAAmAQAAK0EAADBBAAA1QQA
APAEAAAPBQAAGAUAABsFAAAnBQAAKgUAAC4FAAAzBQAANwUAADoFAABCBQAARQUAAEgFAABLBQAA
TwUAAFcFAADaBQAA4gUAAJ0GAACnBgAAtAYAAL8GAADJBgAAAwAAAAgAAAAJAAAACgAAAAsAAAAM
AAAADQAAAA4AAAAPAAAAEQAAABMAAAAWAAAABAAAAAYAAAAAAAAABQAAAAYAAAC8AwAABgAAAAYA
AADEAwAABwAAAAYAAADMAwAABwAAAAcAAADMAwAABwAAAAgAAADMAwAAEQAAAAkAAAAAAAAAFAAA
AAoAAADUAwAAFQAAAAoAAADcAwAABAAAAAsAAAAAAAAABwAAAAsAAADkAwAAAQAGABcAAAABAAYA
GQAAAAEABgAaAAAAAQAGABsAAAABAAYAAgAAAAEAAwAXAAAAAQAIABcAAAABAAAAHAAAAAQAAgAk
AAAABQAGAAIAAAAGAAcAHwAAAAYACQAhAAAABgABACMAAAAHAAYAAgAAAAcABAAYAAAABwAAACQA
AAAIAAoAHQAAAAgABQAiAAAAAQAAAAEAAAAFAAAAAAAAABIAAACcAwAA+wYAAAAAAAABAAAA8wYA
AAIAAQABAAAA0AYAABQAAABwEAUAAQAaAAEAWxAAABoAAABbEAIAGgAeAFsQAQAaACAAWxADAA4A
BwACAAIAAADZBgAAMwAAABoAEABxEA0AAAAMAG4QBwAGAAwBbiAMABAADAEiAgcAcBAJAAIAEgAh
EzUwGQBIAwEA1TP/ANAzAAETBBAAcSAEAEMADAMSFG4gCABDAAwDbiAKADIA2AAAASjnbhALAAIA
DAARAAAABQADAAIAAADnBgAAKAAAACIABwBwEAkAAABUIQAAbiAKABAADABuIAoAMAAMAFQhAgBu
IAoAEAAMAG4gCgBAAAwAbhALAAAADABwIAEAAgAMAFQhAQBuIAYAEAAKAA8AAgABAAAAAADuBgAA
AwAAAFQQAwARAAAAAAAAAAAAAAACAAAAAAAAAAEAAABsAgAAAgAAAGwCAAABAAAAAAAAAAIAAAAA
AAAAAQAAAAYAAAABAAAABQAAAAIAAAAGAAYAAQAAAAsAIDM4NjBmODVjMjY1M2VmOWM2NjNjMzkw
ODdmY2I1MWI1ACA5NTkyMWZjZDU2NGY5MTM2ODIyZWJjYzE1MTIwOGFkMQAGPGluaXQ+AAFJAAFM
AAJMSQADTElJAAJMTAAaTGJlL2RhdW50bGVzcy90d29mYS9WYXVsdDsAGkxkYWx2aWsvYW5ub3Rh
dGlvbi9UaHJvd3M7ABVMamF2YS9sYW5nL0V4Y2VwdGlvbjsAE0xqYXZhL2xhbmcvSW50ZWdlcjsA
EkxqYXZhL2xhbmcvT2JqZWN0OwASTGphdmEvbGFuZy9TdHJpbmc7ABlMamF2YS9sYW5nL1N0cmlu
Z0J1aWxkZXI7AB1MamF2YS9zZWN1cml0eS9NZXNzYWdlRGlnZXN0OwAHU0hBLTUxMgABVgAKVmF1
bHQuamF2YQABWgACWkwAA1pMTAACW0IAAWEABmFwcGVuZAABYgABYwABZAACZGQABmRpZ2VzdACA
AWVlZTMzNTVjMWI0Y2IyNDg1ODZiOTNjZTMxNDgwNWI1OGFkOWNiMjk5MjM5ZTU4MzE0MmM1OWE2
ZWQ3ZmQxMmM4ZTIwYjVhNTc4NzgwNTQwYTI4N2VhOTg1ZTRhYzY2YzM2ZWIwN2VlOGE3YzVjYzdj
ZDk2Yzk0NmUwZDk0Nzk4AAZlcXVhbHMAuAFnQUFBQUFCa0FKekozN1NGNXFLbHdYRHd1T2JXNXpM
RHIzVTJUaEZ6WmxyN24teFdsd3AwcHZjUDJZM3EwVnZjRGZwN0NvemdWVi11bHdFal9OTDlCTFlv
M2JwSlRxcVVPZXk2SWJaLUFjaEp1cDh3TlZNbGVsQ0VfWm9yR2h0dlREV1llZXd0SHI2cEUxa2xU
b0NFTVpQQ1JVOVZnRnVKaTZVd0x2eWNHRWQxWVctRXRmRXV5MFk9AAhnZXRCeXRlcwALZ2V0SW5z
dGFuY2UACXN1YnN0cmluZwAIdG9TdHJpbmcABXZhbHVlAAcABw4+S0tMABwBAAcOaYdaSwEUDT8A
FgIAAAcOABEABw4AAgIBJRwBGAMABAICAAABAAEAAQEAgYAE9AQBAqwFAgGkBgEBhAcAAAAQAAAA
AAAAAAEAAAAAAAAAAQAAACYAAABwAAAAAgAAAAwAAAAIAQAAAwAAAAsAAAA4AQAABAAAAAQAAAC8
AQAABQAAAA4AAADcAQAABgAAAAEAAABMAgAAAxAAAAEAAABsAgAAASAAAAQAAAB0AgAABiAAAAEA
AACcAwAAARAAAAYAAAC8AwAAAiAAACYAAADqAwAAAyAAAAQAAADQBgAABCAAAAEAAADzBgAAACAA
AAEAAAD7BgAAABAAAAEAAAAcBwAA
```

We can use CyberChef to decode this and turn it into a binary file. The first few characters say `dex` and the app does indeed load this file using an `InMemoryClassLoader` to add additional functional to the application. After saving the file as a dex file, it can be opened in e.g. jadx-gui which will result in the following code:

```java
package be.dauntless.twofa;

import java.security.MessageDigest;

/* loaded from: /Users/jeroen/Downloads/payload (1).dex */
public class Vault {
    String a = "95921fcd564f9136822ebcc151208ad1";
    String c = "3860f85c2653ef9c663c39087fcb51b5";
    String b = "eee3355c1b4cb248586b93ce314805b58ad9cb299239e583142c59a6ed7fd12c8e20b5a578780540a287ea985e4ac66c36eb07ee8a7c5cc7cd96c946e0d94798";
    public String d = "gAAAAABkAJzJ37SF5qKlwXDwuObW5zLDr3U2ThFzZlr7n-xWlwp0pvcP2Y3q0VvcDfp7CozgVV-ulwEj_NL9BLYo3bpJTqqUOey6IbZ-AchJup8wNVMlelCE_ZorGhtvTDWYeewtHr6pE1klToCEMZPCRU9VgFuJi6UwLvycGEd1YW-EtfEuy0Y=";

    public String dd() {
        return this.d;
    }

    public boolean a(String str, String str2) throws Exception {
        return a(this.a + str + this.c + str2).equals(this.b);
    }

    private String a(String str) throws Exception {
        byte[] digest = MessageDigest.getInstance("SHA-512").digest(str.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(Integer.toString((b & 255) + 256, 16).substring(1));
        }
        return sb.toString();
    }
}

```

When submitting a pincode, the app will call Vault.a with the chosen pin and a hardcoded secret:

```java
public void onCompleted(String str) {
    try {
        if (((Boolean) MainActivity.this.vault.getClass().getMethod("a", String.class, String.class).invoke(MainActivity.this.vault, str, "de287e29a4a38788ba96136d6c2f21d0")).booleanValue()) {
            Toast.makeText(MainActivity.this.getApplicationContext(), "Correct", 1).show();
            Method method = MainActivity.this.vault.getClass().getMethod("dd", new Class[0]);
            MainActivity mainActivity = MainActivity.this;
            mainActivity.submitKey(str, (String) method.invoke(mainActivity.vault, new Object[0]));
        } else {
            Toast.makeText(MainActivity.this.getApplicationContext(), "Wrong", 1).show();
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
    pinPadView.clear();
}
```

In order for Vault.a to return true, the SHA-512 of `Vault.a + pin + Vault.c + hardcoded` needs to equal `Vault.b`.

We can create a small python script to bruteforce the pincode, which is the only unknown part:

```python

import hashlib
def Sha512Hash(pwd):
    return  hashlib.sha512(pwd.encode('utf-8')).hexdigest()

# a + pin + c + hardcoded
hardcoded = "de287e29a4a38788ba96136d6c2f21d0"
a = "95921fcd564f9136822ebcc151208ad1"
c = "3860f85c2653ef9c663c39087fcb51b5"
b = "eee3355c1b4cb248586b93ce314805b58ad9cb299239e583142c59a6ed7fd12c8e20b5a578780540a287ea985e4ac66c36eb07ee8a7c5cc7cd96c946e0d94798"
# sol = Sha512Hash(a + pin + c + hardcoded)
for i in range(100000, 999999):
    if Sha512Hash(a + str(i) + c + hardcoded) == b:
        print(i)
```

Which will print out the pincode:

```
➜  solution python3 pysolve.py 
878960
```

The difficult aspect of this challenge is that you have to be quite fast, so you'll have to automate. Once the PIN is found, the easiest solution is to enter it in the app within the timeframe and the flag will be printed on screen.

## PoC script
No PoC script

## Flag
csc(The_2FA_codes_mason_what_do_they_mean)

## Creator
Jeroen Beckers

## Creator bio
Hi, I'm Jeroen and I love hacking mobile apps. I'm a co-author of the OWASP MASVS/MASTG and I teach the SANS SEC575 Mobile application security and ethical hacking course. I work at NVISO as the Mobile Solution lead and I also organize the CSCBE.