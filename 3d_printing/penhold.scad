holder_radius = 46;
holder_thickness = 3;
holder_height = 30;
tube_bottom_thickness = 1;
pen_count = 16;
pen_radius = 4.5;
pen_length = 150;
rotx = 30;
rotz = -60;

{ // pen model for editor preview
    for (a=[1:360/pen_count:360]) {
        rotate([0,0,a])
        translate([holder_radius,0,0])
        rotate([rotx,0,rotz])
        %cylinder(h=pen_length, r = pen_radius);
    }
}

//intermediate variables
r = pen_radius+holder_thickness;
bot_shift = tan(rotx)*r;
cutoff_h = 2*sin(rotx)*r;
cylinder_length = cutoff_h*2 + holder_height;
cylinder_length = 2*tan(rotx)*r + 1/cos(rotx)*holder_height;
cutoff_r = cylinder_length + holder_radius + r; //upper bound of each var

difference() {
  { //material part of the tubes
    for (a=[1:360/pen_count:360]) {
      rotate([0,0,a])
      translate([holder_radius,0,0])
      rotate([rotx,0,rotz])
      translate([0,0,-bot_shift])
      cylinder(h=cylinder_length, r = pen_radius + holder_thickness);
    }
  }
  difference() {
    {//hole part of the tubes
      for (a=[1:360/pen_count:360]) {
        rotate([0,0,a])
        translate([holder_radius,0,0])
        rotate([rotx, 0, rotz])
        translate([0,0,-bot_shift])
        cylinder(h=cylinder_length, r = pen_radius);
      }
    }
    //stop drilling that hole before hitting the bottom
    cylinder(h=tube_bottom_thickness, r=cutoff_r);
  }
  //cut out the bottom
  translate([0,0,-cutoff_h])
  cylinder(h=cutoff_h, r = cutoff_r);
  //cut out the top
  translate([0,0,holder_height])
  cylinder(h=cutoff_h, r = cutoff_r);
}
