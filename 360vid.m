fps = 30degrees = 360duration = 5azimuth_i = 80elevation = 30frames = duration * fpsincrement = degrees / framesangles = [azimuth_i:increment:(azimuth_i + degrees)];for i = angles  %figure ("visible", "off");  view(i, elevation)  %sleep(0.5)  name = strcat('prod/', mat2str(i*10), '.png')  print(name, '-dpng', '-mono', '-S1920,1080')endfor