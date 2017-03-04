var SVGNS = "http://www.w3.org/2000/svg";

function circles_parameterized_with_border(parentelement, f_x, f_y, f_r, i_min, i_max, color, border_width, border_color) {
  circles_parameterized(parentelement, f_x, f_y, f_r, i_min, i_max, border_color);
  circles_parameterized(parentelement, f_x, f_y, function(x){return f_r(x)-border_width}, i_min, i_max, color);
}

function circles_parameterized(parentelement,f_x, f_y, f_r, i_min, i_max, color) {
  var points = []
  var radiuses = []
  for (var i=i_min; i<=i_max; i++) {
    points.push([f_x(i),f_y(i)]);
    radiuses.push(f_r(i));
  }
  circles(parentelement, points, radiuses, color);
}

function fancypath_parameterized_with_border(parentelement, f_x, f_y, f_w, i_min, i_max,
    color, border_width, border_color) {
  fancypath_parameterized(parentelement,f_x, f_y, f_w, i_min, i_max, border_color)
  fancypath_parameterized(parentelement,f_x, f_y, function(x){return f_w(x)-border_width}, i_min, i_max, color)
}

function fancypath_parameterized(parentelement,f_x, f_y, f_w, i_min, i_max, color) {
  var path = []
  var widths = []
  for (var i=i_min; i<=i_max; i++) {
    path.push([f_x(i),f_y(i)]);
    widths.push(f_w(i));
  }
  fancypath(parentelement, path, widths, color);
}

function fancypath_with_border(parentelement,points,widths,color,border_width,border_color) {
  fancypath(parentelement, points, widths, border_color);
  fancypath(parentelement, points, widths.map(function(x){return x-border_width}), color);
}

function fancypath(parentelement, points, widths, color) {
  for (var i=0; i<points.length-1; i++) {
    el = fancyline(parentelement,points[i],points[i+1],widths[i],widths[i+1],color);
  }
  for (var i=0; i<points.length; i++) {
    el = circle(parentelement, points[i], widths[i]/2,color);
  }

}

function circles_with_border(parentelement, points, radiuses, color, border_width, border_color) {
  circles(parentelement, points, radiuses, border_color);
  circles(parentelement, points, radiuses.map(function(x){return x-border_width}), color)
}

function circles(parentelement, points, radiuses, color) {
  for (var i=0; i<points.length; i++) {
    circle(parentelement, points[i], radiuses[i], color)
  }
}

function circle(parentelement, point, radius, color) {
  var shape = document.createElementNS(SVGNS, "circle");
  shape.setAttributeNS(null, "cx", point[0]);
  shape.setAttributeNS(null, "cy", point[1]);
  shape.setAttributeNS(null, "r",  radius);
  shape.setAttributeNS(null, "fill", color); 
  parentelement.appendChild(shape);

}

function fancyline(parentelement, point1, point2, width1, width2, color) {
  var x1 = point1[0];
  var y1 = point1[1];
  var x2 = point2[0];
  var y2 = point2[1];
  var dx = x2-x1;
  var dy = y2-y1;
  var angle = Math.atan2(dy,dx);
  var w1 = width1/2;
  var w2 = width2/2;
  

  var shape = document.createElementNS(SVGNS, "polygon")
  
  //pp1 : left of point1
  var ppx1 = x1 + w1*Math.cos(angle+Math.PI/2);
  var ppy1 = y1 + w1*Math.sin(angle+Math.PI/2);
  //pp2 : left of point2
  var ppx2 = x2 + w2*Math.cos(angle+Math.PI/2);
  var ppy2 = y2 + w2*Math.sin(angle+Math.PI/2);
  //pp3 : right of point2
  var ppx3 = x2 + w2*Math.cos(angle-Math.PI/2);
  var ppy3 = y2 + w2*Math.sin(angle-Math.PI/2);
  //pp4 : right of point1
  var ppx4 = x1 + w1*Math.cos(angle-Math.PI/2);
  var ppy4 = y1 + w1*Math.sin(angle-Math.PI/2);

  shape.setAttributeNS(null, "points", 
      [ppx1+","+ppy1, ppx2+","+ppy2, ppx3+","+ppy3, ppx4+","+ppy4].join(" "))
  shape.setAttributeNS(null, "fill", color)

  parentelement.appendChild(shape);

}

