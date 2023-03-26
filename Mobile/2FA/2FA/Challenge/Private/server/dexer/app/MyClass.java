

package be.dauntless.twofa;

import android.util.Log;

import java.security.MessageDigest;

public class Vault{

    // 243d16af5d636a9a5c2ce5c2c5531b8d7777779a9c965708ef7b4ca380c75a60c063a2de287e29a4a38788ba96136d6c2f21d0
    String a = "c0464a67969afeffc119ed5c7841c05e";
    String c = "f2d3e977f0b719b19cba665c9d5adc18";
    String b = "cecc3f78f4eb98de0dc3a58264fdf8c6abc3a2a55a1a0a8d564b0d4542974e8658d0611ea2d127a7e141450ea4c75b16f58cb165925c3ff4e6fdba0b4c468afa";

    public String d = "xxxxxxxxxxxxxxxxxxxxx";
   
    public boolean a(String b, String c) throws Exception
    {
        return this.a(a + b + this.c + c).equals(this.b);
    }

    private String a(String b) throws Exception
    {
        //Log.d("xxx" ,b);
        MessageDigest md = MessageDigest.getInstance("SHA-512");
        byte[] digest = md.digest(b.getBytes());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < digest.length; i++) {
            sb.append(Integer.toString((digest[i] & 0xff) + 0x100, 16).substring(1));
        }
        //Log.d("xxx", sb.toString());
        return sb.toString();
    }
}

