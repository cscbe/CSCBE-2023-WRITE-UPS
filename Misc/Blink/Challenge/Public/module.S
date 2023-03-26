#define __SFR_OFFSET 0

#include "avr/io.h"     

.global transmit

#define temp r23
#define counter r24
#define yh r29
#define yl r28
#define mask r17
#define currentByte r16

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

.macro preprocessByte p1
    ld temp, y
    eor temp, \p1
    st y+, temp
.endM

.extern m

.section .text

transmit:
    pushStart                     
    sbi   DDRB, 5                 
    call preprocess               
    call beacon                   
    popEnd
    reti                           

preprocess:
    ldi yh, hi8(m)                
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

beacon:
    ldi counter, 15         
    ldi yh, hi8(m)          
    ldi yl, lo8(m)
    loop_beacon:
      ld currentByte, y+    
      call beaconByte       
      dec counter
      brne loop_beacon      
    ret

beaconByte:
    ldi mask, 0x80          
    check_bits:
      mov temp, currentByte
      and temp, mask        
      cp temp, mask         
      brne bit_0            
      call blinkS      
      rjmp after_blink      
      bit_0: 
        call blinkL
      after_blink:
        lsr mask            
        cpi mask, 0x00      
        brne check_bits     
      ret

blinkS:
  push r24
  sbi   PINB, 5       
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  sbi   PINB, 5       
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  pop r24
  ret

blinkL:
  push r24
  sbi   PINB, 5       
  ldi   r25, hi8(1000)
  ldi   r24, lo8(1000)
  call  delay_ms
  sbi   PINB, 5       
  ldi   r25, hi8(400)
  ldi   r24, lo8(400)
  call  delay_ms
  pop r24
  ret

delay_ms:
  ldi   r31, hi8(4000)
  ldi   r30, lo8(4000)
1:
  sbiw    r30, 1
  brne    1b
  sbiw    r24, 1
  brne    delay_ms
  ret