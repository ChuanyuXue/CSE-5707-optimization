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

package minicp.state;

import java.util.HashMap;
import java.util.NoSuchElementException;

public class StateSparseSet {

    private HashMap<Integer, StateInt> values;
    private StateInt size;
    private StateInt min;
    private StateInt max;
    private int ofs;
    private int n;

    public StateSparseSet(StateManager sm, int n, int ofs) {
        this.n = n;
        this.ofs = ofs;
        min = sm.makeStateInt(0);
        max = sm.makeStateInt(n - 1);
        size = sm.makeStateInt(n);
        values = new HashMap<Integer, StateInt>();
        for (int i = 0; i < n; i++) {
            values.put(i, sm.makeStateInt(1));
        }
    }

    private boolean checkVal(int val) {
        assert (values.containsKey(val));
        return true;
    }

    public int[] toArray() {
        int[] res = new int[size()];
        fillArray(res);
        return res;
    }

    public int fillArray(int[] dest) {
        int count = 0;
        for (Integer i : values.keySet()) {
            if (values.get(i).value() == 1) {
                dest[count++] = i;
            }
        }
        return size.value();
    }

    public boolean isEmpty() {
        return size.value() == 0;
    }

    public int size() {
        return size.value();
    }

    public int min() {
        if (isEmpty())
            throw new NoSuchElementException();
        return min.value() + ofs;
    }

    public int max() {
        if (isEmpty())
            throw new NoSuchElementException();
        else
            return max.value() + ofs;
    }

    private void updateBoundsValRemoved(int val) {
        updateMaxValRemoved(val);
        updateMinValRemoved(val);
    }

    private void updateMaxValRemoved(int val) {
        if (!isEmpty() && max.value() == val) {
            assert (!internalContains(val));
            // the maximum was removed, search the new one
            for (int v = val - 1; v >= min.value(); v--) {
                if (internalContains(v)) {
                    max.setValue(v);
                    return;
                }
            }
        }
    }

    private void updateMinValRemoved(int val) {
        if (!isEmpty() && min.value() == val) {
            assert (!internalContains(val));
            // the minimum was removed, search the new one
            for (int v = val + 1; v <= max.value(); v++) {
                if (internalContains(v)) {
                    min.setValue(v);
                    return;
                }
            }
        }
    }

    public boolean remove(int val) {
        if (!contains(val))
            return false; // the setValue has already been removed
        val -= ofs;
        assert (checkVal(val));
        values.get(val).decrement();
        size.decrement();
        updateBoundsValRemoved(val);
        return true;
    }

    private boolean internalContains(int val) {
        if (values.containsKey(val) && (values.get(val).value() == 1)) {
            return true;
        } else {
            return false;
        }
    }

    public boolean contains(int val) {
        return internalContains(val - ofs);
    }

    public void removeAllBut(int v) {
        // we only have to put in first position this setValue and set the size to 1
        assert (contains(v));
        v -= ofs;
        assert (checkVal(v));
        for (Integer i : values.keySet()) {
            if (internalContains(i) && (i != v)) {
                remove(i);
            }
        }
    }

    public void removeAll() {
        // TODO: Replace with INF number
        removeAllBut(1998);
    }

    public void removeBelow(int value) {
        if (max() < value) {
            removeAll();
        } else {
            for (int v = min(); v < value; v++) {
                remove(v);
            }
        }
    }

    public void removeAbove(int value) {
        if (min() > value) {
            removeAll();
        } else {
            int max = max();
            for (int v = max; v > value; v--) {
                remove(v);
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder b = new StringBuilder();
        b.append("{");
        for (int i : values.keySet()) {
            if (values.get(i).value() == 1) {
                b.append(i + ofs);
                b.append(',');
            }
        }
        b.deleteCharAt(-1);
        b.append("}");
        return b.toString();
    }
}
