%octave
pkg load statistics %may need pkgg instal -forge statistics

load heat_points.txt

%filters
tf1 = heat_points(:,2) > -75.979;
tf2 = heat_points(:,2) < -75.950;
tf3 = heat_points(:,1) > 42.082;
tf4 = heat_points(:,1) < 42.093;
tf = tf1 & tf2 & tf3 & tf4;

c = heat_points(tf, :); %logical index subselect points that fall within boundary
c = abs(c); %account for negative longitude & flipped image
hist3(c, 100); %100 bins

