# Parking Frenzy

### Efficient maneuver computation for vehicles with many trailers

Explicit computation of control input for [non-holonomic](https://en.wikipedia.org/wiki/Nonholonomic_system) vehicles is a classical application example for the theory of [differential flatness](https://en.wikipedia.org/wiki/Flatness_(systems_theory)). In particular, it allows to determine the required steering profile of a car with trailers given the path profile that the last trailer axle should follow.

For instance, consider a car with two trailers. 

![](figures/train.png)

One may choose any (sufficiently differentiable) path <img src="svgs/f53eb0f7b75281603756896a69b3018d.svg?invert_in_darkmode" align=middle width=102.81019979999998pt height=27.6567522pt/> for the last trailer axle. From this path and its derivatives, all the other paths <img src="svgs/d7b553287fe0cae527f49076dde18b0c.svg?invert_in_darkmode" align=middle width=104.23716764999998pt height=27.6567522pt/> can be computed explicitly. The angle between the link <img src="svgs/171c56ba54530ae6055635392861c1d4.svg?invert_in_darkmode" align=middle width=36.52961069999999pt height=21.18721440000001pt/> and the link <img src="svgs/cbcb6907e71e1bbd11e61abdc726c05b.svg?invert_in_darkmode" align=middle width=36.52961069999999pt height=21.18721440000001pt/> is the required steering angle of the head car. Note also that the four-wheeled head car is equivalent to two two-wheeled trailers.

The equations are elementary, but naively applying them quickly leads to untractable expressions with growing numbers of trailers. 

### Recursive equations
The kinematics of the system implies the following equation
<p align="center"><img src="svgs/7bd011c3b87b419fc4d9f8b80557939a.svg?invert_in_darkmode" align=middle width=274.5978411pt height=42.4111644pt/></p>

Using <img src="svgs/b1525bb86e2565a9578158c562079c70.svg?invert_in_darkmode" align=middle width=166.63819259999997pt height=27.6567522pt/> and applying the above equation <img src="svgs/efcf8d472ecdd2ea56d727b5746100e3.svg?invert_in_darkmode" align=middle width=38.17727759999999pt height=21.18721440000001pt/> times, we get a map
<p align="center"><img src="svgs/a77430662ca9b67de1fcd7c1273e3096.svg?invert_in_darkmode" align=middle width=412.03396245pt height=29.58934275pt/></p>
which allows to compute all trailer positions from the derivatives of the desired trajectory of <img src="svgs/d4bd11686e685e56f3320fe149d80d16.svg?invert_in_darkmode" align=middle width=35.20368554999999pt height=24.65753399999998pt/>.

However, doing so more than a few times (even using computer algebra) quickly leads to very large expressions and computation time. This is mainly due to the repeated derivatives of the square root term.

### Using angles

The first trick is to use additional angle variables by rewriting the recursive equation as follows
<p align="center"><img src="svgs/a7b54b67451299756605243a90781a8f.svg?invert_in_darkmode" align=middle width=537.3826425pt height=39.452455349999994pt/></p>

This is useful because from the first derivative of the arc-tangent we get
<p align="center"><img src="svgs/1e0d1c11fc3692a45745cf77946b487d.svg?invert_in_darkmode" align=middle width=354.97668689999995pt height=39.713394599999994pt/></p>
and this expression is rational in (no square roots). Hence, the multiple derivatives <img src="svgs/2847a70544ff96fda68b9912890814ad.svg?invert_in_darkmode" align=middle width=48.620754599999984pt height=29.190975000000005pt/> of <img src="svgs/be7aa80b01a2c2c39ea4ed4cff441af6.svg?invert_in_darkmode" align=middle width=31.067411099999987pt height=24.65753399999998pt/> can be computed from the derivatives of <img src="svgs/6347cbf489ed80f180d33a57b743e25a.svg?invert_in_darkmode" align=middle width=47.71701164999999pt height=24.65753399999998pt/> by successively applying product rules and quotient rules. In turn, the derivatives of <img src="svgs/c1dee54b8aace34fac6027f0e9a39402.svg?invert_in_darkmode" align=middle width=43.54461869999999pt height=24.65753399999998pt/> and <img src="svgs/abf8c6ff8182a6059b1d51860f5375a2.svg?invert_in_darkmode" align=middle width=45.37108289999999pt height=24.65753399999998pt/> are obtained by applying chain rules. These product-, quotient- and chain-rules are higher order variant of the usual ones (more on this below).

### More intermediate variables

The second trick is to decompose the mapping <img src="svgs/417a5301693b60807fa658e5ef9f9535.svg?invert_in_darkmode" align=middle width=10.75343279999999pt height=14.15524440000002pt/> in sub-steps involving more intermediate variables (the derivatives of all <img src="svgs/acc433299a99053a1abda8186a07965d.svg?invert_in_darkmode" align=middle width=14.604341399999988pt height=14.15524440000002pt/>, not just <img src="svgs/07d7104fe13d9faea3e641ad3d053832.svg?invert_in_darkmode" align=middle width=13.89085829999999pt height=14.15524440000002pt/>). Differentiating the original relation <img src="svgs/b29adaa9e6ca7a666c0ebdbe30725f94.svg?invert_in_darkmode" align=middle width=114.74904044999998pt height=24.7161288pt/> (<img src="svgs/d09536de7e7712cdfc5d7544dfca70e7.svg?invert_in_darkmode" align=middle width=67.34383095pt height=22.831056599999986pt/> times), gives a map
<p align="center"><img src="svgs/83dd2c42c5963b7ca38c59d26c409dd3.svg?invert_in_darkmode" align=middle width=557.55191085pt height=23.497574099999998pt/></p>
And
<p align="center"><img src="svgs/7cb31372ed8c59110e804c05e9dea52b.svg?invert_in_darkmode" align=middle width=172.8972069pt height=15.251136449999997pt/></p>

### High order product and quotient rules
Computing the derivatives of the angles <img src="svgs/3cc1484752cc8ef69d55b6991e28be35.svg?invert_in_darkmode" align=middle width=17.78167709999999pt height=14.15524440000002pt/> is easy: first compute the derivatives of the products
<p align="center"><img src="svgs/5e5e17f4de0cc7bda295f2895eb90589.svg?invert_in_darkmode" align=middle width=214.87867665pt height=18.2666319pt/></p>
with the product rule and then compute the derivatives of the quotient of 
<p align="center"><img src="svgs/d23435a450c05899038b0f051088464a.svg?invert_in_darkmode" align=middle width=207.57252945pt height=18.2666319pt/></p>
with the quotient rule. The product rule is given by
<p align="center"><img src="svgs/abbdb186fdfbc5f2da82dc54c3104224.svg?invert_in_darkmode" align=middle width=321.6987939pt height=47.1348339pt/></p>
To get the quotient rule for <img src="svgs/a79b98382d240e9a9ffbd6eb7ae7014f.svg?invert_in_darkmode" align=middle width=67.44880559999999pt height=24.65753399999998pt/>, one first obtains a rule for the reciprocal <img src="svgs/05d3043eab0f4e5440902a1b8fca69e9.svg?invert_in_darkmode" align=middle width=96.19858379999998pt height=24.65753399999998pt/>. This rule is obtained from the product rule and the equation <img src="svgs/fbd20db80429bd1a105e634ae0f5a9ed.svg?invert_in_darkmode" align=middle width=99.8513571pt height=24.65753399999998pt/>. The product rule is then applied again on <img src="svgs/507ad28ff324a6f5a8ebe56f72f6fc62.svg?invert_in_darkmode" align=middle width=71.10157724999998pt height=29.168957400000025pt/>.

Next, defining
<p align="center"><img src="svgs/2a83e64e012427c1ff2f185bfacbecee.svg?invert_in_darkmode" align=middle width=141.64519875pt height=32.990165999999995pt/></p>
then
<p align="center"><img src="svgs/599f4993569e7ab8c7549794f008194f.svg?invert_in_darkmode" align=middle width=227.16701534999996pt height=47.1348339pt/></p>
This has two benefits: 1) the product rule uses simple coefficients convolution, 2) since high order derivatives tend to be numerically large, dividing them by <img src="svgs/9d6c5e19ffd270ead9ea60bbae1902d0.svg?invert_in_darkmode" align=middle width=13.64158619999999pt height=22.831056599999986pt/> leads to better "conditioned " computations. Note that the above is the same as computing the coefficients of the product of polynomials with coefficients <img src="svgs/affed31cd6a91b422fafefe0490e3287.svg?invert_in_darkmode" align=middle width=21.91128389999999pt height=29.190975000000005pt/> and <img src="svgs/269c9fdebb47178d570db923f16834ad.svg?invert_in_darkmode" align=middle width=21.97781519999999pt height=29.190975000000005pt/> and truncating the result at degree <img src="svgs/89f2e0d2d24bcf44db73aab8fc03252c.svg?invert_in_darkmode" align=middle width=7.87295519999999pt height=14.15524440000002pt/>.

