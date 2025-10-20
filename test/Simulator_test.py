"""
from Simulator import Simulator 


if __name__ == '__main__':
    obj = Simulator('final_data_1013.csv')
    obj.decide_invest()
    #obj.run()
    #obj.check_current_profit()
    #obj.update_logic()
    #obj.make_portfolio()
    #obj.test()
"""

import pytest

from Simulator import Simulator 

def test_decide_invest():
    s = Simulator('test_simulator.csv', '../datas')
    status_list = s.decide_invest(end='2024-12-31')

    expected_list = ['buy','-','dca_skip','buy','sell']
    idx = 0

    for s in status_list:
        assert s == expected_list[idx]
        idx = idx+1



def test_update_logic():
    s = Simulator('test_simulator.csv', '../datas')
    ret_list = s.update_logic(end='2024-12-31')

    assert ret_list[0] == 'alpha'
    assert ret_list[1] == 'delta'
    assert ret_list[2] == 'delta'
    assert ret_list[3] == 'epsilon'
    assert ret_list[4] == 'alpha'


