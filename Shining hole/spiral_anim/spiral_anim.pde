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
  framecount = 400;
  thing_scale = 0.9*min(width, height);
  
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
  translate(width/2, height/2);
  translate(sin(PI + 2*PI*I/framecount)*15,cos(PI + 2*PI*I/framecount)*15);
  translate(-thing_scale/2, -thing_scale/2);
  shape(thing, 0, 0, thing_scale, thing_scale); 
  popMatrix();
  
  pushMatrix();
  translate(width/2, height/2);
  translate(sin(2*PI*I/framecount)*15,cos(2*PI*I/framecount)*15);
  translate(-thing_scale/2, -thing_scale/2);
  shape(thing, 0, 0, thing_scale, thing_scale); 
  popMatrix();
  
  gifExport.setDelay(20);
  gifExport.addFrame();
  
  I++;

}