# Parking Frenzy

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
To get the quotient rule for $f(s)/g(s)$, one first obtain a rule for the reciprocal $\bar g(s) = 1/g(s)$. This rule is obtained from the product rule and the equation $g(s)\cdot\bar g(s) = 1$. The product rule is then applied again on $f(s)\cdot\bar g(s)$.




