# Parking Frenzy

### Efficient maneuver computation for vehicles with many trailers

Explicit computation of control input for [non-holonomic](https://en.wikipedia.org/wiki/Nonholonomic_system) vehicles is a classical application example for the theory of [differential flatness](https://en.wikipedia.org/wiki/Flatness_(systems_theory)). In particular, it allows to determine the required steering profile of a car with trailers given the path profile that the last trailer axle should follow.

For instance, consider a car with two trailers. 

![](figures/train.png)

One may choose any (sufficiently differentiable) path <img src="svgs/f53eb0f7b75281603756896a69b3018d.svg?invert_in_darkmode" align=middle width=102.81019979999998pt height=27.6567522pt/> for the last trailer axle. From this path and its derivatives, all the other paths <img src="svgs/d7b553287fe0cae527f49076dde18b0c.svg?invert_in_darkmode" align=middle width=104.23716764999998pt height=27.6567522pt/> can be computed explicitly. The angle between the link <img src="svgs/171c56ba54530ae6055635392861c1d4.svg?invert_in_darkmode" align=middle width=36.52961069999999pt height=21.18721440000001pt/> and the link <img src="svgs/cbcb6907e71e1bbd11e61abdc726c05b.svg?invert_in_darkmode" align=middle width=36.52961069999999pt height=21.18721440000001pt/> is the required steering angle of the head car. Note also that the four-wheeled head car is equivalent to two two-wheeled trailers.

The equations are elementary, but naively applying them quickly leads to untractable expressions with growing numbers of trailers.

### Recursive equations

<p align="center"><img src="svgs/5181a57f817b897366c0059ed957f3c2.svg?invert_in_darkmode" align=middle width=440.5529864999999pt height=42.4111644pt/></p>

with

<p align="center"><img src="svgs/9a0100796489988e70fec2547432a130.svg?invert_in_darkmode" align=middle width=200.77081694999998pt height=17.2895712pt/></p>


