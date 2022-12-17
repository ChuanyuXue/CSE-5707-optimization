package minicp.examples;

import minicp.cp.Factory;
import minicp.engine.constraints.Element1D;
import minicp.engine.constraints.Element1DVar;
import minicp.engine.constraints.Element2D;
import minicp.engine.constraints.Equal;
import minicp.engine.core.IntVar;
import minicp.engine.core.Solver;
import minicp.search.DFSearch;
import minicp.search.SearchStatistics;

import java.util.Arrays;

import static minicp.cp.BranchingScheme.firstFail;
import static minicp.cp.Factory.*;

public class QuasigroupCompletion {
    public static void main(String[] args) {
        int m = 5;
        Solver cp = Factory.makeSolver();
        IntVar[][] mat = new IntVar[m][m];
        IntVar[][] matT = new IntVar[m][m];
        IntVar[] matFlat = new IntVar[m * m];

        // Initialize mat and matT
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                mat[i][j] = makeIntVar(cp, 0, m - 1);
                matT[i][j] = makeIntVar(cp, 0, m - 1);
            }
        }

        // Initialize matFlat
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                matFlat[i * m + j] = mat[i][j];
            }
        }

        // Link mat and matT
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                cp.post(
                        equal(
                                mat[i][j],
                                matT[j][i]));
            }
        }

        // Add all different constraints to columns and rows
        for (int i = 0; i < m; i++) {
            cp.post(allDifferent(mat[i]));
            cp.post(allDifferent(matT[i]));
        }

        // Add quasigroup constraints
        for (int a = 0; a < m; a++) {
            for (int b = 0; b < m; b++) {
                IntVar bA = mat[b][a];
                IntVar aBT = matT[a][b];
                IntVar temp = makeIntVar(cp, 0, m - 1);
                cp.post(new Element1DVar(matT[b], aBT, temp));
                cp.post(new Element1DVar(mat[a], bA, temp));
            }
        }

        DFSearch dfs = makeDfs(cp, firstFail(matFlat));
        dfs.onSolution(() -> {
            System.out.println(Arrays.deepToString(mat));
        });

        SearchStatistics stats = dfs.solve();
        System.out.println(stats);
    }
}
