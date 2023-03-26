# WhatThePassword

## Category

Reversing

## Estimated difficulty

Easy

## Description

A small keygen that seems to be solvable with `strings`, but the values are actually modified inside an init() function.

## Scenario

Enter the password and get the flag, it's that easy! ... Or is it?

## Write-up

Running `strings` on the binary gives some interesting results:

```
/lib64/ld-linux-x86-64.so.2
puts
strlen
__libc_start_main
__cxa_finalize
printf
__isoc99_scanf
strcmp
libc.so.6
GLIBC_2.7
GLIBC_2.2.5
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
PTE1
u/UH
<KC*E
wH@k
kICl
Enter the password:
%19s
Welcome! Here's your flag: %s
Wrong
;*3$"
csc{n0t_wh4t_1t_s33ms!}
l3tm31n
GCC: (Debian 10.2.1-6) 10.2.1 20210110
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
keygen.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
_ITM_deregisterTMCloneTable
puts@GLIBC_2.2.5
_edata
_fini
strlen@GLIBC_2.2.5
printf@GLIBC_2.2.5
__data_start
strcmp@GLIBC_2.2.5
__gmon_start__
__dso_handle
_IO_stdin_used
_end
__bss_start
main
__construct_gc
__isoc99_scanf@GLIBC_2.7
__TMC_END__
_ITM_registerTMCloneTable
flag
__cxa_finalize@GLIBC_2.2.5
_init
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
```

Most notably, we see `csc{n0t_wh4t_1t_s33ms!}` and `l3tm31n`. However, trying this password doesn't work:

```➜  keygen.1 echo "l3tm31n" | ./keygen
Enter the password:
Wrong
➜  keygen.1 
```

Let's take a look with r2:

```
➜  keygen.1 r2 keygen                                          
Warning: run r2 with -e io.cache=true to fix relocations in disassembly
 -- r2OS r2pad 0.1 SMP GENERIC r2_64 GNU/r2OS
[0x00001070]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00001070]> afl
0x00001070    1 33           entry0
0x000012c2    7 82           sym.strcmp
0x000010a0    4 41   -> 34   sym.deregister_tm_clones
0x000010d0    4 57   -> 51   sym.register_tm_clones
0x00001110    5 57   -> 50   sym.__do_global_dtors_aux
0x00001060    1 6            sym.imp.__cxa_finalize
0x00001150    1 5            entry.init0
0x00001314    1 9            sym._fini
0x00001155    4 112          main
0x000011c5    7 253          entry.init1
0x00001000    3 23           sym._init
0x00001030    1 6            sym.imp.puts
0x00001040    1 6            sym.imp.printf
0x00001050    1 6            sym.imp.__isoc99_scanf
[0x00001070]> smain
[0x00001155]> pdf
            ; DATA XREF from entry0 @ 0x1084
┌ 112: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_20h @ rbp-0x20
│           0x00001155      55             push rbp
│           0x00001156      4889e5         mov rbp, rsp
│           0x00001159      4883ec20       sub rsp, 0x20
│           0x0000115d      488d3da40e00.  lea rdi, str.Enter_the_password: ; 0x2008 ; "Enter the password:"
│           0x00001164      e8c7feffff     call sym.imp.puts           ; int puts(const char *s)
│           0x00001169      488d45e0       lea rax, [var_20h]
│           0x0000116d      4889c6         mov rsi, rax
│           0x00001170      488d3da50e00.  lea rdi, str.19s            ; 0x201c ; "%19s"
│           0x00001177      b800000000     mov eax, 0
│           0x0000117c      e8cffeffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x00001181      488d45e0       lea rax, [var_20h]
│           0x00001185      488d35042f00.  lea rsi, obj.pwd            ; 0x4090 ; "l3tm31n"
│           0x0000118c      4889c7         mov rdi, rax
│           0x0000118f      e82e010000     call sym.strcmp             ; int strcmp(const char *s1, const char *s2)
│           0x00001194      85c0           test eax, eax
│       ┌─< 0x00001196      751a           jne 0x11b2
│       │   0x00001198      488d35a12e00.  lea rsi, obj.flag           ; 0x4040 ; "csc{n0t_wh4t_1t_s33ms!}"
│       │   0x0000119f      488d3d820e00.  lea rdi, str.Welcome__Here_s_your_flag:__s ; 0x2028 ; "Welcome! Here's your flag: %s\n"
│       │   0x000011a6      b800000000     mov eax, 0
│       │   0x000011ab      e890feffff     call sym.imp.printf         ; int printf(const char *format)
│      ┌──< 0x000011b0      eb0c           jmp 0x11be
│      │└─> 0x000011b2      488d3d8e0e00.  lea rdi, str.Wrong          ; 0x2047 ; "Wrong"
│      │    0x000011b9      e872feffff     call sym.imp.puts           ; int puts(const char *s)
│      │    ; CODE XREF from main @ 0x11b0
│      └──> 0x000011be      b800000000     mov eax, 0
│           0x000011c3      c9             leave
└           0x000011c4      c3             ret
[0x00001155]> 
```

The main function is fairly straightforward. The password is compared to the string at 0x4090 and then the flag is printed. However, we know that l3tm31n is not the correct password, so let's use GDB to see which value is stored at in $rsi when we arrive at the strcmp call:

```gdb
➜  keygen.1 gdb ./keygen
(gdb) b main
Breakpoint 1 at 0x1159
(gdb) run
Starting program: /home/kali/cscbe/baby/keygen.1/keygen 

Breakpoint 1, 0x0000555555555159 in main ()
(gdb) disas
Dump of assembler code for function main:
   0x0000555555555155 <+0>:     push   %rbp
   0x0000555555555156 <+1>:     mov    %rsp,%rbp
=> 0x0000555555555159 <+4>:     sub    $0x20,%rsp
   0x000055555555515d <+8>:     lea    0xea4(%rip),%rdi        # 0x555555556008
   0x0000555555555164 <+15>:    callq  0x555555555030 <puts@plt>
   0x0000555555555169 <+20>:    lea    -0x20(%rbp),%rax
   0x000055555555516d <+24>:    mov    %rax,%rsi
   0x0000555555555170 <+27>:    lea    0xea5(%rip),%rdi        # 0x55555555601c
   0x0000555555555177 <+34>:    mov    $0x0,%eax
   0x000055555555517c <+39>:    callq  0x555555555050 <__isoc99_scanf@plt>
   0x0000555555555181 <+44>:    lea    -0x20(%rbp),%rax
   0x0000555555555185 <+48>:    lea    0x2f04(%rip),%rsi        # 0x555555558090 <pwd>
   0x000055555555518c <+55>:    mov    %rax,%rdi
   0x000055555555518f <+58>:    callq  0x5555555552c2 <strcmp>
   0x0000555555555194 <+63>:    test   %eax,%eax
   0x0000555555555196 <+65>:    jne    0x5555555551b2 <main+93>
   0x0000555555555198 <+67>:    lea    0x2ea1(%rip),%rsi        # 0x555555558040 <flag>
   0x000055555555519f <+74>:    lea    0xe82(%rip),%rdi        # 0x555555556028
   0x00005555555551a6 <+81>:    mov    $0x0,%eax
   0x00005555555551ab <+86>:    callq  0x555555555040 <printf@plt>
   0x00005555555551b0 <+91>:    jmp    0x5555555551be <main+105>
   0x00005555555551b2 <+93>:    lea    0xe8e(%rip),%rdi        # 0x555555556047
   0x00005555555551b9 <+100>:   callq  0x555555555030 <puts@plt>
   0x00005555555551be <+105>:   mov    $0x0,%eax
   0x00005555555551c3 <+110>:   leaveq 
   0x00005555555551c4 <+111>:   retq   
End of assembler dump.
(gdb) b * main+58
Breakpoint 2 at 0x55555555518f
(gdb) c
Continuing.
Enter the password:
testytest  

Breakpoint 2, 0x000055555555518f in main ()

(gdb) x/20x $rsi
0x555555558090 <pwd>:   0x43316830      0x0077306e      0x00000000      0x00000000
0x5555555580a0 <pwd+16>:        0x00000000      0x00000000      0x00000000      0x00000000
0x5555555580b0: 0x00000000      0x00000000      0x00000000      0x00000000
0x5555555580c0: 0x00000000      0x00000000      0x00000000      0x00000000
0x5555555580d0: 0x00000000      0x00000000      0x00000000      0x00000000
(gdb) print (char*) $rsi
$1 = 0x555555558090 <pwd> "0h1Cn0w"
```

By entering this password, we get the flag:

```
➜  keygen.1 echo "0h1Cn0w" | ./keygen       
Enter the password:
Welcome! Here's your flag: csc{wh4t_1s_th1s_m4g1c}
➜  keygen.1 
```

And we have the flag!

But how did this happen? Well, there is a function which is executed before the main() function of the binary:

```
➜  keygen.1 r2 keygen
Warning: run r2 with -e io.cache=true to fix relocations in disassembly
 -- Downloading and verifying the blockchain...
[0x00001070]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00001070]> afl
0x00001070    1 33           entry0
0x000012c2    7 82           sym.strcmp
0x000010a0    4 41   -> 34   sym.deregister_tm_clones
0x000010d0    4 57   -> 51   sym.register_tm_clones
0x00001110    5 57   -> 50   sym.__do_global_dtors_aux
0x00001060    1 6            sym.imp.__cxa_finalize
0x00001150    1 5            entry.init0
0x00001314    1 9            sym._fini
0x00001155    4 112          main
0x000011c5    7 253          entry.init1
0x00001000    3 23           sym._init
0x00001030    1 6            sym.imp.puts
0x00001040    1 6            sym.imp.printf
0x00001050    1 6            sym.imp.__isoc99_scanf
[0x00001070]> sentry.init1
[0x000011c5]> pdf
            ;-- __construct_gc:
┌ 253: entry.init1 ();
│           ; var int64_t var_40h @ rbp-0x40
│           ; var int64_t var_38h @ rbp-0x38
│           ; var int64_t var_30h @ rbp-0x30
│           ; var int64_t var_20h @ rbp-0x20
│           ; var int64_t var_18h @ rbp-0x18
│           ; var int64_t var_10h @ rbp-0x10
│           ; var int64_t var_8h @ rbp-0x8
│           ; var int64_t var_4h @ rbp-0x4
│           0x000011c5      55             push rbp
│           0x000011c6      4889e5         mov rbp, rsp
│           0x000011c9      48b83c4b432a.  movabs rax, 0x7701452a434b3c
│           0x000011d3      ba00000000     mov edx, 0
│           0x000011d8      488945e0       mov qword [var_20h], rax
│           0x000011dc      488955e8       mov qword [var_18h], rdx
│           0x000011e0      c745f0000000.  mov dword [var_10h], 0
│           0x000011e7      c745fc000000.  mov dword [var_4h], 0
│       ┌─< 0x000011ee      eb47           jmp 0x1237
│      ┌──> 0x000011f0      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x000011f3      4898           cdqe
│      ╎│   0x000011f5      488d15942e00.  lea rdx, obj.pwd            ; 0x4090 ; "l3tm31n"
│      ╎│   0x000011fc      0fb60410       movzx eax, byte [rax + rdx]
│      ╎│   0x00001200      0fbed0         movsx edx, al
│      ╎│   0x00001203      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x00001206      4898           cdqe
│      ╎│   0x00001208      0fb64405e0     movzx eax, byte [rbp + rax - 0x20]
│      ╎│   0x0000120d      0fbec8         movsx ecx, al
│      ╎│   0x00001210      89d0           mov eax, edx
│      ╎│   0x00001212      29c8           sub eax, ecx
│      ╎│   0x00001214      83e880         sub eax, 0xffffff80
│      ╎│   0x00001217      99             cdq
│      ╎│   0x00001218      c1ea19         shr edx, 0x19
│      ╎│   0x0000121b      01d0           add eax, edx
│      ╎│   0x0000121d      83e07f         and eax, 0x7f
│      ╎│   0x00001220      29d0           sub eax, edx
│      ╎│   0x00001222      89c1           mov ecx, eax
│      ╎│   0x00001224      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x00001227      4898           cdqe
│      ╎│   0x00001229      488d15602e00.  lea rdx, obj.pwd            ; 0x4090 ; "l3tm31n"
│      ╎│   0x00001230      880c10         mov byte [rax + rdx], cl
│      ╎│   0x00001233      8345fc01       add dword [var_4h], 1
│      ╎│   ; CODE XREF from entry.init1 @ 0x11ee
│      ╎└─> 0x00001237      837dfc07       cmp dword [var_4h], 7
│      └──< 0x0000123b      7eb3           jle 0x11f0
│           0x0000123d      48b87748406b.  movabs rax, 0x154137186b404877
│           0x00001247      48ba6b49436c.  movabs rdx, 0x67f46146c43496b
│           0x00001251      488945c0       mov qword [var_40h], rax
│           0x00001255      488955c8       mov qword [var_38h], rdx
│           0x00001259      c745d0423e00.  mov dword [var_30h], 0x3e42 ; 'B>'
│           0x00001260      c745f8000000.  mov dword [var_8h], 0
│       ┌─< 0x00001267      eb4f           jmp 0x12b8
│      ┌──> 0x00001269      8b45f8         mov eax, dword [var_8h]
│      ╎│   0x0000126c      83c004         add eax, 4
│      ╎│   0x0000126f      4898           cdqe
│      ╎│   0x00001271      488d15c82d00.  lea rdx, obj.flag           ; 0x4040 ; "csc{n0t_wh4t_1t_s33ms!}"
│      ╎│   0x00001278      0fb60410       movzx eax, byte [rax + rdx]
│      ╎│   0x0000127c      0fbed0         movsx edx, al
│      ╎│   0x0000127f      8b45f8         mov eax, dword [var_8h]
│      ╎│   0x00001282      4898           cdqe
│      ╎│   0x00001284      0fb64405c0     movzx eax, byte [rbp + rax - 0x40]
│      ╎│   0x00001289      0fbec8         movsx ecx, al
│      ╎│   0x0000128c      89d0           mov eax, edx
│      ╎│   0x0000128e      29c8           sub eax, ecx
│      ╎│   0x00001290      83e880         sub eax, 0xffffff80
│      ╎│   0x00001293      99             cdq
│      ╎│   0x00001294      c1ea19         shr edx, 0x19
│      ╎│   0x00001297      01d0           add eax, edx
│      ╎│   0x00001299      83e07f         and eax, 0x7f
│      ╎│   0x0000129c      29d0           sub eax, edx
│      ╎│   0x0000129e      89c2           mov edx, eax
│      ╎│   0x000012a0      8b45f8         mov eax, dword [var_8h]
│      ╎│   0x000012a3      83c004         add eax, 4
│      ╎│   0x000012a6      89d1           mov ecx, edx
│      ╎│   0x000012a8      4898           cdqe
│      ╎│   0x000012aa      488d158f2d00.  lea rdx, obj.flag           ; 0x4040 ; "csc{n0t_wh4t_1t_s33ms!}"
│      ╎│   0x000012b1      880c10         mov byte [rax + rdx], cl
│      ╎│   0x000012b4      8345f801       add dword [var_8h], 1
│      ╎│   ; CODE XREF from entry.init1 @ 0x1267
│      ╎└─> 0x000012b8      837df813       cmp dword [var_8h], 0x13
│      └──< 0x000012bc      7eab           jle 0x1269
│           0x000012be      90             nop
│           0x000012bf      90             nop
│           0x000012c0      5d             pop rbp
└           0x000012c1      c3             ret
[0x000011c5]> 
```

This function takes the two variables at 0x4040 and 0x4090 and shifts all the characters based on two hardcoded character arrays. This init function is the result of using `__attribute__ ((__constructor__))` in C.

## PoC script
```
echo "0h1Cn0w" | ./keygen
```

## Flag
`csc{wh4t_1s_th1s_m4g1c}`

## Creator
Jeroen Beckers

## Creator bio
...
