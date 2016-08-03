use <universal_bracket.scad>;

module punched_universal_bracket(
    servo_height,
    battery_height,
    thickness,
    bracket_width
) {
    difference() {
        universal_bracket(
            servo_height,
            battery_height,
            thickness,
            bracket_width,
            bottom_screw_size
        );

        // Bottom screw
        translate([bracket_width / 2, bracket_width / 2, 0]) {
            cylinder(
                h=thickness * 3,
                r1=bottom_screw_size / 2,
                r2=bottom_screw_size / 2,
                center=true
            );
        }
    }
}

module free_wheel_bracket(
    servo_height,
    battery_height,
    thickness,
    bracket_width,
    screw_size,
    screw_support
) {
    difference() {
        union() {
            // Main bracket
            punched_universal_bracket(
                servo_height,
                battery_height,
                thickness,
                bracket_width,
                bottom_screw_size
            );

            // Battery support
            translate([0, 0, servo_height - thickness]) {
                cube([bracket_width, bracket_width, thickness]);
            }

            // Servo screw support
            translate([bracket_width / 2, 0 , servo_height / 2]) { 
                rotate([90, 0, 0]) {
                    cylinder(
                        h=screw_support,
                        r1=screw_size * 1.5,
                        r2=screw_size * 1.1
                    );
                }
            }
        }

        // Servo screw insert
        translate([bracket_width / 2, 0 , servo_height / 2]) { 
            rotate([90, 0, 0]) {
                cylinder(
                    h=screw_support * 3,
                    r1=screw_size / 2,
                    r2=screw_size / 2,
                    center=true
                );
            }
        }
    }
}

servo_height = 20;
battery_height = 9.5;
thickness = 3;
bracket_width = 15;
screw_size = 4.85;
screw_support = 11.25;
bottom_screw_size = 3.90;

free_wheel_bracket(
    servo_height,
    battery_height,
    thickness,
    bracket_width,
    screw_size,
    screw_support,
    bottom_screw_size
);
