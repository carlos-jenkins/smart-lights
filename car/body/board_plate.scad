module standoff(height, screw, screw_cover) {
    difference() {
        cylinder(
            h=height,
            r1=(screw + screw_cover) / 2,
            r2=(screw + screw_cover) / 2,
            $fn=32
        );
        translate([0, 0, -1]) {
            cylinder(
                h=height * 2,
                r1=screw / 2,
                r2=screw / 2,
                $fn=8
            );
        }
    }
}


module board_plate(
    width,
    lenght,
    thickness,
    screw,
    screw_cover,
    height,
    separation,
) {
    standoff = screw + screw_cover;
    standoff_separation = separation - standoff;

    cube([width, lenght, thickness], center=true);
    
    translate([standoff_separation / 2, 0, 0]) {
        standoff(height + thickness, screw, screw_cover);
    }
    translate([-standoff_separation / 2, 0, 0]) {
        standoff(height + thickness, screw, screw_cover);
    }
    // cube([separation, lenght, thickness * 2], center=true);
}


// Standoffs
screw = 3.28;
screw_cover = 2.33;
height = 8;
separation = 63.48;

// Base plate
width = 80;
length = 15;
thickness = 2.5;


board_plate(
    width,
    length,
    thickness,
    screw,
    screw_cover,
    height,
    separation
);
