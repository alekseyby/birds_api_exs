CREATE TABLE bird_colors_info as SELECT color, COUNT(*)
    FROM birds
    GROUP BY color;