from DataManager import DataManager as d
import pandas as pd
import pytest
from pathlib import Path

def test_load_data_from_csv():
    csv_file = "dm_test.csv"

    df = d.load_data_from_csv(csv_file)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["종목명", "logic"]
    assert len(df) == 5
    assert df.loc[0, "종목명"] == "삼성전자"
    assert df.loc[2, "logic"] == "delta"



def test_save_data_to_csv():
    data = [1,2,3,4,5]
    df = pd.DataFrame(data, columns=['val'])

    d.save_data_to_csv('val.csv', df)

    file_check = Path("./datas/val.csv")  # 프로젝트 내의 특정 파일
    assert file_check.is_file(), f"파일 '{file_check}'이(가) 존재하지 않습니다."


@pytest.mark.parametrize("name, expected", [('삼성전자', '005930'),('하나금융지주','086790')])
def test_name_to_code(name, expected):

    code = d.name_to_code(name)
    assert code == expected


def test_add_code():
    data = ['삼성바이오로직스','HD현대중공업','한화에어로스페이스']
    df = pd.DataFrame(data, columns=['종목명'])

    r_df = d.add_code(df)

    assert isinstance(r_df, pd.DataFrame)
    assert list(df.columns) == ["종목명", "Code"]
    assert len(df) == 3
    assert df.loc[0, "Code"] == "207940"
    assert df.loc[1, "Code"] == "329180"
    assert df.loc[2, "Code"] == "012450"


@pytest.mark.parametrize("code, expected", [('000270', 100700),('105560',82900)])
def test_load_stock_data(code, expected):
    df = d.load_stock_data(code, end='2024-12-31')

    assert df['Close'][-1] == expected

