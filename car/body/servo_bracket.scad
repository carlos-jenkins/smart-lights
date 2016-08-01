use <universal_bracket.scad>;

module servo_bracket(
    servo_height,
    servo_width,
    battery_height,
    tickness,
    bracket_width
) {
    universal_bracket(
        servo_height,
        battery_height,
        tickness,
        bracket_width
    );
    translate([bracket_width + servo_width, 0, 0]) {
        universal_bracket(
            servo_height,
            battery_height,
            tickness,
            bracket_width
        );
    }
    cube([
        bracket_width * 2 + servo_width, 
        bracket_width, tickness
    ]);
}

servo_height = 20;
servo_width = 41;
battery_height = 9.5;
tickness = 3;
bracket_width = 15;

servo_bracket(
    servo_height,
    servo_width,
    battery_height,
    tickness,
    bracket_width
);
