# Parking Frenzy

![](anim-min.gif)

[Nicer animation](https://www.youtube.com/watch?v=t34qcpstTYk)

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
<p align="center"><img src="svgs/69c3e31d052cc6f278f4fd5d436a8cbe.svg?invert_in_darkmode" align=middle width=412.03396245pt height=29.58934275pt/></p>

which allows to compute all trailer positions from the derivatives of the desired trajectory of <img src="svgs/d4bd11686e685e56f3320fe149d80d16.svg?invert_in_darkmode" align=middle width=35.20368554999999pt height=24.65753399999998pt/>.

However, doing so more than a few times (even using computer algebra) quickly leads to very large expressions and computation time. This is mainly due to the repeated derivatives of the square root term.

### Using angles

The first trick is to use additional angle variables by rewriting the recursive equation as follows

<p align="center"><img src="svgs/360c957c7625ea6c60d1120b38b9ca31.svg?invert_in_darkmode" align=middle width=545.40973575pt height=39.452455349999994pt/></p>

This is useful because from the first derivative of the arc-tangent we get

<p align="center"><img src="svgs/1e0d1c11fc3692a45745cf77946b487d.svg?invert_in_darkmode" align=middle width=354.97668689999995pt height=39.713394599999994pt/></p>

and this expression is rational in (no square roots). Hence, the multiple derivatives <img src="svgs/a70db411e1a33b18202ebf7b9481e0dd.svg?invert_in_darkmode" align=middle width=48.620754599999984pt height=34.337843099999986pt/> of <img src="svgs/3431c263a302fd1db6cb715168289908.svg?invert_in_darkmode" align=middle width=39.09450434999999pt height=24.65753399999998pt/> can be computed from the derivatives of <img src="svgs/6347cbf489ed80f180d33a57b743e25a.svg?invert_in_darkmode" align=middle width=47.71701164999999pt height=24.65753399999998pt/> by successively applying product rules and quotient rules. In turn, the derivatives of <img src="svgs/32dfce1370b4e3e82209f3da7e7c0b10.svg?invert_in_darkmode" align=middle width=51.57171194999999pt height=24.65753399999998pt/> and <img src="svgs/254ae93246ab561cb999d65801b40262.svg?invert_in_darkmode" align=middle width=53.39817614999999pt height=24.65753399999998pt/> are obtained by applying chain rules. These product-, quotient- and chain-rules are higher order variant of the usual ones (more on this below).

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

To get the quotient rule for <img src="svgs/a79b98382d240e9a9ffbd6eb7ae7014f.svg?invert_in_darkmode" align=middle width=67.44880559999999pt height=24.65753399999998pt/>, one first obtains a rule for the reciprocal <img src="svgs/05d3043eab0f4e5440902a1b8fca69e9.svg?invert_in_darkmode" align=middle width=96.19858379999998pt height=24.65753399999998pt/>. This rule is obtained from the product rule and the equation <img src="svgs/fbd20db80429bd1a105e634ae0f5a9ed.svg?invert_in_darkmode" align=middle width=99.8513571pt height=24.65753399999998pt/>. The product rule is then applied again on <img src="svgs/fe3f2f532573e3d29d020fc29dcbd46e.svg?invert_in_darkmode" align=middle width=71.10157229999999pt height=24.65753399999998pt/>.

Next define

<p align="center"><img src="svgs/2a83e64e012427c1ff2f185bfacbecee.svg?invert_in_darkmode" align=middle width=141.64519875pt height=32.990165999999995pt/></p>

then

<p align="center"><img src="svgs/599f4993569e7ab8c7549794f008194f.svg?invert_in_darkmode" align=middle width=227.16701534999996pt height=47.1348339pt/></p>

This has two benefits: 1) the product rule uses simple coefficients convolution, 2) since high order derivatives tend to be numerically large, dividing them by <img src="svgs/9d6c5e19ffd270ead9ea60bbae1902d0.svg?invert_in_darkmode" align=middle width=13.64158619999999pt height=22.831056599999986pt/> leads to better "conditioned " computations. Note that the above is the same as computing the coefficients of the product of polynomials with coefficients <img src="svgs/affed31cd6a91b422fafefe0490e3287.svg?invert_in_darkmode" align=middle width=21.91128389999999pt height=29.190975000000005pt/> and <img src="svgs/269c9fdebb47178d570db923f16834ad.svg?invert_in_darkmode" align=middle width=21.97781519999999pt height=29.190975000000005pt/> and truncating the result at degree <img src="svgs/89f2e0d2d24bcf44db73aab8fc03252c.svg?invert_in_darkmode" align=middle width=7.87295519999999pt height=14.15524440000002pt/>. The corresponding quotient rule is obtained in the same way as above.


### High order composition rule

To complete the computations of <img src="svgs/a69e80fed79c7251863f7552dce583a5.svg?invert_in_darkmode" align=middle width=17.06057264999999pt height=22.831056599999986pt/>, we still need a high order composition rule to compute the derivatives of 

<p align="center"><img src="svgs/7e4e71db35fb7372d5a40fa9b45c8789.svg?invert_in_darkmode" align=middle width=146.15694555pt height=13.881256950000001pt/></p>

The first attempt was made using [Faa di Bruno's](https://en.wikipedia.org/wiki/Fa%C3%A0_di_Bruno%27s_formula) formula, in particular the form involving [Bell polynomials](https://en.wikipedia.org/wiki/Bell_polynomials#Recurrence_relations) since these can be easily implemented in code via a seemingly efficient recurrence relation. It turns out however that computing these polynomials this way quickly leads to very long computation times. I then stumbled on a [post](https://mathoverflow.net/questions/364036/combinatorics-of-multivariate-fa%C3%A0-di-bruno-formula) noting the "inefficiency" of Faa di Bruno formulae compared to power series approaches. Indeed, it is better to reconsider the problem from the point of view of formal power series. Our goal is to compute the first <img src="svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/> derivatives of the composite function <img src="svgs/a6d29c2900ac7b61baf6b84023b0e44d.svg?invert_in_darkmode" align=middle width=51.52411769999999pt height=24.65753399999998pt/> (at a given value of <img src="svgs/6f9bad7347b91ceebebd3ad7e6f6f2d1.svg?invert_in_darkmode" align=middle width=7.7054801999999905pt height=14.15524440000002pt/>)

To this end, let us look at the Taylor expansion of <img src="svgs/27280abcf92710218525f89d1f365008.svg?invert_in_darkmode" align=middle width=58.898576549999994pt height=24.65753399999998pt/> around <img src="svgs/8b839ae69dec8bfbdf995bcc1ad93dee.svg?invert_in_darkmode" align=middle width=36.29572979999999pt height=24.65753399999998pt/>.
<p align="center"><img src="svgs/0c0b7da81b2e765923a8eb18a5a328b3.svg?invert_in_darkmode" align=middle width=312.98644575pt height=41.486034149999995pt/></p>

and then, let us replace <img src="svgs/cdb4346e7e0053cb44dc04c5f12c862e.svg?invert_in_darkmode" align=middle width=28.921270949999986pt height=24.65753399999998pt/> by its Taylor series around <img src="svgs/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode" align=middle width=14.25802619999999pt height=14.15524440000002pt/>

<p align="center"><img src="svgs/a666fb9bf43d8057c644b43e9b72f9b5.svg?invert_in_darkmode" align=middle width=485.40961589999995pt height=53.2425333pt/></p>

Clearly, defining the power series

<p align="center"><img src="svgs/ea81422d9ff3b282289098b67de2608f.svg?invert_in_darkmode" align=middle width=214.1736234pt height=41.486034149999995pt/></p>

<p align="center"><img src="svgs/f054e0ca7df488092e04bc9f2d5e87d9.svg?invert_in_darkmode" align=middle width=141.385101pt height=16.438356pt/></p>

<p align="center"><img src="svgs/b193913ca49fcab9405f4992def000e2.svg?invert_in_darkmode" align=middle width=179.58451664999998pt height=41.486034149999995pt/></p>

we have that

<p align="center"><img src="svgs/3e13f54a432b5d3f3bdb45b734e8eb88.svg?invert_in_darkmode" align=middle width=473.01588344999993pt height=74.34741765pt/></p>

Hence, computing the first <img src="svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/> coefficients of the power series

<p align="center"><img src="svgs/cb37e00d46cebb22099fd2b1da0585ec.svg?invert_in_darkmode" align=middle width=102.98129325pt height=16.438356pt/></p>

we get the first <img src="svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/> derivatives of <img src="svgs/a6d29c2900ac7b61baf6b84023b0e44d.svg?invert_in_darkmode" align=middle width=51.52411769999999pt height=24.65753399999998pt/>. Furthermore, re-expressing everything in terms of <img src="svgs/affed31cd6a91b422fafefe0490e3287.svg?invert_in_darkmode" align=middle width=21.91128389999999pt height=29.190975000000005pt/> and <img src="svgs/269c9fdebb47178d570db923f16834ad.svg?invert_in_darkmode" align=middle width=21.97781519999999pt height=29.190975000000005pt/> we get rid of the factorial terms and end up manipulating polynomials. In turn, the (truncated) composition of polynomials can be implemented using the product rule for building the monomials one by one.

### Animation speed

To produce an animation of a car with many trailers, one chooses a trajectory <img src="svgs/d4bd11686e685e56f3320fe149d80d16.svg?invert_in_darkmode" align=middle width=35.20368554999999pt height=24.65753399999998pt/> for the last trailer's axle and then use the map <img src="svgs/417a5301693b60807fa658e5ef9f9535.svg?invert_in_darkmode" align=middle width=10.75343279999999pt height=14.15524440000002pt/> to compute all the other trailers and car positions. However doing so and using <img src="svgs/1327ee3255e3557f570b285d55d6f5b8.svg?invert_in_darkmode" align=middle width=35.55920774999999pt height=20.221802699999984pt/> leads to a jerky animation since the head car's speed generally varies wildly (high derivatives) over time. As a remedy, we impose the head car's rear axle speed (which can be computed from the derivatives of <img src="svgs/fed4fd57d90d2ab0789f75ca1fb9b5a2.svg?invert_in_darkmode" align=middle width=53.925215849999994pt height=24.65753399999998pt/> by integration of the equation

<p align="center"><img src="svgs/1abc5e890a058fd6cfa08157c4f5b317.svg?invert_in_darkmode" align=middle width=234.27507344999998pt height=50.152748249999995pt/></p>


### Note

Equations in this README file where typesetted with the help of [readme2tex](https://github.com/leegao/readme2tex)



