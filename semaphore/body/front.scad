module semaphore_front(
    width,
    length,
    thickness,
    light_width,
    light_length,
    separation
) {
    difference() {
        cube([width, length, thickness], center=true);
        cube(
            [light_width, light_length, thickness * 2],
            center=true
        );
        translate([0, - light_width - separation, 0]) {
            cube(
                [light_width, light_length, thickness * 2],
                center=true
            );
        }
        translate([0, light_width + separation, 0]) {
            cube(
                [light_width, light_length, thickness * 2],
                center=true
            );
        }
    }
}

width = 82;
length = 130;
thickness = 2;
light_width = 31.90;
light_length = 31.90;
separation = 10;

semaphore_front(
    width,
    length,
    thickness,
    light_width,
    light_length,
    separation
);