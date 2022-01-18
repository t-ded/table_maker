
# Only logically wrong inputs are tested - this leaves the program vulnerable
# to wrong input possibilities that have not been found

# -*- coding: utf8 -*-
from tablemaker import Labs
import pytest
import numpy as np

def test_inputs():
    with pytest.raises(ValueError):
        lab = Labs({}, [1, 2, 3])  # Empty quantities dict
    with pytest.raises(ValueError):
        lab = Labs({"A": "B"}, [[1, 2], [1, 2]])  # More data columns than header columns
    with pytest.raises(ValueError):
        lab = Labs({"A": "B", "C": "D"}, [1, 2])  # Less data columns than header columns
    with pytest.raises(ValueError):
        lab = Labs({"A": "B"}, [1, 2], [-1, 5])  # More rounding digits than columns
    with pytest.raises(ValueError):
        lab = Labs({"A": "B", "C": "D"}, [1, 2], [5])  # Less rounding digits than columns

def test_stat_values():
    lab = Labs({"A": "B", "C": "D", "E": "F", "G": "H", "I": "J"},
               [[1, 1, 1], [1, 2, 3], [0.05, 0.012, 0.08], [155, 64, 28], [0.6, 0.08, 0.12]],
              [None, None, None, None, 3])
    lab.stat_values(lab.data)
    assert lab.means == ["1", "2,0", "0,05", "80", "0,267"]
    assert lab.SEs == ["0", "0,5", "0,02", "30", "0,136"]
    assert lab.rounding_digits == [0, 1, 2, -1, 3]
    
def test_first_nonzero():
    lab = Labs({"A": "B"}, [[]])
    lst = [lab.first_nonzero(x) for x in [0.0, 6, 12, 146, 19023, -0.052, 0.28, 0.000197, 0.8392, 0.00720]]
    assert lst == [0, 0, -1, -2, -4, 2, 1, 4, 1, 3] 
