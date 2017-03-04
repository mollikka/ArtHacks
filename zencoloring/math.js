function rest_friction(value, minimum) {
  if (Math.abs(value)<minimum) {return 0}
  else {return value}
}
