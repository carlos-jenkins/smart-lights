screw = 2.91;
screw_cover = 2.33;
height = 8;

width = 93.86;
length = 63.48;

module standoff() {
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

module board_plate() {
    linear_extrude(height=2.5)
        import("board_plate.dxf");

    half_standoff = (screw + screw_cover) / 2;

    translate([
        half_standoff, 
        half_standoff, 
        0
    ]) {
        standoff();
    }
    
    translate([
        width - half_standoff, 
        length - half_standoff, 
        0
    ]) {
        standoff();
    }
    
    translate([
        width - half_standoff, 
        half_standoff, 
        0
    ]) {
        standoff();
    }
    
    translate([
        half_standoff, 
        length - half_standoff, 
        0
    ]) {
        standoff();
    }
}

board_plate();