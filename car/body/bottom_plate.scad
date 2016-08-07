module hole(
    bracket_width,
    screw_size,
    thickness
) {
    translate([bracket_width / 2, bracket_width / 2, 0]) {
        cylinder(
            h=thickness * 3,
            r1=screw_size / 2,
            r2=screw_size / 2,
            center=true
        );
    }
}

module bottom_plate(
    width,
    length,
    thickness,
    bracket_width,
    screw_size
) {
    difference() {
        cube([width, length, thickness]);
        
        translate([0, 0, 0]) {
            hole(bracket_width, screw_size, thickness);
        }
        
        translate([width - bracket_width, 0, 0]) {
            hole(bracket_width, screw_size, thickness);
        }
        
        translate([0, length - bracket_width, 0]) {
            hole(bracket_width, screw_size, thickness);
        }
        
        translate([width - bracket_width, length - bracket_width, 0]) {
            hole(bracket_width, screw_size, thickness);
        }
    }
}


width = 80;
length = 59.50;
thickness = 2.5;

bracket_width = 15;
screw_size = 3.90;

bottom_plate(
    width,
    length,
    thickness,
    bracket_width,
    screw_size
);