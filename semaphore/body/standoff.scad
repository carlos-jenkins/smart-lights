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


// Standoffs
screw = 3.28;
screw_cover = 2.33;
height = 80;

standoff(height, screw, screw_cover);