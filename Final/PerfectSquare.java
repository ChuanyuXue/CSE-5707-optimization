package minicp.examples;

import minicp.cp.Factory;
import minicp.engine.constraints.Disjunctive;
import minicp.engine.constraints.Equal;
import minicp.engine.constraints.IsLessOrEqual;
import minicp.engine.constraints.IsLessOrEqualVar;
import minicp.engine.constraints.Or;
import minicp.engine.constraints.IsOr;
import minicp.engine.constraints.LessOrEqual;
import minicp.engine.core.BoolVar;
import minicp.engine.core.IntVar;
import minicp.engine.core.Solver;
import minicp.search.DFSearch;
import minicp.search.SearchStatistics;
import java.util.Arrays;
import java.util.Collection;

import static minicp.cp.BranchingScheme.*;
import static minicp.cp.Factory.*;

public class PerfectSquare {
    public static void main(String[] args) {
        int size = 112;
        int[] tiles = { 50, 42, 37, 35, 33, 29,
                27, 25, 24, 19, 18, 17,
                16, 15, 11, 10, 9, 8, 7,
                6, 4, 2 };

        Solver cp = makeSolver(false);

        IntVar[] flattenXY = new IntVar[tiles.length * 2];

        IntVar[] xPos = makeIntVarArray(cp, tiles.length, size);
        IntVar[] yPos = makeIntVarArray(cp, tiles.length, size);

        for (int i = 0; i < tiles.length; i++) {
            cp.post(lessOrEqual(xPos[i], size - tiles[i]));
            cp.post(lessOrEqual(yPos[i], size - tiles[i]));
        }

        for (int i = 0; i < tiles.length; i++) {
            for (int j = i + 1; j < tiles.length; j++) {
                BoolVar[] boolshitOR = { makeBoolVar(cp), makeBoolVar(cp) };

                BoolVar[] boolshitX = { makeBoolVar(cp), makeBoolVar(cp) };
                cp.post(new IsLessOrEqualVar(boolshitX[0], plus(xPos[i], tiles[i]), xPos[j]));
                cp.post(new IsLessOrEqualVar(boolshitX[1], plus(xPos[j], tiles[j]), xPos[i]));
                cp.post(new IsOr(boolshitOR[0], boolshitX));

                BoolVar[] boolshitY = { makeBoolVar(cp), makeBoolVar(cp) };
                cp.post(new IsLessOrEqualVar(boolshitY[0], plus(yPos[i], tiles[i]), yPos[j]));
                cp.post(new IsLessOrEqualVar(boolshitY[1], plus(yPos[j], tiles[j]), yPos[i]));
                cp.post(new IsOr(boolshitOR[1], boolshitY));

                cp.post(new Or(boolshitOR));
            }
        }

        for (int i = 0; i < tiles.length; i++) {
            flattenXY[i * 2] = xPos[i];
            flattenXY[i * 2 + 1] = yPos[i];
        }

        DFSearch dfs = makeDfs(cp, firstFail(flattenXY));
        dfs.onSolution(() -> {
            System.out.println(Arrays.toString(flattenXY));
        });
        SearchStatistics stats = dfs.solve(stat -> stat.numberOfSolutions() >= 1); // stop on first solution
        System.out.println(stats);

    }
}
