# TEBench
Quantify the robustness of ML-based traffic engineering algorithms in environments where demand distributions keep changing over time.
###  Original Utilities provided by TEBench
1. **Perturbated Matrices Generation**: Generate perturbated traffic matrices with varying levels of sparsity and demand changes.
    - Usage: ```python benchmark/add_perturbation.py```
2. **LP-based Traffic Solver Data Generation**:
   - Usage: ```python utilities/calcuate_optimal_values.py {hist_file_name}.hist {train|test} --ecmp_topo Abilene --opt_function {MAXUTIL | MAXFLOW | MAXCONC}```
3. **Robustness Calculation**: Calculate the robustness of a given algorithm using the generated data.   


### Datasets provided by TEBench
1. **Original Data**: The original data for the Abilene, ASN2k, B4, Kdl, and GEANT topologies.

| Network Name | Node Count | Edge Count |
|--------------|------------|------------|
| Abilene      | 12         | 15         |
| ASN2k        | 22         | 37         |
| B4           | 19         | 27         |
| Kdl          | 14         | 21         |
| GEANT        | 22         | 37         |

2. **Pertrubated Data**: The perturbated data for the Abilene, ASN2k, B4, Kdl, and GEANT topologies.

3. **Trained Model Weights for DOTE and TEAL**: The trained model weights for the DOTE and TEAL algorithms.

### Helper Functions provided by TEBench
1. DOTE to TEAL 
2. TEAL to DOTE


## Disclaimer for Copyrights
The works contained within the DOTE and TEAL folders are the property of the author of the paper. These materials are typically the intellectual products resulting from research and are owned by the researcher or writer who created them. This ownership implies that the author holds the copyright to the content in these folders, which may include data, written content, code, and other forms of intellectual property. This designation ensures that the author retains control over how these materials are used, distributed, or modified. 



## Definition of Robustness
- 1. [Maximum Concurrent Flow(MCF)](https://dl.acm.org/doi/pdf/10.1145/77600.77620)

Maximize $λ$ 
subject to:
0 $\leq$ $f(u, v)$ $\leq$ $c(u, v)$ for all $(u, v) \in E$,
$\sum f(u, v) = 0$ for all $v \in V \setminus {\text{sources, sinks}}$,
$\sum f(s, v) \geq \lambda$ for all $(s, v) \in E$,
$\sum f(v, t) \geq \lambda$ for all $(v, t) \in E$.

* $\lambda$: Represents the objective value to be maximized, indicating the maximum concurrent flow rate in the network.
* $f(u, v)$ : Represents the flow from node $u$ to $v$.
* $c(u, v)$: Represents the maximum allowable flow (capacity) from node $u$ to $v$.
* $E$: Represents the set of all edges in the network.
* $V$ : Represents the set of all nodes in the network.
* $\text{sources, sinks}$: Represent the sources (starting points) and sinks (destinations) in the network.


2.  Normalized Changes

$\text{Normalized Change} = \frac{\| T(t + \Delta t) - T(t) \|_2}{\| T(t) \|_2}$

* $T(t)$: Represents the traffic matrix at time $t$.
* $T(t + \Delta t)$: Represents the traffic matrix at a later time $t + \Delta t$.
* $\Delta t$: The time interval between the two observations of the traffic matrix.
* $\|\cdot\|_2$: Denotes the $L2$ norm, which measures the magnitude of a vector. In this context, it quantifies the change in the traffic matrix.


### Our Definition of Robustness 
$$
\text{Robustness} = \frac{1}{N} \sum_{i=1}^{N} \lambda_i (1 - \beta \cdot NC_i)
$$


  * $N$: Represents the total number of data sets or scenarios considered.
  * $\lambda_i$: Represents the Maximum Concurrent Flow (MCF) rate for the $i$-th data set or scenario.
* $\beta$: A weighting factor that modulates the impact of the Normalized Change on the overall metric.
* $NC_i$: The Normalized Change for the $i$-th data set, indicating the change in the traffic matrix at the specific time step relative to its initial state.
* $\textbf{Robustness}$: A measure that integrates both the efficiency of flow across the network (via $\lambda_i$) and the stability of this flow over time (accounting for changes via $NC_i$).
