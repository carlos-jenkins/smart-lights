use <universal_bracket.scad>;

servo_height = 20;
battery_height = 9.5;
tickness = 4;
bracket_width = 20;

module free_wheel_bracket(
    servo_height,
    battery_height,
    tickness,
    bracket_width,
    screw_size
) {
    difference() {
        universal_bracket(
            servo_height,
            battery_height,
            tickness,
            bracket_width
        );
        translate([bracket_width / 2, 0 , servo_height / 2]) { 
            rotate([90, 0, 0]) {
                cylinder(
                    h=tickness * 2,
                    r1=(screw_size / 2),
                    r2=(screw_size / 2),
                    center=true
                );
            }
        }
    }
}

servo_height = 20;
battery_height = 9.5;
tickness = 4;
bracket_width = 20;
screw_size = 4.85;

free_wheel_bracket(
    servo_height,
    battery_height,
    tickness,
    bracket_width,
    screw_size
);
