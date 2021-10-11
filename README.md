# AirDrumming
The air drumming software

## How to use
To use the software you will need drumsticks. Then at the top of one drumstick you will have mount a ball of green color and a ball of blue color on the other. To make the ball get a styrofoam ball and tape it with colored paper. Then put yellow bands on your knees. These can be made from colored paper too. The rectangles on the screen display the drums: hi-hat, snare, high tom, mid tom, floor tom and crash cymbal (from left to right). To play on the drum move the colored ball into the rectangle. To play the kick and the hi-hat pedal just move your knee up and down.

## Problems
- The color detection is not perfect and sometimes the balls become undetectable or get split into many parts.
- The leg bits tend to play multiple times or do not rest.
- There might be other colorful objects in the background.
- The sound mixer is far from perfect.
- It is hard for the program to detect playing at high bpm.

## Ideas
- Rather than playing on rectangle enter play when the up to down movement is detected inside the rectangle.
- Mark the instrument as unplayed when the drumstick/leg moves up by x pixels.
- Get a better boundary detection algorithm.
- Use better camera.
- Get a tracking algorithm to discard the colorful background objects.
