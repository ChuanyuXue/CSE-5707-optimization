/*
 * mini-cp is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License  v3
 * as published by the Free Software Foundation.
 *
 * mini-cp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY.
 * See the GNU Lesser General Public License  for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with mini-cp. If not, see http://www.gnu.org/licenses/lgpl-3.0.en.html
 *
 * Copyright (c)  2018. by Laurent Michel, Pierre Schaus, Pascal Van Hentenryck
 */

package minicp.engine.constraints;

import minicp.engine.core.AbstractConstraint;
import minicp.engine.core.IntVar;
import minicp.util.GraphUtil;
import minicp.util.GraphUtil.Graph;
import minicp.util.exception.InconsistencyException;
import minicp.util.exception.NotImplementedException;
import tinycsp.Domain;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * Arc Consistent AllDifferent Constraint
 *
 * Algorithm described in
 * "A filtering algorithm for constraints of difference in CSPs" J-C. Régin,
 * AAAI-94
 */
public class AllDifferentDC extends AbstractConstraint {

    private IntVar[] x;

    private final MaximumMatching maximumMatching;

    private final int nVar;
    private int nVal;

    // residual graph
    private ArrayList<Integer>[] in;
    private ArrayList<Integer>[] out;
    private int nNodes;
    private Graph g = new Graph() {
        @Override
        public int n() {
            return nNodes;
        }

        @Override
        public Iterable<Integer> in(int idx) {
            return in[idx];
        }

        @Override
        public Iterable<Integer> out(int idx) {
            return out[idx];
        }
    };

    private int[] match;
    private boolean[] matched;

    private int minVal;
    private int maxVal;

    public AllDifferentDC(IntVar... x) {
        super(x[0].getSolver());
        this.x = x;
        maximumMatching = new MaximumMatching(x);
        match = new int[x.length];
        this.nVar = x.length;
    }

    @Override
    public void post() {
        for (int i = 0; i < nVar; i++) {
            x[i].propagateOnDomainChange(this);
        }
        updateRange();

        matched = new boolean[nVal];
        nNodes = nVar + nVal + 1;
        in = new ArrayList[nNodes];
        out = new ArrayList[nNodes];
        for (int i = 0; i < nNodes; i++) {
            in[i] = new ArrayList<>();
            out[i] = new ArrayList<>();
        }
        propagate();
    }

    private void updateRange() {
        minVal = Integer.MAX_VALUE;
        maxVal = Integer.MIN_VALUE;
        for (int i = 0; i < nVar; i++) {
            minVal = Math.min(minVal, x[i].min());
            maxVal = Math.max(maxVal, x[i].max());
        }
        nVal = maxVal - minVal + 1;
    }

    private int getNodeId(int value) {
        return value + x.length - minVal;
    }

    private void updateGraph() {
        nNodes = nVar + nVal + 1;
        int sink = nNodes - 1;
        for (int j = 0; j < nNodes; j++) {
            in[j].clear();
            out[j].clear();
        }
        for (int i = 0; i < nVal; i++) {
            matched[i] = false;
        }
        for (int i = 0; i < x.length; i++) {
            in[i].add(getNodeId(match[i]));
            out[getNodeId(match[i])].add(i);
            matched[match[i] - minVal] = true;
        }
        for (int i = 0; i < nVar; i++) {
            for (int v = x[i].min(); v <= x[i].max(); v++) {
                if (x[i].contains(v) && match[i] != v) {
                    in[getNodeId(v)].add(i);
                    out[i].add(getNodeId(v));
                }
            }
        }
        for (int v = minVal; v <= maxVal; v++) {
            if (!matched[v - minVal]) {
                in[sink].add(getNodeId(v));
                out[getNodeId(v)].add(sink);
            } else {
                in[getNodeId(v)].add(sink);
                out[sink].add(getNodeId(v));
            }
        }
    }

    @Override
    public void propagate() {
        int size = maximumMatching.compute(match);
        if (size < x.length) {
            throw new InconsistencyException();
        }
        updateRange();
        updateGraph();
        int[] scc = GraphUtil.stronglyConnectedComponents(g);
        for (int i = 0; i < nVar; i++) {
            for (int v = minVal; v <= maxVal; v++) {
                if (match[i] != v && scc[i] != scc[getNodeId(v)]) {
                    x[i].remove(v);
                }
            }
        }
    }
}
