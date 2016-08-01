module universal_bracket(
        servo_height,
        battery_height,
        tickness,
        bracket_width
    ) {
    base_height = servo_height + battery_height;
    cube([
        bracket_width, tickness, base_height + tickness
    ]);
    cube([bracket_width, bracket_width, tickness]);
    translate([0, 0, base_height]) {
        cube([bracket_width, bracket_width, tickness]);
    } 
}

servo_height = 20;
battery_height = 9.5;
tickness = 4;
bracket_width = 15;

universal_bracket(
    servo_height,
    battery_height,
    tickness,
    bracket_width
);
