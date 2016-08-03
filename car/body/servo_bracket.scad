use <free_wheel_bracket.scad>;

module servo_hole(
    bracket_width,
    thickness,
    servo_screw_size,
    servo_mount_hole_width,
    servo_mount_hole_height
) {
    half_screw = servo_screw_size / 2;

    translate([
        bracket_width - half_screw - servo_mount_hole_width,
        0,
        servo_mount_hole_height + half_screw
    ]) {
        rotate([90, 0, 0]) {
            cylinder(
                h=thickness * 3,
                r1=half_screw,
                r2=half_screw,
                center=true
            );
        }
    }
}

module servo_side_bracket(
    servo_height,
    battery_height,
    thickness,
    bracket_width,
    bottom_screw_size,
    servo_screw_size
) {
    // FIXME: Parametrize
    servo_mount_hole_width = 2.55;
    servo_mount_hole_height = 3.25;
    servo_mount_hole_distance = 6;

    difference() {
        punched_universal_bracket(
            servo_height,
            battery_height,
            thickness,
            bracket_width,
            bottom_screw_size
        );

        servo_hole(
            bracket_width,
            thickness,
            servo_screw_size,
            servo_mount_hole_width,
            servo_mount_hole_height
        );

        translate([
            0, 0, servo_mount_hole_distance + servo_screw_size
        ]) {
            servo_hole(
                bracket_width,
                thickness,
                servo_screw_size,
                servo_mount_hole_width,
                servo_mount_hole_height
            );
        }
    }
}

module servo_bracket(
    servo_height,
    servo_width,
    battery_height,
    thickness,
    bracket_width,
    bottom_screw_size,
    servo_screw_size
) {
    servo_side_bracket(
        servo_height,
        battery_height,
        thickness,
        bracket_width,
        bottom_screw_size,
        servo_screw_size
    );
    translate([bracket_width * 2 + servo_width, 0, 0]) {
        mirror() {
            servo_side_bracket(
                servo_height,
                battery_height,
                thickness,
                bracket_width,
                bottom_screw_size,
                servo_screw_size
            );
        }
    }
    translate([0, 0 , servo_height + battery_height]) {
        cube([
            bracket_width * 2 + servo_width, 
            bracket_width, thickness
        ]);
    }
}

servo_height = 20;
servo_width = 41;
battery_height = 9.5;
thickness = 3;
bracket_width = 15;
bottom_screw_size = 3.90;
servo_screw_size = 3.35;

servo_bracket(
    servo_height,
    servo_width,
    battery_height,
    thickness,
    bracket_width,
    bottom_screw_size,
    servo_screw_size
);
