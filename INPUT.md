# Parking Frenzy

![](anim-min.gif)

[Nicer animation](https://www.youtube.com/watch?v=t34qcpstTYk)

### Efficient maneuver computation for vehicles with many trailers

Explicit computation of control input for [non-holonomic](https://en.wikipedia.org/wiki/Nonholonomic_system) vehicles is a classical application example for the theory of [differential flatness](https://en.wikipedia.org/wiki/Flatness_(systems_theory)). In particular, it allows to determine the required steering profile of a car with trailers given the path profile that the last trailer axle should follow.

For instance, consider a car with two trailers. 

![](figures/train.png)

One may choose any (sufficiently differentiable) path $(x_1(s),y_1(s))^T$ for the last trailer axle. From this path and its derivatives, all the other paths $(x_k(s),y_k(s))^T$ can be computed explicitly. The angle between the link $3-4$ and the link $4-5$ is the required steering angle of the head car. Note also that the four-wheeled head car is equivalent to two two-wheeled trailers.

The equations are elementary, but naively applying them quickly leads to untractable expressions with growing numbers of trailers. 

### Recursive equations
The kinematics of the system implies the following equation
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
\end{pmatrix}.
$$

Using $q_k(s):=(x_k(s), y_k(s))^T$ and applying the above equation $n-1$ times, we get a map
$$
\varphi: \quad \left(q_1(s), q_1^{(1)}(s), \ldots, q_1^{(n-1)}(s)\right) \ \longmapsto \ \big(q_1(s), ..., q_n(s)\big)
$$

which allows to compute all trailer positions from the derivatives of the desired trajectory of $q_1(s)$.

However, doing so more than a few times (even using computer algebra) quickly leads to very large expressions and computation time. This is mainly due to the repeated derivatives of the square root term.

### Using angles

The first trick is to use additional angle variables by rewriting the recursive equation as follows
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
L_k
\begin{pmatrix}
\cos{\alpha_k} \\
\sin{\alpha_k}
\end{pmatrix}
\qquad
\textnormal{with}
\qquad
\alpha(s) = \arctan_2(x_{k}'(s),y_{k}'(s)).
$$

This is useful because from the first derivative of the arc-tangent we get
$$
\frac d {ds} \arctan_2(x_{k}',y_{k}') 
= \frac d {ds} \arctan \frac{y_{k}'}{x_{k}'} 
= \frac{x'_k y''_k - x''_k y'_k}{x'^2_k + y'^2_k}
$$
and this expression is rational in (no square roots). Hence, the multiple derivatives $\alpha^{(r)}(s)$ of $\alpha(s)$ can be computed from the derivatives of $x_{1,2}(s)$ by successively applying product rules and quotient rules. In turn, the derivatives of $\sin(\alpha)$ and $\cos(\alpha)$ are obtained by applying chain rules. These product-, quotient- and chain-rules are higher order variant of the usual ones (more on this below).

### More intermediate variables

The second trick is to decompose the mapping $\varphi$ in sub-steps involving more intermediate variables (the derivatives of all $q_k$, not just $q_1$). Differentiating the original relation $q_{k+1}=f(q_k, q'_k)$ ($n-k-1$ times), gives a map
$$
\phi_k : \qquad \big( q_k(s), q'_k(s), \ldots, q_k^{(n-k)}(s) \big)
\ \longmapsto \ 
\big( q_{k+1}(s), q'_{k+1}(s), \ldots, q_{k+1}^{(n-k-1)}(s) \big).
$$
And
$$
\varphi = \phi_1 \circ \phi_2 \circ \cdots \circ \phi_{n-1} .
$$

### High order product and quotient rules
Computing the derivatives of the angles $\alpha_k$ is easy: first compute the derivatives of the products
$$
x'_k y''_k, \quad  x''_k y'_k, \quad x'^2_k \quad \textnormal{and} \quad y'^2_k
$$
with the product rule and then compute the derivatives of the quotient of 
$$
x'_k y''_k - x''_k y'_k \quad \textnormal{and} \quad x'^2_k + y'^2_k
$$
with the quotient rule. The product rule is given by
$$
\frac{d^r}{ds^r} \big( f(s) \cdot g(s) \big) = \sum_{j=0}^r 
\begin{pmatrix} r \\ j \end{pmatrix}
f^{(r-j)}(s) \cdot g^{(j)}(s).
$$

To get the quotient rule for $f(s)/g(s)$, one first obtains a rule for the reciprocal $\bar g(s) = 1/g(s)$. This rule is obtained from the product rule and the equation $g(s)\cdot\bar g(s) = 1$. The product rule is then applied again on $f(s)\cdot\bar{g(s)}$.

Next define
$$
f^{[k]}(s) := \frac 1 {k!} f^(k)(s)
$$
then
$$
\left(f\cdot g\right)^{[r]}  = \sum_{j=0}^r 
f^{[r-j]}(s) \cdot g^{[j]}(s).
$$

This has two benefits: 1) the product rule uses simple coefficients convolution, 2) since high order derivatives tend to be numerically large, dividing them by $k!$ leads to better "conditioned " computations. Note that the above is the same as computing the coefficients of the product of polynomials with coefficients $f^{[i]}$ and $g^{[j]}$ and truncating the result at degree $r$. The corresponding quotient rule is obtained in the same way as above.


### High order composition rule

To complete the computations of $\phi_k$, we still need a high order composition rule to compute the derivatives of 
$$
\cos{\alpha_k} \quad \textnormal{and} \quad \sin{\alpha_k}
$$

The first attempt was made using [Faa di Bruno's](https://en.wikipedia.org/wiki/Fa%C3%A0_di_Bruno%27s_formula) formula, in particular the form involving [Bell polynomials](https://en.wikipedia.org/wiki/Bell_polynomials#Recurrence_relations) since these can be easily implemented in code via a seemingly efficient recurrence relation. It turns out however that computing these polynomials this way quickly leads to very long computation times. I then stumbled on a [post](https://mathoverflow.net/questions/364036/combinatorics-of-multivariate-fa%C3%A0-di-bruno-formula) noting the "inefficiency" of Faa di Bruno formulae compared to power series approaches. Indeed, it is better to reconsider the problem from the point of view of formal power series. Our goal is to compute the first $n$ derivatives of the composite function $f(g(s))$ (at a given value of $s$)

To this end, let us look at the Taylor expansion of $f(g(s_0))$ around $g(s_0)$.
$$
f(g(s_0)) 
= \sum_k \frac 1 {k!} f^{(k)}\left( g(s_0) \right) \left( g(s) - g(s_0) \right)^k
$$
and then, let us replace $g(s)$ by its Taylor series around $s_0$
$$
f(g(s_0)) 
= \sum_k \frac 1 {k!} f^{(k)}\left( g(s_0) \right) \left(
\left\{ 
\sum_l \frac 1 {l!} g^{(l)}(l_0)\cdot(s-s_0)^l
\right\}
 - g(s_0) \right)^k
$$
Clearly, defining the power series
$$
p_1(x) := \sum_k \frac 1 {k!} f^{(k)}(g(s_0)) \cdot x^k 
$$

$$
p_2(y) := -g(s_0) + y
$$
$$
p_3(z) := \sum_l \frac{1}{l!} g^{(l)}(s_0) \cdot z^l
$$
we have that
$$
f(g(s)) = p_1 \circ p_2 \circ p_3 (s-s_0) = \sum_k \frac 1 {k!} 
\underbrace{\left(\frac{d^k f(g(s))}{ds^k}\right)\Bigg|_{s=s_0}}_{\textnormal{values of interrest}} (s-s_0)^k
$$
Hence, computing the first $n$ coefficients of the power series
$$ p_1 \circ p_2 \circ p_3 (w) $$
we get the first $n$ derivatives of $f(g(s))$. Furthermore, re-expressing everything in terms of $f^{[i]}$ and $g^{[j]}$ we get rid of the factorial terms and end up manipulating polynomials. In turn, the (truncated) composition of polynomials can be implemented using the product rule for building the monomials one by one.

### Animation speed

To produce an animation of a car with many trailers, one chooses a trajectory $q_1(s)$ for the last trailer's axle and then use the map $\varphi$ to compute all the other trailers and car positions. However doing so and using $s=t$ leads to a jerky animation since the head car's speed generally varies wildly (high derivatives) over time. As a remedy, we impose the head car's rear axle speed (which can be computed from the derivatives of $q_1(s(t))$ by integration of the equation

$$
\dot s(t) = \frac 1 {\sqrt{x'^2_{n-1}(s(t)) + y'^2_{n-1}(s(t))}}
$$


### Note

Equations in this README file where typesetted with the help of [readme2tex](https://github.com/leegao/readme2tex)



