from DataManager import DataManager as d
import pandas as pd
import pytest
import Logic as l


@pytest.mark.parametrize("code, dca, alpha, gamma, delta, epsilon", [('042660',0.591, 0.15, 0.704, 0.15, 0.356),('035420',-0.046, 0.3, 0.152, 0.534, 0.498),('055550',0.24, 0.218, 0.609, 0.255, 0.255),('009540', 1.156, 0.685, 0.362, 0.526, 0.913),('028260', -0.004, 0.269, 0.464, 0.205, 0.205)])
def test_run_logic(code, dca, alpha, gamma, delta, epsilon):
    df = d.load_stock_data(code, end='2024-12-31')

    ret = l.Logic_dca.run_logic(df)
    assert round(ret,3) == dca

    ret = l.Logic_alpha.run_logic(df)
    assert round(ret,3) == alpha

    ret = l.Logic_gamma.run_logic(df)
    assert round(ret,3) == gamma

    ret = l.Logic_delta.run_logic(df)
    assert round(ret,3) == delta

    ret = l.Logic_epsilon.run_logic(df)
    assert round(ret,3) == epsilon


@pytest.mark.parametrize("code, alpha, gamma, delta, epsilon", [('032830', 'buy', '-', 'buy', 'buy'),('086790', 'buy', 'buy', 'buy', '-'),('015760', 'buy', 'buy', '-', 'buy'),('196170','buy', 'buy', '-', 'buy')])
def test_check_buy(code, alpha, gamma, delta, epsilon):
    df = d.load_stock_data(code, end='2024-12-31')

    ret = l.Logic_alpha._check_buy(df)
    assert ret == alpha

    ret = l.Logic_gamma._check_buy(df)
    assert ret == gamma

    ret = l.Logic_delta._check_buy(df)
    assert ret == delta

    ret = l.Logic_epsilon._check_buy(df)
    assert ret == epsilon


@pytest.mark.parametrize("code, alpha, gamma, delta, epsilon", [('011200','-', '-', '-', '-'),('064350','-', '-', 'sell', 'sell'),('000810', '-', '-', 'sell', 'sell'),('010140', 'sell', '-', 'sell', 'sell')])
def test_check_sell(code, alpha, gamma, delta, epsilon):
    df = d.load_stock_data(code, end='2024-12-31')

    ret = l.Logic_alpha._check_sell(df, df['Close'][-10], 1)
    assert ret == alpha

    ret = l.Logic_gamma._check_sell(df, df['Close'][-10], 1)
    assert ret == gamma

    ret = l.Logic_delta._check_sell(df, df['Close'][-100], 1)
    assert ret == delta

    ret = l.Logic_epsilon._check_sell(df, df['Close'][-100], 1)
    assert ret == epsilon

