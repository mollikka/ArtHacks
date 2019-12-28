

module hexgrid(hexcoord_list, r) {
  h = 2*sqrt(3/4);

  V = [0, h*r, 0];
  U = [3/4*h*r, h*r/2, 0];

  for (vec = hexcoord_list) {
    i = vec[0];
    j = vec[1];

    translate(i*V + j*U)
    children();
  }

}
