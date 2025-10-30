import sys
import os

curr_path = os.getcwd()
root_path = os.path.dirname(curr_path)
sys.path.append(root_path)

from DataManager import DataManager as d

import pandas as pd
import pytest
import Logic as l


@pytest.mark.parametrize("code, dca, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu", [('042660',0.591, 0.15, 0.704, 0.15, 0.356, 1.049, 1.582, 0.47, 1.302, 0.559, 0.564, 0.333),('035420',-0.046, 0.3, 0.152, 0.534, 0.498, -0.32, 0.035, 0.085, -0.279, -0.105, 0.025, 0.255),('055550',0.24, 0.218, 0.609, 0.255, 0.255, 0.391,0.16, 0.303, 0.339, 0.113, 0.622, 0.218),('009540', 1.156, 0.685, 0.362, 0.526, 0.913, 0.353, 0.568, 0.416, 0.344, -0.03, 1.018, 0.925),('028260', -0.004, 0.269, 0.464, 0.205, 0.205, 0.474, 0.32, -0.056, 0.213, 0.251, 0.172, 0.031),('316140',0.314,0.875,-0.038,0.584,0.628,0.339, 0.902, 0.86, 0.364, 0.151, 0.581, 0.855),('033780',0.209,0.097,0.067,0.068,0.068,0.177,0.213, 0.024, 0.212, 0.067, 0.018, 0.068),('086280', 0.425, 1.6, 1.526, 1.461, 1.461, 1.271, 1.163, 0.089, 0.817, 1.098, 1.379, 1.303),('003230', 5.918, 4.939, 4.04, 6.105, 6.287, 0.64, 0.662, 0.913, 2.128, 6.627, 3.426, 4.055),('006800', 0.056, 0.348, 0.58, 0.165, 0.375, 0.426, 0.07, -0.198, 0.194, 0.688, 0.545, 0.4),('006800',0.056, 0.348, 0.58, 0.165, 0.375, 0.426, 0.07, -0.198, 0.194, 0.688, 0.545, 0.4),('272210', 0.473, 0.851, 1.878, 0.675, 1.041, 0.216, 0.185, -0.127, 0.216, 0.456, 1.25, 0.718)])

def test_run_logic(code, dca, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu):
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

    ret = l.Logic_zeta.run_logic(df)
    assert round(ret,3) == zeta

    ret = l.Logic_eta.run_logic(df)
    assert round(ret,3) == eta

    ret = l.Logic_theta.run_logic(df)
    assert round(ret,3) == theta

    ret = l.Logic_iota.run_logic(df)
    assert round(ret,3) == iota

    ret = l.Logic_kapa.run_logic(df)
    assert round(ret,3) == kapa

    ret = l.Logic_lamda.run_logic(df)
    assert round(ret,3) == lamda

    ret = l.Logic_mu.run_logic(df)
    assert round(ret,3) == mu





@pytest.mark.parametrize("code, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu", [('032830', 'buy', '-', 'buy', 'buy','-', '-', '-', '-', '-', '-', '-'),('086790', 'buy', 'buy', 'buy', '-', '-', '-', '-', 'buy', 'buy', '-', '-'),('015760', 'buy', 'buy', '-', 'buy', '-', '-', '-', '-', '-', '-', '-'),('196170','buy', 'buy', '-', 'buy', '-', '-', '-', '-', '-', '-', '-'),('267260','-','-','buy','buy','-','-', '-', '-', '-', '-', '-'),('259960','buy','-','-','-','-','-', '-', '-', '-', '-', '-'),('009150','buy','buy','buy','buy','-','-','-', '-', '-', '-', '-'),('017670','buy','-','buy','buy','-','-','-','-', '-', '-', '-'),('079550','buy','buy','-','buy','-','-','-','-','-', '-', '-'),('267250', '-', '-', 'buy', '-', '-', '-', '-', '-', '-', '-', '-'),('443060', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-')])
def test_check_buy(code, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu):
    df = d.load_stock_data(code, end='2024-12-31')

    
    ret = l.Logic_alpha._check_buy(df)
    assert ret == alpha
    
    ret = l.Logic_gamma._check_buy(df)
    assert ret == gamma

    ret = l.Logic_delta._check_buy(df)
    assert ret == delta

    ret = l.Logic_epsilon._check_buy(df)
    assert ret == epsilon
    
    ret = l.Logic_zeta._check_buy(df)
    assert ret == zeta

    ret = l.Logic_eta._check_buy(df)
    assert ret == eta

    ret = l.Logic_theta._check_buy(df)
    assert ret == theta

    ret = l.Logic_iota._check_buy(df)
    assert ret == iota

    ret = l.Logic_kapa._check_buy(df)
    assert ret == kapa

    ret = l.Logic_lamda._check_buy(df)
    assert ret == lamda

    ret = l.Logic_mu._check_buy(df)
    assert ret == mu



@pytest.mark.parametrize("code, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu", [('011200','-', '-', '-', '-','-','-', '-', '-', '-', '-', '-'),('064350','-', '-', 'sell', 'sell','sell','sell', '-', 'sell','-', 'sell', 'sell'),('000810', '-', '-', 'sell', 'sell','sell','sell', '-', 'sell','-', '-', 'sell'),('010140', 'sell', '-', 'sell', 'sell','sell','sell', '-', 'sell','-', '-', 'sell'),('010130','-','-','sell','sell','sell','sell', '-', 'sell','-', '-', 'sell'),('024110','-','-','sell','sell','sell','sell', '-', 'sell','-', '-', 'sell'),('323410','-','-','-','-','-','-','-','-','-', '-', '-'),('298040','-','-','sell','sell','sell','sell','-','sell','-', 'sell', 'sell'),('079550','-', '-', 'sell', 'sell', 'sell', 'sell', '-', 'sell', '-', 'sell', 'sell'),('005830', '-', '-', 'sell', 'sell', 'sell', 'sell', '-', 'sell', '-', '-', 'sell')])
def test_check_sell(code, alpha, gamma, delta, epsilon, zeta, eta, theta, iota, kapa, lamda, mu):
    df = d.load_stock_data(code, end='2024-12-31')

    #ret = l.Logic_alpha._check_sell(df, df['Close'][-10], 1)
    ret = l.Logic_alpha._check_sell(df, df['Close'].iloc[-10], 1)
    assert ret == alpha

    #ret = l.Logic_gamma._check_sell(df, df['Close'][-10], 1)
    ret = l.Logic_gamma._check_sell(df, df['Close'].iloc[-10], 1)
    assert ret == gamma

    #ret = l.Logic_delta._check_sell(df, df['Close'][-100], 1)
    ret = l.Logic_delta._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == delta

    #ret = l.Logic_epsilon._check_sell(df, df['Close'][-100], 1)
    ret = l.Logic_epsilon._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == epsilon

    ret = l.Logic_zeta._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == zeta

    ret = l.Logic_eta._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == eta

    ret = l.Logic_theta._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == theta

    ret = l.Logic_iota._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == iota

    ret = l.Logic_kapa._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == kapa

    ret = l.Logic_lamda._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == lamda

    ret = l.Logic_mu._check_sell(df, df['Close'].iloc[-100], 1)
    assert ret == mu



