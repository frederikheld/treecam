# Research on Lens Shading Compensation for the PiCamera

This topic is relevant for you if you're planning to use the original PiCamera module it a third-party lens like the ArduCam camera modules. 

Lens shading occurs when the sensor is used with a lens that alters the angle at which light falls onto the sensor by a different amount going from the center to the edges of the picture. This happens with every lens and the PiCamera module compensates for the shift introduced by the original lens. If the camera module is used with any third-party lens, the compensation will most probably not fit to the lens and the shading will be visible. The correction has to configured according to the lens then.

Lens shading correction with the PiCam is not trivial. The following links provide information on how to do it:

* [Announcement of the PiCamera module V2](https://www.raspberrypi.org/blog/new-8-megapixel-camera-board-sale-25/). The post mentions lens shading.
* [Lens shading calibration for ArduCam lenses](https://www.arducam.com/docs/cameras-for-raspberry-pi/native-raspberry-pi-cameras/lens-shading-calibration/). Well-written tutorial with examples for the effect and how it looks compensated. It also comes with presets for ArduCam lenses which can be taken as a basis to correct lenses from other vendors. Unfortunately the approach includes re-compiling the camera C code. There must be a simpler way. (updated on January 7th 2021)
* [Tutorial and discussion on custom lens shading tables](https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=190586&sid=ccaae62a565eae381e01a203ae385674) (posted on August 10th 2017)
* [Reserach on lens shading correction of the RasPi Cam with third-party lenses](https://arxiv.org/abs/1911.13295)
* [PR that offers to add lens shading correction to `picamera`](https://github.com/waveform80/picamera/pull/470) Open since 2018. Currently maintained in a fork that is available as [`picamerax`](https://pypi.org/project/picamerax/).

Conclusion: Use [`picamerax`](https://pypi.org/project/picamerax/) instead of [`picamera`](https://pypi.org/project/picamera/).