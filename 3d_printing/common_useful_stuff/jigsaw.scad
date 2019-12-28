module hex_jigsaw(r,h,tolerance) {

  //tolerance is for the negative jigsaw, and works for low positive values

  translate([-sqrt(2)*r,0,0])
  {
    cylinder(r=r+tolerance, h=h, $fn=40);

    rotate([0,0,45]) {
      translate([r,-r,0])
        difference() {
          fourth_anticircle(r,h,tolerance);
          rotate([0,0,-45])translate([0,0,-1])
              cube([r,r,h+2]);
        }
      translate([0,-r,0])
        cube([r,r,h]);
    }
    mirror()
    rotate([0,0,45+180]) {
      translate([r,-r,0])
        difference() {
          fourth_anticircle(r,h,tolerance);
          rotate([0,0,-45])translate([0,0,-1])
              cube([r,r,h+2]);
        }
      translate([0,-r,0])
        cube([r,r,h]);
    }
  }
  module fourth_anticircle(r,h,tolerance) {
    difference() {
      cube([r,r,h]);
      translate([r,r,-1])
      cylinder(r=r-tolerance,h=h+2, $fn=40);
    }
  }
}

