package minicp.examples;

import minicp.cp.Factory;
import minicp.engine.constraints.Equal;
import minicp.engine.core.IntVar;
import minicp.engine.core.Solver;
import minicp.search.DFSearch;
import minicp.search.SearchStatistics;

import java.util.Arrays;

import static minicp.cp.BranchingScheme.*;
import static minicp.cp.Factory.*;

public class AllIntervalSeries {
    public static void main(String[] args) {
        int n = 5;
        Solver cp = makeSolver(false);
        IntVar[] s = makeIntVarArray(cp, n, n);
        IntVar[] d = makeIntVarArray(cp, n, n);

        cp.post(allDifferent(s));
        cp.post(allDifferent(d));

        sum(s[0], s[1]);

        for (int i = 0; i < n - 1; i++) {
            cp.post(equal(d[i], abs(sum(s[i + 1], minus(s[i])))));
        }

        DFSearch dfs = makeDfs(cp, firstFail(s));
        dfs.onSolution(() -> {
            System.out.println(Arrays.toString(s));
        });

        SearchStatistics stats = dfs.solve(); // stop on first solution
        System.out.println(stats);
    }
}
