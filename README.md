# PythonHandTrackingVolumeControl 

### Info
This python program is made for controlling your PC volume from your phone using hand tracking.
Hand tracking is achieved with cv2 and mediapipe.
Video communication is achieved with an app called IP Webcam which you install on your phone. IP Webcam hosts a website from which you can pull video from.
If you have a separate phone only for this, it is recommended to turn it into a dedicated IP webcam. You can do this on your phone settings
under --> Power management/Stream on device boot.
### Controls
pinky down => set volume, 
distance between index and thumb == volume % 
be careful how your phone is rotated if the volume constantly changes try flipping the phone.
### Setup
First run setup.py. There you will input your targeted fps (30 is recommended and works fine), smoothness (how volume percentage changes according to your finger movement) and your url.
NOTE: url will be displayed on your phone when you begin the stream
### More
minDist and maxDist should be adjusted by your preference and on your system. Minimum distance represents the distance between your thumb and index finger that will set the volume to 0 
maxDist represents the exact same thing just to set the volume to 100%
test.py should be ignored. 
url should use http not https or you will get an error
