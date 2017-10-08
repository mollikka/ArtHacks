difference() {
  scale([1,1,0.3])
  surface(file = "400x200/map_0_0.png", convexity = 5);
  translate([0,0,-1])
  cube([400,200,2]);
}
