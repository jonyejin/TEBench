# TEBench
Quantify the robustness of ML-based traffic engineering algorithms in environments where demand distributions keep changing over time.

## Definition of Robustness
- 1. [Maximum Concurrent Flow(MCF)](https://dl.acm.org/doi/pdf/10.1145/77600.77620)
$$
\begin{align*}
\text{Maximize}\ &\lambda \\
\text{subject to} \\
&0 \leq f(u, v) \leq c(u, v) &&\forall (u, v) \in E, \\
&\sum_{u \in V} f(u, v) = 0 &&\forall v \in V \setminus \{ \text{sources, sinks} \}, \\
&\sum_{(s, v) \in E} f(s, v) \geq \lambda, \\
&\sum_{(v, t) \in E} f(v, t) \geq \lambda.
\end{align*}

$$

* $\lambda$: Represents the objective value to be maximized, indicating the maximum concurrent flow rate in the network.
* $f(u, v)$ : Represents the flow from node $u$ to $v$.
* $c(u, v)$: Represents the maximum allowable flow (capacity) from node $u$ to $v$.
* $E$: Represents the set of all edges in the network.
* $V$ : Represents the set of all nodes in the network.
* $\text{sources, sinks}$: Represent the sources (starting points) and sinks (destinations) in the network.



- 2.  Normalized Change
$$
\text{Normalized Change} = \frac{\| T(t + \Delta t) - T(t) \|_2}{\| T(t) \|_2}
$$

* $T(t)$: Represents the traffic matrix at time $t$.
* $T(t + \Delta t)$: Represents the traffic matrix at a later time $t + \Delta t$.
* $\Delta t$: The time interval between the two observations of the traffic matrix.
* $\|\cdot\|_2$: Denotes the $L2$ norm, which measures the magnitude of a vector. In this context, it quantifies the change in the traffic matrix.


### Our Definition of Robustness 
$$
\text{Robustness} = \frac{1}{N} \sum_{i=1}^{N} \lambda_i (1 - \beta \cdot NC_i)
$$


  * $N$: Represents the total number of data sets or scenarios considered.
    * *$\lambda_i$: Represents the Maximum Concurrent Flow (MCF) rate for the $i$-th data set or scenario.
    * *$\beta$: A weighting factor that modulates the impact of the Normalized Change on the overall metric.
    * $NC_i$: The Normalized Change for the $i$-th data set, indicating the change in the traffic matrix at the specific time step relative to its initial state.
    * $\textbf{Robustness}$: A measure that integrates both the efficiency of flow across the network (via $\lambda_i$) and the stability of this flow over time (accounting for changes via $NC_i$).