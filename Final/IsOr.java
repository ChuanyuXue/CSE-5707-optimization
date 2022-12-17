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
import minicp.engine.core.BoolVar;
import minicp.state.StateInt;
import minicp.util.exception.NotImplementedException;

/**
 * Reified logical or constraint
 */
public class IsOr extends AbstractConstraint { // b <=> x1 or x2 or ... xn

    private final BoolVar b;
    private final BoolVar[] x;
    private final int n;

    private int[] freeVarIndex;
    private StateInt nFreeVars;

    private final Or or;

    /**
     * Creates a constraint such that
     * the boolean b is true if and only if
     * at least variable in x is true.
     *
     * @param b the boolean that is true if at least one variable in x is true
     * @param x an non empty array of variables
     */
    public IsOr(BoolVar b, BoolVar[] x) {
        super(b.getSolver());
        this.b = b;
        this.x = x;
        this.n = x.length;
        or = new Or(x);

        nFreeVars = getSolver().getStateManager().makeStateInt(n);
        freeVarIndex = new int[n];
        for (int i = 0; i < n; i++) {
            freeVarIndex[i] = i;
        }
    }

    @Override
    public void post() {
        b.propagateOnFix(this);
        for (BoolVar xi : x) {
            xi.propagateOnFix(this);
        }
    }

    @Override
    public void propagate() {
        // Implement the constraint as efficiently as possible and make sure you pass
        // all the tests
        if (b.isTrue()) { // If b is true, post Or constraint.
            getSolver().post(new Or(x));
            this.setActive(false);
        } else if (b.isFalse()) { // If b is false, set all unBound BoolVars to false.
            int nU = nFreeVars.value();
            for (int i = 0; i < nU; i++) {
                x[freeVarIndex[i]].fix(false);
            }
            this.setActive(false);
        } else {
            int nU = nFreeVars.value();
            for (int i = 0; i < nU; i++) { // Iterate over unbound variables.
                int idx = freeVarIndex[i];
                if (x[idx].isTrue()) { // If at least one variable is true, fix b to true.
                    b.fix(true);
                    this.setActive(false);
                    return;
                } else if (x[idx].isFalse()) { // If the variable is false, remove from freeVarIndex.
                    freeVarIndex[i] = freeVarIndex[nU - 1];
                    freeVarIndex[nU - 1] = idx;
                    nU--;
                }
            }
            nFreeVars.setValue(nU); // Update number of unbound vars

            // If no unbound vars, then all are false, hence b is false too.
            if (nU == 0) {
                b.fix(false);
                this.setActive(false);
            }
        }
    }
}
