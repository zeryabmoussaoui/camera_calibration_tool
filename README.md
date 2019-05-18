**Author :** [Zeryab Moussaoui](https://fr.linkedin.com/in/zeryab-moussaoui-9a728029)
**Contributer:**  [Raphael Casimir](https://fr.linkedin.com/in/rapha%C3%ABl-casimir-47068691)

# Real time camera calibration tool 

A very simple tool to calibrate your monocular camera.
 
## Requirements

Python 2.7.12 is supported, but should also work on Python3. 

The following libraries shall be installed :
* numpy
* pyyaml
* opencv-python 

## Installation

* Download the github project (zip)
* Unzip and copy all files in any directory.

## Howto

### Find camera id

You shall first find your camera id , otherwise install v4l2-tools and run :
```
v4l2-ctl --list-devices
```
Which outputs :

```
Integrated Camera (usb-0000:00:1a.0-1.6):
        /dev/video*0*
```

### Preparation

Print the [chessboard.png](./chessboard.png) and stick it to a flat surface.

###  Launch the tool

Run : 
```
python calibration_calibration
```
it will display a video stream :

![](https://i.ibb.co/3pJM3NL/calibration.png)

###  Taking  chessboard images

Depending on your environment, move either the camera or the cheesboard in all the operation.

Press [Space] on the displayed screen, if corners are detected you will see:

![](https://i.ibb.co/8mMGSv3/chessboard-2.png)

Repeat operation to get at least 10 images 

###  Calibrate

Press [c] to compute calibration , it will save them in a yaml file :

```
camera_matrix:
- - 611.4552961374491
  - 0.0
  - 315.59196871694695
- - 0.0
  - 590.4987441125558
  - 225.73019949244863
- - 0.0
  - 0.0
  - 1.0
dist_coeff:
- - -0.42142237717306885
  - 0.3413019078047165
  - 5.686155424228582e-05
  - 0.00041026072376253945
  - 0.01644419849720093

```

You can add more images using [space] and perform calibration again to see of mean error is descreasing. 

### Other command
Press :
* [ESC] to exit.
* [r] to reset operation.
