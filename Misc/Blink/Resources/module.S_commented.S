#define __SFR_OFFSET 0

; used for led definitions
#include "avr/io.h"     

;_______________________________________________________
; Functions called by C++
;-------------------------------------------------------
.global transmit

;_______________________________________________________
; Register name definitions.
;-------------------------------------------------------
#define temp r23
#define counter r24
#define yh r29
#define yl r28
#define mask r17
#define currentByte r16

;___________________________________
; Macro definitions.
;-----------------------------------
; Pushes the registers that must be restored after the execution of the assembler code.
.macro pushStart
    push r14
    push r15
    push r16
    push r17
    push r24
    push r25
    push r28
    push r29
    push r30
    push r31
.endM

; Restores the registers at the end of the execution of the assembler code.
; Note that the reigsters must be poped in the opposite order :)
.macro popEnd
    pop r31
    pop r30
    pop r29
    pop r28
    push r25
    push r24
    pop r17
    pop r16
    push r15
    push r14
.endM

; Loads one message byte from memory (y pointer), xors it with the p1 register, and replaces
; it in memory.
.macro preprocessByte p1
    ld temp, y
    eor temp, \p1
    st y+, temp
.endM

;___________________________________________
; Global variables - created by C++ code. 
;-------------------------------------------
; reserve space in memory
.extern m

;___________________________________
; Start of code
;-----------------------------------
.section .text

transmit:
    pushStart                     ; save all the registers we'll be using 
    sbi   DDRB, 5                 ; Set PB5 as output
    call preprocess               ; XOR the message with the key
    call beacon                   ; transmit the bits of the XORed message by blinking the onboard led
    popEnd
    reti                          ; return to C code 

; Used to XOR the message with the XOR key byte by byte
preprocess:
    ldi yh, hi8(m)                ; load the address of the message in y
    ldi yl, lo8(m)
    ldi currentByte, 0x74
    preprocessByte currentByte
    ldi currentByte, 0x68
    preprocessByte currentByte
    ldi currentByte, 0x65
    preprocessByte currentByte
    ldi currentByte, 0x79
    preprocessByte currentByte
    ldi currentByte, 0x41
    preprocessByte currentByte   
    ldi currentByte, 0x72
    preprocessByte currentByte
    ldi currentByte, 0x33
    preprocessByte currentByte
    ldi currentByte, 0x41
    preprocessByte currentByte
    ldi currentByte, 0x6d
    preprocessByte currentByte
    ldi currentByte, 0x30
    preprocessByte currentByte
    ldi currentByte, 0x6e
    preprocessByte currentByte
    ldi currentByte, 0x67
    preprocessByte currentByte
    ldi currentByte, 0x55
    preprocessByte currentByte
    ldi currentByte, 0x73
    preprocessByte currentByte
    ldi currentByte, 0x21
    preprocessByte currentByte
    ret

; Send out the bytes
beacon:
    ldi counter, 15         ; load the length of the message in the counter
    ldi yh, hi8(m)          ; load the address of the message in y
    ldi yl, lo8(m)
    loop_beacon:
      ld currentByte, y+    ; get the next byte in currentByte register
      call beaconByte       ; send out the bits of the byte by blinking the led
      dec counter
      brne loop_beacon      ; more bytes to process
    ret

; Beacons the value in currentByte register, bit by bit
beaconByte:
    ldi mask, 0x80          ; initialize a bit mask to 1
    check_bits:
      mov temp, currentByte
      and temp, mask        ; temp = currentByte & mask
      cp temp, mask         ; check if (temp == mask), meaning current bit is a 1
      brne bit_0            ; if temp != mask, the current bit is a 0, so jump to the blinkLong part
      call blinkShort       ; otherwise, blinkShort
      rjmp after_blink      
      bit_0: 
        call blinkLong
      after_blink:
        lsr mask            ; shift the bit mask left by 1
        cpi mask, 0x00      ; check if (mask == 0x00), meaning that we are done
        brne check_bits     ; if not done, repeat the loop
      ret

; turn the onboard led on for 400ms
blinkShort:
  push r24
  sbi   PINB, 5       ; Toggle PINB
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  sbi   PINB, 5       ; Toggle PINB
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  pop r24
  ret

; turn the onboard led on for 1s
blinkLong:
  push r24
  sbi   PINB, 5       ; Toggle PINB
  ldi   r25, hi8(1000)
  ldi   r24, lo8(1000)
  call  delay_ms
  sbi   PINB, 5       ; Toggle PINB
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  pop r24
  ret

; Delay r25:r24 ms. We need to place the value in two registers because it's > 255. 
delay_ms:
  ldi   r31, hi8(4000)
  ldi   r30, lo8(4000)
1:
  sbiw    r30, 1
  brne    1b
  sbiw    r24, 1
  brne    delay_ms
  ret