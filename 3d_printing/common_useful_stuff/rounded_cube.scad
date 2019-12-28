module rounded_cube(dimensions,r) {

  translate([r,r,0])
  cube(
      [dimensions[0]-2*r,
       dimensions[1]-2*r,
       dimensions[2]
      ]);

  translate([r,0,r])
  cube(
      [dimensions[0]-2*r,
       dimensions[1],
       dimensions[2]-2*r
      ]);

  translate([0,r,r])
  cube(
      [dimensions[0],
       dimensions[1]-2*r,
       dimensions[2]-2*r
      ]);

  translate([r,r,r])
  sphere(r=r, $fn=100);

  translate([dimensions[0]-r,r,r])
  sphere(r=r, $fn=100);

  translate([r,dimensions[1]-r,r])
  sphere(r=r, $fn=100);

  translate([dimensions[0]-r,dimensions[1]-r,r])
  sphere(r=r, $fn=100);

  translate([r,r,dimensions[2]-r])
  sphere(r=r, $fn=100);

  translate([dimensions[0]-r,r,dimensions[2]-r])
  sphere(r=r, $fn=100);

  translate([r,dimensions[1]-r,dimensions[2]-r])
  sphere(r=r, $fn=100);

  translate([dimensions[0]-r,dimensions[1]-r,dimensions[2]-r])
  sphere(r=r, $fn=100);

  translate([r,r,r])
  cylinder($fn=100,r=r,h=dimensions[2]-2*r);

  translate([dimensions[0]-r,r,r])
  cylinder($fn=100,r=r,h=dimensions[2]-2*r);

  translate([r,dimensions[1]-r,r])
  cylinder($fn=100,r=r,h=dimensions[2]-2*r);

  translate([dimensions[0]-r,dimensions[1]-r,r])
  cylinder($fn=100,r=r,h=dimensions[2]-2*r);

  translate([r,r,r])
  rotate([270,0,0])
  cylinder($fn=100,r=r,h=dimensions[1]-2*r);

  translate([dimensions[0]-r,r,r])
  rotate([270,0,0])
  cylinder($fn=100,r=r,h=dimensions[1]-2*r);

  translate([r,r,dimensions[2]-r])
  rotate([270,0,0])
  cylinder($fn=100,r=r,h=dimensions[1]-2*r);

  translate([dimensions[0]-r,r,dimensions[2]-r])
  rotate([270,0,0])
  cylinder($fn=100,r=r,h=dimensions[1]-2*r);

  translate([r,r,r])
  rotate([0,90,0])
  cylinder($fn=100,r=r,h=dimensions[0]-2*r);

  translate([r,dimensions[1]-r,r])
  rotate([0,90,0])
  cylinder($fn=100,r=r,h=dimensions[0]-2*r);

  translate([r,r,dimensions[2]-r])
  rotate([0,90,0])
  cylinder($fn=100,r=r,h=dimensions[0]-2*r);

  translate([r,dimensions[1]-r,dimensions[2]-r])
  rotate([0,90,0])
  cylinder($fn=100,r=r,h=dimensions[0]-2*r);

}
