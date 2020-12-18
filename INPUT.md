# Parking Frenzy

### Efficient maneuver computation for vehicles with many trailers

Explicit computation of control input for [non-holonomic](https://en.wikipedia.org/wiki/Nonholonomic_system) vehicles is a classical application example for the theory of [differential flatness](https://en.wikipedia.org/wiki/Flatness_(systems_theory)). In particular, it allows to determine the required steering profile of a car with trailers given the path profile that the last trailer axle should follow.

For instance, consider a car with two trailers. 

![](figures/train.png)

One may choose any (sufficiently differentiable) path $(x_1(s),y_1(s))^T$ for the last trailer axle. From this path and its derivatives, all the other paths $(x_k(s),y_k(s))^T$ can be computed explicitly. The angle between the link $3-4$ and the link $4-5$ is the required steering angle of the head car. Note also that the four-wheeled head car is equivalent to two two-wheeled trailers.
A formula $x+2=y^2$:
$$\alpha=\sin(x)$$

One more formula

$$
\begin{pmatrix}
x_{k+1} \\
y_{k+1}
\end{pmatrix}
=
\begin{pmatrix}
x_{k} \\
y_{k}
\end{pmatrix}
+
\frac{L_k}{\sqrt{x_{k}'^2 + y_{k}'^2}}
\begin{pmatrix}
x_{k}' \\
y_{k}'
\end{pmatrix}
=
\begin{pmatrix}
x_{k} \\
y_{k}
\end{pmatrix}
+
L_k
\begin{pmatrix}
\cos{\alpha_k} \\
\sin{\alpha_k}
\end{pmatrix}
$$

with

$$ \alpha(s) = \arctan_2(x_{k}'(s),y_{k}'(s)) $$


