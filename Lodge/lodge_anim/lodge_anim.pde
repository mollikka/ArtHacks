import gifAnimation.*;

GifMaker gifExport;

PShape thing;
float I;
float thing_scale;
int framecount;

void setup() {
  size(800, 800);
  thing = loadShape("thing.svg");
  I = 0;
  //circle that fills rectangle
  //thing_scale = sqrt(2) * min(width, height);
  framecount = 600;
  thing_scale = 1.5 * min(width, height);
  
  gifExport = new GifMaker(this, "export.gif", 100);
  gifExport.setRepeat(0);
}

void draw() {
  if (I == framecount) {
    gifExport.finish();
    exit();
  }
  
  background(255);
  
  pushMatrix();
  translate(width/2 - thing_scale/2, height/2 - thing_scale/2);
  shape(thing, 0, 0,thing_scale, thing_scale);
  popMatrix();
  
  rotate(PI/16+sin(2*PI*I/framecount)*PI/32);
  rotate(0.1);
  pushMatrix();
  translate(width/2, height/2);
  //translate(width*(2*PI*I/framecount),100*cos(2*PI*I/framecount));
  translate(-thing_scale/2, -thing_scale/2);
  shape(thing, 0, 0, thing_scale, thing_scale); 
  popMatrix();
  
  gifExport.setDelay(20);
  gifExport.addFrame();
  
  I++;

}