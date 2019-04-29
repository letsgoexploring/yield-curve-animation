# Yield Curve Animation

An animated visualization of the US Treasury yield curve from January 1965 to the present. Code is available in the "Python " directory as either a Jupyter Notebook or a Python script. 

The code uses daily US Treasury yield data from FRED (https://fred.stlouisfed.org/) to construct an animated visualization of the US Treasury yield curve from January 1965 through the present. Data are downloaded using the fredpy module (https://github.com/letsgoexploring/fredpy-package). Animation is saved to eithe .mp4 or .ogv format using ffmpeg (https://ffmpeg.org/).