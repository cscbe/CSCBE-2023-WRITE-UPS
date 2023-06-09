
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#define TFT_BLACK       0x0000
#define TFT_WHITE       0xFFFF

#define Lcd_X  240
#define Lcd_Y  320

const int s[53][53] = {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0,1,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,1,0,0,1,0,1,1,1,1,1,1,1,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,0,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,1,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,1,0,1,1,1,1,0,1,0,1,1,1,0,1,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0},{0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,1,1,1,1,0,0,0,1,1,0,0,1,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0},{0,0,0,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0},{0,0,0,0,0,1,1,0,1,0,1,0,0,1,0,0,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,0,1,1,0,0,1,1,0,0,0,0},{0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,1,1,1,0,1,1,0,0,0,1,0,0,0,0},{0,0,0,0,0,0,1,0,1,1,1,1,0,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1,1,0,1,0,0,1,0,1,1,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0},{0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,0,1,0,0,1,1,1,0,1,0,0,0,0},{0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0},{0,0,0,0,0,1,1,1,0,1,0,1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,1,1,1,0,0,1,1,1,0,0,1,1,0,0,0,0},{0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,0,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0},{0,0,0,0,1,1,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,1,1,0,0,0,0},{0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0},{0,0,0,0,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,1,1,0,1,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0},{0,0,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,0,0,0,0},{0,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0},{0,0,0,0,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,0,0,0,1,0,1,1,1,1,1,1,0,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,0,0},{0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,1,1,1,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0},{0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1,1,0,1,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0},{0,0,0,0,0,1,1,0,1,1,0,1,0,1,0,1,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,0,1,1,1,0,1,0,1,1,0,0,0,0},{0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,1,0,1,1,1,0,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0},{0,0,0,0,1,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,0,0,0},{0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,1,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,1,1,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0},{0,0,0,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0},{0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0},{0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0},{0,0,0,0,1,0,0,1,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,1,0,1,1,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,0,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0},{0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,1,1,1,1,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,0,1,0,1,0,1,1,1,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0},{0,0,0,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,1,1,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0},{0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};

#define TFT_DC 2
#define TFT_CS 15
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

void show_screen(){
  uint8_t x0 = 20;
  uint8_t y0 =  20; 
  int arr_size = (sizeof(s)/sizeof(s[0]));
  for(int x=0; x<arr_size;x++){
    for(int y=0; y<arr_size;y++){
      int color = TFT_WHITE;
      if (s[x][y] == 1){
        color = TFT_BLACK;
      }
      tft.drawPixel(x0 + 3 * x,     y0 + 3 * y, color);
      tft.drawPixel(x0 + 3 * x + 1, y0 + 3 * y, color);
      tft.drawPixel(x0 + 3 * x + 2, y0 + 3 * y, color);
      
      tft.drawPixel(x0 + 3 * x,     y0 + 3 * y + 1, color);
      tft.drawPixel(x0 + 3 * x + 1, y0 + 3 * y + 1, color);
      tft.drawPixel(x0 + 3 * x + 2, y0 + 3 * y + 1, color);

      tft.drawPixel(x0 + 3 * x,     y0 + 3 * y + 2, color);
      tft.drawPixel(x0 + 3 * x + 1, y0 + 3 * y + 2, color);
      tft.drawPixel(x0 + 3 * x + 2, y0 + 3 * y + 2, color);       
    }
  }
}

void setup() {

  tft.begin();
  tft.fillScreen(TFT_BLACK);
  show_screen();
}

void loop() {
  delay(100);
}