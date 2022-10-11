Knapsack! Assigment - CSE5707 - Fall 2022
Chuanyu Xue and Samson Weiner
--------------------------------------
-- How to run code --
We implemented four solvers: a dynamic programming solution, a greedy solution, a hill-climbing solution, and a genetic algorithm solution.

Dynamic programming:
python3 dp-numpy.py -i path-to-dataset

Greedy:
python3 greedy.py -i path-to-dataset

Hill climbing:
python3 hillclimb.py -i path-to-dataset
optional parameters: 
    -n number of neighbors (default 10)
    -m max number of iterations (default 100)

Genetic algorithm:
python3 GA.py -i path-to-dataset
optional parameters:
    -p start probability for random initialization 
    -g initialize with greedy variants
    -m mutation rate
    -t mutation type
    -s population size
    -n number of generations
--------------------------------------
-- Results summary --
We applied our methods to a variety of datasets of different scales. Specifically, we used 10 low dimension datasets and 10 large scale datasets with known optimal values. Additionally, we generated our own very large dataset of 100,000 items.

The DP algorithm computes the solution deterministically, so always achieves the optimal solution. We found the runtime beings to significantly slow down as the number of items reach the 1000s.
For the large dataset we created, our initial python implementation crashed due to memory overflow. With a C implementation, however, we were still able to achieve results fairly quickly.

The greedy algorithm, as expected, always achieves a near perfect solution, but with the fastest runtime.

The hill climbing approach we implemented is very rudimentary, mainly for testing purposes. As such, it achieved very mediocre results.

For the genetic algorithm, we tested numerous design choices at different steps in the algorithm. This included different types of mutations and selection criteria.
We found the results to greatly depend on the initial starting point.
Additionally, we implemented a seeding state based on the greedy solution. For larger datasets, our tests showed this approach never actually exceeded the greedy solution value. We suspect this is because the local search space around the greedy is to expansive.
However, for smaller datasets (when the search space is small), this combined approach did actually improve the greedy algorithm.


The external datasets can be downloaded at this link: 
http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/


## optLow-dimensional 0/1 knapsack problems

Low dimension datasets courtesy of the University of Cauco.

| file               | Optimum  | brute_force | DP   | Greedy | GA   | Climb |
| ------------------ | -------- | ----------- | ---- | ------ | ---- | ----- |
| f1_l-d_kp_10_269   | 295      | 295         | 295  | 294    | 293  | 285   |
| f2_l-d_kp_20_878   | 1024     | 1024        | 1024 | 1081   | 976  | 935   |
| f3_l-d_kp_4_20     | 33       | 33          | 33   | 35     | 35   | 35    |
| f4_l-d_kp_4_11     | 23       | 23          | 23   | 16     | 23   | 23    |
| f5_l-d_kp_15_375   | 481.0694 | N/A         | N/A  | N/A    | N/A  | N/A   |
| f6_l-d_kp_10_60    | 52       | 52          | 52   | 52     | 52   | 46    |
| f7_l-d_kp_7_50     | 107      | 107         | 107  | 102    | 107  | 92    |
| f8_l-d_kp_23_10000 | 9767     | 9767        | 9767 | 9751   | 9734 | 9727  |
| f9_l-d_kp_5_80     | 130      | 130         | 130  | 130    | 130  | 118   |
| f10_l-d_kp_20_879  | 1025     | 1025        | 1025 | 1019   | 984  | 992   |

## Large scale 0/1 knapsack problems

The large scale instances of 0/1 knapsack problem are describe in "Pisinger, D., Where are the hard knapsack problems? Computers & Operations Research, 2005. 32(9): p. 2271-2284"

More large scale 0/1 knapsack problems visit [David Pisinger's optimization codes](http://www.diku.dk/~pisinger/codes.html)

| file                  | Optimum | Greedy | Greedy_time (py) | DP   | DP_time (py) | DP_time (C) | GA    | GA_time | Climb | Climb_time |
| --------------------- | ------- | ------ | ---------------- | ---- | ------------ | ----------- | ----- | ------- | ----- | ---------- |
| knapPI_1_100_1000_1   | 9147    | 8817   | 0.000            | opt  | 0.021        | 0.001       | 7931  | 0.736   | 2738  | 0.002      |
| knapPI_1_200_1000_1   | 11238   | 11227  | 0.001            | opt  | 0.041        | 0.002       | 7660  | 1.243   | 1746  | 0.008      |
| knapPI_1_500_1000_1   | 28857   | 28834  | 0.001            | opt  | 0.329        | 0.006       | 13032 | 2.717   | 7000  | 0.004      |
| knapPI_1_1000_1000_1  | 54503   | 54386  | 0.001            | opt  | 1.433        | 0.047       | 18390 | 5.221   | 8532  | 0.006      |
| knapPI_1_2000_1000_1  | 110625  | 110547 | 0.004            | opt  | 5.923        | 0.123       | 21792 | 9.978   | 20349 | 0.026      |
| knapPI_1_5000_1000_1  | 276457  | 276379 | 0.016            | opt  | 37.996       | 1.429       | 41657 | 24.89   | 45865 | 0.034      |
| knapPI_1_10000_1000_1 | 563647  | 563605 | 0.018            | opt  | 154.860      | 2.264       | 74617 | 48.029  | 90701 | 0.07       |

| file                  | Optimum | Greedy | Greedy_time (py) | DP   | DP_time (py) | DP_time (C) | GA    | GA_time | Climb | Climb_time |
| --------------------- | ------- | ------ | ---------------- | ---- | ------------ | ----------- | ----- | ------- | ----- | ---------- |
| knapPI_2_100_1000_1   | 1514    | 1487   | 0.002            | opt  | 0.021        | 0.001       | 1423  | 0.754   | 873   | 0.002      |
| knapPI_2_200_1000_1   | 1634    | 1604   | 0.000            | opt  | 0.050        | 0.002       | 1277  | 1.191   | 929   | 0.008      |
| knapPI_2_500_1000_1   | 4566    | 4552   | 0.000            | opt  | 0.337        | 0.015       | 2877  | 2.679   | 2545  | 0.004      |
| knapPI_2_1000_1000_1  | 9052    | 9046   | 0.001            | opt  | 1.439        | 0.047       | 5491  | 5.125   | 4995  | 0.006      |
| knapPI_2_2000_1000_1  | 18051   | 18038  | 0.004            | opt  | 5.875        | 0.110       | 10971 | 10.115  | 10135 | 0.009      |
| knapPI_2_5000_1000_1  | 44356   | 44351  | 0.007            | opt  | 37.990       | 1.429       | 25823 | 24.409  | 26149 | 0.032      |
| knapPI_2_10000_1000_1 | 90204   | 90200  | 0.041            | opt  | 157.242      | 2.278       | 51335 | 48.991  | 50651 | 0.06       |

| file                  | Optimum | Greedy | Greedy_time (py) | DP   | DP_time (py) | DP_time (C) | GA    | GA_time | Climb | Climb_time |
| --------------------- | ------- | ------ | ---------------- | ---- | ------------ | ----------- | ----- | ------- | ----- | ---------- |
| knapPI_3_100_1000_1   | 2397    | 2375   | 0.000            | opt  | 0.021        | 0.001       | 1595  | 0.716   | 1023  | 0.002      |
| knapPI_3_200_1000_1   | 2697    | 2649   | 0.001            | opt  | 0.041        | 0.003       | 1776  | 1.203   | 1095  | 0.003      |
| knapPI_3_500_1000_1   | 7117    | 7098   | 0.001            | opt  | 0.331        | 0.016       | 3874  | 2.696   | 2904  | 0.006      |
| knapPI_3_1000_1000_1  | 14390   | 14374  | 0.002            | opt  | 1.418        | 0.047       | 7355  | 5.145   | 5675  | 0.006      |
| knapPI_3_2000_1000_1  | 28919   | 28827  | 0.002            | opt  | 5.868        | 0.105       | 13116 | 9.987   | 10896 | 0.009      |
| knapPI_3_5000_1000_1  | 72505   | 72446  | 0.004            | opt  | 38.697       | 0.587       | 30792 | 24.331  | 39128 | 0.034      |
| knapPI_3_10000_1000_1 | 146919  | 146888 | 0.008            | opt  | 155.175      | 2.266       | 60509 | 48.034  | 55004 | 0.055      |


## Custom large dataset

| Methods on `Customized_100000` | Result | Time                  |
| ------------------------------ | ------ | --------------------- |
| Greedy Py                      | 358964 | 0.147                 |
| DP Py                          | N/A    | Memory Overflow       |
| DP Py (numpy accelerating)     | N/A    | 10000.000 (estimated) |
| DP C                           | 358973 | 23.716                |
| Hill Climb                     | 55672  | 0.403                 |
| GA                             | 62687  | 478.000               |
|                                |        |                       |
