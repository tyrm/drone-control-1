class Ambience {
  Minim my_minim;
  AudioPlayer player;
  
  int active_amb = 0;
  int active_page = 0;
  
  int gain_min = -50;
  int gain_max = 0;
  
  // ambaince files data
  String []amb_file;
  String []amb_description;
  PImage []amb_image;
  
  // UI main cords 
  int m_x = 3;
  int m_y = 3;
  int m_w = 794;
  int m_h = 417;
  
  int m_selections = 4;
  int m_spacer = 5;
  
  // UI gain cords
  int g_x;
  int g_y;
  int g_w;
  int g_h;
  
  int g_bar_x;
  int g_bar_y;
  int g_bar_w;
  int g_bar_h;
  
  int g_label_x;
  int g_label_y;
  int g_label_w;
  int g_label_h;
  
  int g_text_x;
  int g_text_y;
  int g_text_w;
  int g_text_h;
  
  // UI ambiance selector cords
  int s_selectarea_x;
  int s_selectarea_y;
  int s_selectarea_w;
  int s_selectarea_h;
  
  int s_pageup_x;
  int s_pageup_y;
  int s_pageup_w;
  int s_pageup_h;
  
  int s_pagedown_x;
  int s_pagedown_y;
  int s_pagedown_w;
  int s_pagedown_h;
  
  int s_scrollbar_x;
  int s_scrollbar_y;
  int s_scrollbar_w;
  int s_scrollbar_h;
  
  Ambience(Minim m) {
    my_minim = m;
    
    if (fileExists("ambience.json")) {
       // load config
      JSONArray json_config = loadJSONArray("ambience.json");
      
      // int arrays
      amb_file = new String[json_config.size()];
      amb_description = new String[json_config.size()];
      amb_image = new PImage[json_config.size()];
      
      for (int i = 0; i < json_config.size(); i++) {
        
        JSONObject entry = json_config.getJSONObject(i); 
    
        // Save Metadata
        amb_file[i] = entry.getString("file");
        amb_description[i] = entry.getString("description");
        
        // Load Image
        String image_filename = entry.getString("image");
        amb_image[i] = loadImage(image_filename);
        
        println("Ambiance found: " + amb_file[i]);
      }
      
      // Start first ambience
      if (fileExists(amb_file[active_amb])){
        println("starting first ambience");
        player = my_minim.loadFile(amb_file[active_amb]);
        player.setGain(-20);
        player.play();
      }
      
    } else {
      println("ambience.json not found!");
    }
    
    // Do lots of weird math in a contrived effort to make things elastic
    // gain
    g_w = 100;
    g_x = m_x + (m_w-g_w);
    g_y = m_y;
    g_h = m_h;
    
    g_label_x = g_x;
    g_label_y = g_y;
    g_label_w = g_w;
    g_label_h = 40;
    
    g_text_x = g_x;
    g_text_w = g_w;
    g_text_h = 30;
    
    g_bar_w = 30;
    g_bar_x = g_x + ((g_w - g_bar_w) / 2);
    g_bar_y = g_y + g_label_h;
    g_bar_h = g_h - g_label_h - g_text_h;
    
    g_text_y = g_y + g_label_h + g_bar_h;
    
    // selector
    s_pageup_w = 60;
    s_pageup_h = 60;
    s_pageup_x = m_x + (m_w - g_w - m_spacer - s_pageup_w);
    s_pageup_y = m_y;
  
    s_pagedown_w = 60;
    s_pagedown_h = 60;
    s_pagedown_x = m_x + (m_w - g_w - m_spacer - s_pagedown_w);
    s_pagedown_y = m_y + m_h - s_pagedown_h;
    
    s_scrollbar_w = 60;
    s_scrollbar_x = m_x + (m_w - g_w - m_spacer - s_scrollbar_w);
    s_scrollbar_y = m_y + s_pageup_h + m_spacer;
    s_scrollbar_h = m_h - s_pageup_h - s_pagedown_h - (m_spacer * 2);
    
    s_selectarea_x = m_x;
    s_selectarea_y = m_y;
    s_selectarea_w = m_w - s_scrollbar_w - g_w - (m_spacer * 2);
    s_selectarea_h = m_h;
  }
  
  void display() {
    // *************
    // * draw gain *
    // *************
    stroke(255);
    fill(0, 0, 0, 127);
    rect(g_x, g_y, g_w, g_h); // border
    
    rect(g_bar_x, g_bar_y, g_bar_w, g_bar_h); // bar outline
    
    fill(255);
    textAlign(CENTER, CENTER);  
    textSize(24);
    text("Gain" , g_label_x, g_label_y, g_label_w, g_label_h);
    
    textSize(16);
    float gain = player.getGain();
    text(nf(gain, 0, 2), g_text_x, g_text_y, g_text_w, g_text_h);
    
    int gain_y = int(map(gain, gain_min, gain_max, g_bar_h, 0));
    rect(g_bar_x, g_bar_y + gain_y, g_bar_w, g_bar_h - gain_y); // gain bar
    
    // *****************
    // * draw selector *
    // *****************
    stroke(255);
    fill(0, 0, 0, 127);
    rect(s_pageup_x, s_pageup_y, s_pageup_w, s_pageup_h); // page up
    rect(s_pagedown_x, s_pagedown_y, s_pagedown_w, s_pagedown_h); // page down
    rect(s_scrollbar_x, s_scrollbar_y, s_scrollbar_w, s_scrollbar_h); // scrollbar
    
    // display selections
    int select_box_h = (s_selectarea_h - (m_spacer * (m_selections - 1))) / m_selections;
    int img_h = select_box_h - (m_spacer * 2);
    int img_w = (img_h * 80) / 48;
    int img_x = s_selectarea_x + m_spacer;
    
    for (int i = 0; i < m_selections; i++) {
      int cursor = (active_page * m_selections) + i;
      if (cursor <= amb_file.length - 1) {
        if (cursor == active_amb) {
          stroke(255);
          fill(255, 255, 255, 90);
        } else {
          stroke(255);
          fill(0, 0, 0, 127);
        }
    
        int select_box_y = m_y + ((select_box_h + m_spacer) * i);
        rect(s_selectarea_x, select_box_y, s_selectarea_w, select_box_h); // select box
        
        int img_y = m_y + ((select_box_h + m_spacer) * i) + m_spacer;
        image(amb_image[cursor], img_x, img_y, img_w, img_h);
      }
    }
  }
  
  void displayBackground() {
    image(amb_image[active_amb], 0, 0, width, height);
    noStroke();
    fill(0, 0, 0, 80);
    rect(0, 0, width, height);
  }
  
  void handleMousePressed(int x, int y) {
    // gain adjust
    if (inRect(x, y, g_bar_x, g_bar_y, g_bar_w, g_bar_h)) {
      float new_gain = map(y, g_bar_y + g_bar_h, g_bar_y, gain_min, gain_max);
      player.setGain(new_gain);
    }
    
    // handle selections
    int select_box_h = (s_selectarea_h - (m_spacer * (m_selections - 1))) / m_selections;
    
    for (int i = 0; i < m_selections; i++) {
      int cursor = (active_page * m_selections) + i;
      if (cursor <= amb_file.length - 1) {
        int select_box_y = m_y + ((select_box_h + m_spacer) * i);
        //rect(s_selectarea_x, select_box_y, s_selectarea_w, select_box_h);
        if (inRect(x, y, s_selectarea_x, select_box_y, s_selectarea_w, select_box_h)) {
          if (active_amb != cursor) {
            active_amb = cursor;
            
            float gain = player.getGain();
            player.close();
            player = my_minim.loadFile(amb_file[active_amb]);
            player.setGain(gain);
            player.play();
            
            println("beep", cursor);
          }
        }
      }
    }
  }
  
  void handleMouseDragged(int x, int y) {
    // gain adjust
    if (inRect(x, y, g_bar_x, g_bar_y, g_bar_w, g_bar_h)) {
      float new_gain = map(y, g_bar_y + g_bar_h, g_bar_y, gain_min, gain_max);
      player.setGain(new_gain);
    }
  }
}
