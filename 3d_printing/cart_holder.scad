//Amount of cart slots
cart_count = 2; //[1:1:8]
//Cart type
cart_type = 2; //[0:Snes PAL, 1:Snes NTSC, 2:N64, 3:Gameboy/GBA, 4:DS/3DS]


module cart_cup(cup_height, cup_width, cup_depth, cart_hole_depth) {
    
    difference() {
        translate([0,cup_depth/2,0])
        union() {
            hull() {
                translate([cup_depth/2,0,0])
                cylinder(h=cup_height, d=cup_depth);
                
                translate([cup_width-cup_depth/2,0,0])
                cylinder(h=cup_height, d=cup_depth);
            }
        }
        translate([cup_width/2,0,cup_height-cart_hole_depth])
        children();
    }
}
    
module snescart_pal() {
    translate([-130/2,5,0])
    linear_extrude(88)
    polygon([[0,0],[130,0],
            [130,10],[127,16],[120,18],[100,20],[70,22],
            [60,22],[30,20],[10,18],[3,16],[0,10]]);
    
};


module snescart_ntsc() {
    translate([-130/2,5,0])
    linear_extrude(88)
    polygon([
        [-4,0],[-4,19],[17,19],[17,22],
        [113,22],[113,19],[134,19],[134,0]    
    ]);
    
};

module gameboycart() {
    translate([-58/2,3,0])
    linear_extrude(65)
    polygon([[0,0],[58,0],
            [58,8],[0,8]]);
    
};

module dscart() {
    translate([-34/2,3,0])
    linear_extrude(35)
    polygon([[0,0],[34,0],
            [34,4.5],[0,4.5]]);
    
};

module n64cart() {
    translate([-118/2,5,0])
    linear_extrude(76)
    polygon([[0,0],[0,9],[1,13],[2,15],[3,16],[6,18],[9,19],
            [118-9,19],[118-6,18],[118-3,16],[118-2,15],[118-1,13],[118,9],[118,0]]);
    
};

module cart_stand(  amount_of_carts, delta_y, delta_h, angle,
                    cup_height, cup_width, cup_depth, cart_hole_depth) {

    cut_from_bottom = sin(angle)*cup_depth;
                        
    difference() {
        union() {
            for(i = [0:amount_of_carts-1]) {
                translate([0, -i*delta_y, -cut_from_bottom])
                rotate([angle, 0, 0])
                cart_cup(   cup_height + i*delta_h, cup_width, cup_depth,  
                            cart_hole_depth) 
                #children();
            }
        }
        //ground
        translate([0, -delta_y*amount_of_carts, -cut_from_bottom])
        cube([cup_width, delta_y*(amount_of_carts+1), cut_from_bottom]);
    }
}

//cart_stand(  amount_of_carts, delta_y, delta_h, angle,
//             cup_height, cup_width, cup_depth, cart_hole_depth)

//cart_type: [0:Snes PAL, 1:Snes NTSC, 2:N64, 3:Gameboy/GBA, 4:DS/3DS]

if (cart_type == 0) {
    cart_stand(cart_count, 30, 15, 30, 30, 150, 30, 15) snescart_pal();
}
if (cart_type == 1) {
    cart_stand(cart_count, 30, 15, 30, 30, 150, 30, 15) snescart_ntsc();
}
if (cart_type == 2) {
    cart_stand(cart_count, 26, 15, 30, 30, 130, 26, 15) n64cart();
}
if (cart_type == 3) {
    cart_stand(cart_count, 14, 8, 30, 15, 68, 14, 6) gameboycart();
}
if (cart_type == 4) {
    cart_stand(cart_count, 9, 5, 30, 12, 40, 10, 6) dscart();
}
