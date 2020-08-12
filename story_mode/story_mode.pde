import ddf.minim.*;
import websockets.*;

Ambience ambience;
Menu menu;
Minim minim;
StoryPlayer story_player;

WebsocketClient wsc;

void setup() {
  size(800, 480, P2D);
  background(0);
  
  //wsc = new WebsocketClient(this, "ws://localhost:6969/");
  
  menu = new Menu();
  minim = new Minim(this);
  
  ambience = new Ambience(minim);
  story_player = new StoryPlayer();
  
  story_player.loadStory("stories/drone-1/story.json");
}

void draw() {
  ambience.displayBackground();
  menu.display();
  
  switch (menu.getActive()){
    case 1:
      story_player.display();
      break;
    case 4:
      ambience.display();
      break;
  }
  
  story_player.runStoryPlayer();
}

void mousePressed() {
  int x = mouseX;
  int y = mouseY;
  
  menu.handleMousePressed(x, y);
  
  switch (menu.getActive()){
    case 1:
      story_player.handleMousePressed(x, y);
      break;
    case 4:
      ambience.handleMousePressed(x, y);
      break;
  }
}

void mouseDragged() {
  int x = mouseX;
  int y = mouseY;
  
  switch (menu.getActive()){
    case 4:
      ambience.handleMouseDragged(x, y);
      break;
  }
}

boolean fileExists(String filename) {
  File f = dataFile(filename);
  return f.isFile();
}

boolean inRect(int x, int y, int rx, int ry, int rw, int rh) {
  return (rx <= x) && (x <= rx + rw) && (ry <= y) && (y <= ry + rh);
}
