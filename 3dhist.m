pkg load statistics 
load heat_points.txt


%filters
tf1 = heat_points(:,2) > -75.979;
tf2 = heat_points(:,2) < -75.962;
tf3 = heat_points(:,1) > 42.082;
tf4 = heat_points(:,1) < 42.093;
tf = tf1 & tf2 & tf3 & tf4;

c = heat_points(tf, :);
c = abs(c);
hist3(c, 100);

