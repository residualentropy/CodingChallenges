# Wisconsin Autonomous Perception Coding Challenge

### My Answer

My code is at `main.py`. The code at `Dev.ipynb` is the same thing in notebook form (where it was originally developed, before being copied into `main.py`). It gives the following output as `my_answer.png`:

![my_answer.png](https://github.com/residualentropy/CodingChallenges/blob/master/perception/my_answer.png?raw=true)

### Methodology

I came up with the following general steps:

1. Convert the image to the L\*a\*b\* colorspace and perform thresholding
2. Clean up the thresholded image with basic morphological operations (erosion and dilation)
3. Find the tops of all of the cones by going through the image one pixel at a time
4. Connect each of the tops of the cones to their nearest neighbors, split for each half
5. Find two lines that pass through their mean point and is at their mean angle

### What didn't work

- I tried using just the red channel of the image but that wasn't nearly fine-grained enough
- I tried using PCA on each half of the image (after thresholding) to see if that could work, but it was overly complicated and I never got it to work
- I was going to try some kind of optimization to find the two lines given only the points, but that would be very very slow and could get stuck in local minima

### Libraries

I used the following libraries:

- OpenCV
- Numpy
- Matplotlib (during development only)
