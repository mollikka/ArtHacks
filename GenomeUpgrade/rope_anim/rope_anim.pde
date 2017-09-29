import gifAnimation.*;

GifMaker gifExport;

float I;
int framecount = 400;
int pathstepcount = 200;
int little_pathcount, big_pathcount, pathcount;
int recursive_levels = 4;
int []recursive_pathcounts = {2,2,2,2};
float []recursive_circleRs = {20,40,80,160};
float []recursive_circleSpeeds = {10,10/3,10/9,10/27};
int []recursive_pathsInside;
float cross_section_resolution = 3;
float z_speed = 1000.0;
PVector scene_center;

void setup() {
  size(800, 800, P3D);
  I = 0;
  pathcount = 1;
  recursive_pathsInside = new int[recursive_levels];
  for (int j=0; j<recursive_levels; j++) {
    recursive_pathsInside[j] = pathcount;
    pathcount = pathcount*recursive_pathcounts[j];
  }
  scene_center = new PVector(width/2, height/2, 0);
  
  gif_start();
}

void draw() {
  gif_frame_start();
  
  translate(scene_center.x, scene_center.y, scene_center.z);
  background(0);
  lights();
  rotateX(PI/12);
  rotateY(PI/2);
  translate(0,-630,0);
  for (int p=0; p<pathcount; p++) { 
    noStroke();
    if (p%2 == 0)
      fill(128,0,0);
    if (p%2 == 1)
      fill(128,0,128);
    draw_path(p);
  }
  gif_frame_end();
}

void gif_start() {
  gifExport = new GifMaker(this, "export.gif", 100);
  gifExport.setRepeat(0); 
}

void gif_frame_start() {
  
  
  if (I == framecount) {
    gifExport.finish();
    exit();
  }  
}

void gif_frame_end() {
  I++;
  
  print(int(I));
  print('/');
  print(framecount);
  print('\n');
  
  gifExport.setDelay(20);
  gifExport.addFrame();
}

void draw_path(int p) {
 for (float j=0; j<pathstepcount; j++) {

    PVector point1 = path(j,p);
    PVector forward1 = path_derivative(j,p); 
    forward1.normalize();
    PVector up1 = new PVector();
    PVector.cross(point1, forward1, up1);
    up1.normalize();
    PVector right1 = new PVector();
    PVector.cross(up1, forward1, right1);
    right1.normalize();
    
    PVector point2 = path(j+1,p);
    PVector forward2 = path_derivative(j+1,p); 
    forward2.normalize();
    PVector up2 = new PVector();
    PVector.cross(point2, forward2, up2);
    up2.normalize();
    PVector right2 = new PVector();
    PVector.cross(up2, forward2, right2);
    right2.normalize();
    
    for (float a = 0; a < cross_section_resolution; a++) {
      
      PVector p_a1 = cross_section_path(a*2*PI/cross_section_resolution, point1, up1, right1);
      PVector p_a2 = cross_section_path((a+1)*2*PI/cross_section_resolution, point1, up1, right1);
      
      PVector p_b1 = cross_section_path(a*2*PI/cross_section_resolution, point2, up2, right2);
      PVector p_b2 = cross_section_path((a+1)*2*PI/cross_section_resolution, point2, up2, right2);
      
      beginShape();
      vertex( p_a1.x, p_a1.y, p_a1.z);
      vertex( p_a2.x, p_a2.y, p_a2.z);
      vertex( p_b1.x, p_b1.y, p_b1.z);
      endShape();
      beginShape();
      vertex( p_b2.x, p_b2.y, p_b2.z);
      vertex( p_b1.x, p_b1.y, p_b1.z);
      vertex( p_a2.x, p_a2.y, p_a2.z);
      endShape();
      
    }
  } 
}

PVector path(float t, int p) {
  t = t/pathstepcount;
  
  float x = 0;
  float y = 0;
  for (int j=0; j<recursive_levels; j++) {
    int K = int(j == 0);
    float recursive_P = p/recursive_pathsInside[j]%recursive_pathcounts[j];
    x += recursive_circleRs[j]*sin(I/framecount*2*PI*K + recursive_circleSpeeds[j]*2*PI*t + recursive_P/recursive_pathcounts[j]*2*PI);
    y += recursive_circleRs[j]*cos(I/framecount*2*PI*K + recursive_circleSpeeds[j]*2*PI*t + recursive_P/recursive_pathcounts[j]*2*PI);
  }

  return new PVector(x, z_speed*t, y);
}
PVector path_derivative(float t, int p) {
  t = t/pathstepcount;
  return PVector.sub(path(t+0.001,p), path(t-0.001,p)).normalize();
}

PVector cross_section_path(float angle, PVector point, PVector up, PVector right) {
  return PVector.add(point, PVector.add(PVector.mult(up,sin(angle)*5), PVector.mult(right,cos(angle)*5)));
}