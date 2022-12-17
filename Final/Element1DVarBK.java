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
import minicp.util.exception.NotImplementedException;

public class Element1DVar extends AbstractConstraint {

    private final IntVar[] array;
    private final IntVar y;
    private final IntVar z;
    private int maxAvar = Integer.MIN_VALUE + 1;
    private int minAvar = Integer.MAX_VALUE - 1;

    public Element1DVar(IntVar[] array, IntVar y, IntVar z) {
        super(y.getSolver());
        this.array = array;
        this.y = y;
        this.z = z;

    }

    @Override
    public void post() {
        y.removeBelow(0);
        y.removeAbove(array.length - 1);

        int[] yVals = new int[y.size()];
        y.fillArray(yVals);
        for (int i = 0; i < yVals.length; i++) {
            int[] Tvals = new int[array[yVals[i]].size()];
            array[yVals[i]].fillArray(Tvals);
            boolean hasValueInZ = false;
            for (int j = 0; j < Tvals.length; j++) {
                if (z.contains(Tvals[j]))
                    hasValueInZ = true;
            }
            if (!hasValueInZ)
                y.remove(yVals[i]);
        }

        y.fillArray(yVals);
        int[] zVals = new int[z.size()];
        z.fillArray(zVals);
        for (int i = 0; i < zVals.length; i++) {
            boolean existsInT = false;
            for (int j = 0; j < yVals.length; j++) {
                if (array[yVals[j]].contains(zVals[i])) {
                    existsInT = true;
                    break;
                }
            }
            if (!existsInT)
                z.remove(zVals[i]);
        }

        y.fillArray(yVals);
        for (int i = 0; i < yVals.length; i++) {
            if (array[yVals[i]].max() > maxAvar) {
                maxAvar = array[yVals[i]].max();
            }
            if (array[yVals[i]].min() < minAvar) {
                minAvar = array[yVals[i]].min();
            }
        }
        z.removeAbove(maxAvar);
        z.removeBelow(minAvar);

        y.propagateOnDomainChange(this);
        z.propagateOnBoundChange(this);
    }

    @Override
    public void propagate() {
        int[] yVals = new int[y.size()];
        y.fillArray(yVals);
        for (int i = 0; i < yVals.length; i++) {
            if (array[yVals[i]].min() > z.max()) {
                y.remove(yVals[i]);
            } else if (array[yVals[i]].max() < z.min()) {
                y.remove(yVals[i]);
            }
        }

        y.fillArray(yVals);
        int newMinVar = Integer.MAX_VALUE - 1;
        int newMaxVar = Integer.MIN_VALUE + 1;
        for (int i = 0; i < yVals.length; i++) {
            if (array[yVals[i]].max() > newMaxVar) {
                newMaxVar = array[yVals[i]].max();
            }
            if (array[yVals[i]].min() < newMinVar) {
                newMinVar = array[yVals[i]].min();
            }
        }
        if (newMaxVar < maxAvar) {
            z.removeAbove(newMaxVar);
            maxAvar = newMaxVar;
        }
        if (newMinVar > minAvar) {
            z.removeBelow(newMinVar);
            minAvar = newMinVar;
        }
    }
}

