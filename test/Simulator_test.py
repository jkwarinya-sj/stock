import sys
import os

curr_path = os.getcwd()
root_path = os.path.dirname(curr_path)
sys.path.append(root_path)

import pytest
from Simulator import Simulator 

def test_decide_invest():
    s = Simulator('test_simulator.csv', '../datas')
    status_list = s.decide_invest(end='2024-12-31')

    expected_list = ['dca_skip','-','-','-','buy', '-', '-', '-', '-', '-', '-', '-']
    idx = 0

    for s in status_list:
        assert s == expected_list[idx]
        idx = idx+1



def test_update_logic():
    s = Simulator('test_simulator.csv', '../datas')
    ret_list = s.update_logic(end='2024-12-31')

    assert ret_list[0] == 'dca'
    assert ret_list[1] == 'alpha'
    assert ret_list[2] == 'gamma'
    assert ret_list[3] == 'delta'
    assert ret_list[4] == 'epsilon'
    assert ret_list[5] == 'zeta'
    assert ret_list[6] == 'eta'
    assert ret_list[7] == 'theta'
    assert ret_list[8] == 'iota'
    assert ret_list[9] == 'kapa'
    assert ret_list[10] == 'lamda'
    assert ret_list[11] == 'mu'


