CSE5707 Fall 2022
MiniCP Implementation
Chuanyu Xue


Note:
--------------------------------------------
1. For Problem #1, please rename `StateSparseSetCY` as `StateSparseSet` to do the test. My Hashmap based implementation can pass all testcases, however it failed to RUN for the Problem #234 due to MemoryOverflow Error in a 16Gb Ubuntu machine.
2. For Problem #3 and #4, I added the implementation for `IntVar.fillArray` for convinent. And also for its initialize function with a set of values as parameters (This function is used in the testcases but not implemented).
3. For Problem #4 I am not able to implement but I found a Github Repo: https://github.com/Peiffap/minicp/blob/master/src/main/java/minicp/engine/constraints/AllDifferentDC.java By adding some amendment it works to pass all testcases.


Arichitecture:
--------------------------------------------
/minicp: is the entire minicp project with the implementation that you can build.
/test: only contains the changed file and its test result.



