class StoryPlayer {
  AudioPlayer player;
  
  boolean story_loaded = false;
  boolean story_playing = false;
  boolean story_paused = false;
  int story_part_cursor = 0;
  
  // Storty Config
  String story_folder = "";
  String story_title = "";
  String []story_part_filename;
  
  // UI main cords 
  int m_x = 3;
  int m_y = 3;
  int m_w = 794;
  int m_h = 417;
  
  int m_spacer = 5;
  
  // UI Parts Bar
  int s_partsbar_x;
  int s_partsbar_y;
  int s_partsbar_w;
  int s_partsbar_h;
  
  // UI Scrub Bar
  int s_scrubbar_x;
  int s_scrubbar_y;
  int s_scrubbar_w;
  int s_scrubbar_h;
  
  int s_scruber_x_min;
  int s_scruber_x_max;
  int s_scruber_y;
  int s_scruber_w;
  int s_scruber_h;
  
  // UI Buttons
  int s_btnstop_x;
  int s_btnstop_y;
  int s_btnstop_w;
  int s_btnstop_h;
  
  int s_btnplay_x;
  int s_btnplay_y;
  int s_btnplay_w;
  int s_btnplay_h;
  
  int s_btnnext_x;
  int s_btnnext_y;
  int s_btnnext_w;
  int s_btnnext_h;
  
  int s_btnfour_x;
  int s_btnfour_y;
  int s_btnfour_w;
  int s_btnfour_h;
  
  StoryPlayer(){
    story_part_filename = new String[0];
    
    // Do lots of weird math in a contrived effort to make things elastic
    s_partsbar_x = m_x;
    s_partsbar_y = m_y;
    s_partsbar_w = m_w;
    s_partsbar_h = 15;
    
    s_scrubbar_x = m_x;
    s_scrubbar_y = m_y + s_partsbar_h + m_spacer;
    s_scrubbar_w = m_w;
    s_scrubbar_h = 15;
    
    s_scruber_x_min = m_x;
    s_scruber_y = m_y + s_partsbar_h + m_spacer;
    s_scruber_w = 30;
    s_scruber_h = 15;
    s_scruber_x_max = m_x + s_scrubbar_w - s_scruber_w;
    
    int buttons_h = m_h - s_partsbar_h - m_spacer - s_scrubbar_h;
    int button_size = (buttons_h - (m_spacer * 3)) / 4;
    int button_x = m_x + m_w - button_size;
    int button_y = m_y + s_partsbar_h + (m_spacer * 2) + s_scrubbar_h;
    
    s_btnstop_x = button_x;
    s_btnstop_y = button_y;
    s_btnstop_w = button_size;
    s_btnstop_h = button_size;
  
    s_btnplay_x = button_x;
    s_btnplay_y = button_y + m_spacer + button_size;
    s_btnplay_w = button_size;
    s_btnplay_h = button_size;
  
    s_btnnext_x = button_x;
    s_btnnext_y = button_y + ((m_spacer + button_size) * 2);
    s_btnnext_w = button_size;
    s_btnnext_h = button_size;
  
    s_btnfour_x = button_x;
    s_btnfour_y = button_y + ((m_spacer + button_size) * 3);
    s_btnfour_w = button_size;
    s_btnfour_h = button_size;
    
  }
  
  void loadStory(String filename) {
    stopStory();
    
    if (!fileExists(filename)) {
      print("error loading story file " + filename);
      return;
    }
    
    // Get folder for relative locations
    String[] file_bits = split(filename, '/');
    String folder = "";
    for (int i = 0; i < file_bits.length-1; i++) {
      folder = folder + file_bits[i] + "/";
    }
    story_folder = folder;
    
    // Load json Config
    JSONObject json_config = loadJSONObject(filename);
    
    story_title = json_config.getString("title");
    println("Loading story " + story_title);
    
    // Load Parts
    JSONArray json_config_parts = json_config.getJSONArray("parts");
    story_part_filename = new String[json_config_parts.size()];
    
    for (int i = 0; i < json_config_parts.size(); i++) {
      JSONObject part_config = json_config_parts.getJSONObject(i);
      story_part_filename[i] = part_config.getString("filename");
    }
    
    story_loaded = true;
  }
  
  void display() {
    // Parts Bar
    if (story_part_filename.length > 0) {
      int part_w = (s_partsbar_w - (m_spacer * (story_part_filename.length - 1))) / story_part_filename.length;
      
      for (int i = 0; i < story_part_filename.length; i++) {
        if (story_part_cursor == i) {
          stroke(255);
          fill(255);
        } else {
          stroke(255);
          fill(0, 0, 0, 127);
        }
        
        int part_x = s_partsbar_x + ((part_w + m_spacer) * i) ;
        rect(part_x, s_partsbar_y, part_w, s_partsbar_h); // border
      }
    }
    
    // Scrub Bar
    stroke(255);
    fill(0, 0, 0, 127);
    rect(s_scrubbar_x, s_scrubbar_y, s_scrubbar_w, s_scrubbar_h); // border
    
    if (player != null){
      float position = float(player.position())/float(player.length());
      int scruber_x = int(map(position, 0, 1, s_scruber_x_min, s_scruber_x_max));
      fill(255);
      rect(scruber_x, s_scruber_y, s_scruber_w, s_scruber_h); // scruber
    }
    
    // Buttons 
    if (story_loaded && !story_playing) {
      stroke(255);
      fill(255, 255, 255, 127);
    }
    else {
      stroke(255);
      fill(0, 0, 0, 127);
    }
    rect(s_btnstop_x, s_btnstop_y, s_btnstop_w, s_btnstop_h); // stop button
    
    if (story_playing) {
      stroke(255);
      fill(255, 255, 255, 127);
    }
    else {
      stroke(255);
      fill(0, 0, 0, 127);
    }
    rect(s_btnplay_x, s_btnplay_y, s_btnplay_w, s_btnplay_h); // play button
    
    stroke(255);
    fill(0, 0, 0, 127);
    rect(s_btnnext_x, s_btnnext_y, s_btnnext_w, s_btnnext_h); // next button
    
    stroke(127);
    fill(0, 0, 0, 127);
    rect(s_btnfour_x, s_btnfour_y, s_btnfour_w, s_btnfour_h); // fourth button
    
    // Button Labels
    fill(255);
    textSize(20);
    text("Stop", s_btnstop_x, s_btnstop_y, s_btnstop_w, s_btnstop_h);
    
    if (story_playing && !story_paused) {
      text("Pause", s_btnplay_x, s_btnplay_y, s_btnplay_w, s_btnplay_h);
    }
    else {
      text("Play", s_btnplay_x, s_btnplay_y, s_btnplay_w, s_btnplay_h);
    }
    
    text("Next", s_btnnext_x, s_btnnext_y, s_btnnext_w, s_btnnext_h);
  }
  
  void handleMousePressed(int x, int y) {
    if (inRect(x, y, s_btnstop_x, s_btnstop_y, s_btnstop_w, s_btnstop_h)) {
      // stop
      if (story_playing) {
        stopStory();
      }
    }
    else if (inRect(x, y, s_btnplay_x, s_btnplay_y, s_btnplay_w, s_btnplay_h)) {
      // play
      if (story_loaded) {
        if (!story_playing && !story_paused) {
          startStory();
        }
        else if (story_playing && !story_paused) {
          pauseStory();
        }
        else if (story_playing && story_paused) {
          unpauseStory();
        }
      }
    }
    else if (inRect(x, y, s_btnnext_x, s_btnnext_y, s_btnnext_w, s_btnnext_h)) {
      if (story_part_cursor < story_part_filename.length) {
        boolean was_playing = false;
        if (player != null) {
          was_playing = player.isPlaying();
        }
        
        if (was_playing) {
          player.shiftGain(0, -80, 1000);
          delay(1000);
          player.pause();
        } 
        
        nextPage();
      }
      
    }
    
  }
  
  void nextPage() {
    story_part_cursor = story_part_cursor + 1;
    if (story_playing) {
      startStory();
    }
  }
  
  void pauseStory() {
    player.pause();
    story_paused = true;
  }
  
  void runStoryPlayer() {
    if (story_playing) {
      if (player.position() == player.length()) {nextPage();}
    }
  }
  
  void startStory() {
    player = minim.loadFile(story_folder + story_part_filename[story_part_cursor]);
    
    if (player != null) {
      player.play();
      story_playing = true;
    }
  }
  
  void stopStory() {
    if (player != null){
      player.pause();
      player = null;
    }
    
    story_part_cursor = 0;
    story_playing = false;
    story_paused = false;
  }
  
  void unpauseStory() {
    player.play();
    story_paused = false;
  }
}
