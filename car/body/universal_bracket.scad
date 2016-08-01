module universal_bracket(
        servo_height,
        battery_height,
        thickness,
        bracket_width
    ) {
    base_height = servo_height + battery_height;
    cube([
        bracket_width, thickness, base_height + thickness
    ]);
    cube([bracket_width, bracket_width, thickness]);
    translate([0, 0, base_height]) {
        cube([bracket_width, bracket_width, thickness]);
    } 
}

servo_height = 20;
battery_height = 9.5;
thickness = 3;
bracket_width = 15;

universal_bracket(
    servo_height,
    battery_height,
    thickness,
    bracket_width
);
