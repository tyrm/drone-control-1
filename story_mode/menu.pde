class Menu {
  // Button Config
  int b_count;
  int b_height;
  int b_left;
  int b_margin;
  int b_spacer;
  int b_top;
  int b_width;
  
  int active_b = 0;
  String []menu_text = new String[5];
  
  Menu(){
    b_count = 5;
    b_spacer = 5;
    b_margin = 2;
    
    b_width = (width-(b_spacer*(b_count-1))-(b_margin*2))/b_count;
    b_height = 50;
    b_top = height - b_height - b_margin;
    b_left = 0 + b_margin;
    
    menu_text[0] = "System";
    menu_text[1] = "Story";
    menu_text[2] = "Subject";
    menu_text[3] = "Hardware";
    menu_text[4] = "Ambience";
  }
  
  void display() {
    for (int i = 0; i < b_count; i++) {
      int calc_left = b_left + ((b_width + b_spacer) * i);
      
      stroke(255);
      if (i == active_b) {
        fill(255, 255, 255, 127);
      } else {
        fill(0, 0, 0, 200);
      }
      rect(calc_left, b_top, b_width, b_height);
      
      if (i == active_b) {
        fill(0);
      } else {
        fill(255);
      }
      textSize(30);
      textAlign(CENTER, CENTER);  
      text(menu_text[i], calc_left, b_top, b_width, b_height);
      
      
    }
  }
  
  void handleMousePressed(int x, int y) {
    
    for (int i = 0; i < b_count; i++) {
      int calc_left = b_left + ((b_width + b_spacer) * i);
      if (inRect(x, y, calc_left, b_top, b_width, b_height)) {
        active_b = i;
        break;
      }
    }
  }
  
  int getActive() {
    return active_b;
  }
}
