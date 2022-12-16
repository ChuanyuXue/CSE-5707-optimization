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

/**
 * Absolute value constraint
 */
public class Absolute extends AbstractConstraint {

    private final IntVar x;
    private final IntVar y;

    /**
     * Creates the absolute value constraint {@code y = |x|}.
     *
     * @param x the input variable such that its absolut value is equal to y
     * @param y the variable that represents the absolute value of x
     */
    public Absolute(IntVar x, IntVar y) {
        super(x.getSolver());
        this.x = x;
        this.y = y;
    }

    public void post() {
        y.removeBelow(0);
        int[] vary = new int[y.size()];
        y.fillArray(vary);
        for (int v : vary) {
            if (!x.contains(v)) {
                if (!x.contains(-v)) {
                    y.remove(v);
                }
            }
        }

        int[] varx = new int[x.size()];
        x.fillArray(varx);
        for (int v : varx) {
            if (v < 0) {
                if (!y.contains(-v))
                    x.remove(v);
            } else {
                if (!y.contains(v))
                    x.remove(v);
            }
        }
        x.propagateOnDomainChange(this);
        y.propagateOnDomainChange(this);
    }

    @Override
    public void propagate() {
        int[] vary = new int[y.size()];
        y.fillArray(vary);
        for (int v : vary) {
            if (!x.contains(v)) {
                if (!x.contains(-v)) {
                    y.remove(v);
                }
            }
        }

        int[] varx = new int[x.size()];
        x.fillArray(varx);
        for (int v : varx) {
            if (v < 0) {
                if (!y.contains(-v))
                    x.remove(v);
            } else {
                if (!y.contains(v))
                    x.remove(v);
            }
        }
    }

}
