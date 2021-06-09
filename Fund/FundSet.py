from Fund import Fund
from FundVisualizer import FundVisualizer, setup_mpl
import requests
import multiprocessing
from datetime import date, timedelta

class FundUtil:
    def __init__(self, start_date, end_date):
        setup_mpl()
        self.viz = FundVisualizer()
        self.session = requests.Session()
        self.start_date = start_date
        self.end_date = end_date

session = requests.Session()
start_date = None
end_date = None

def init_process():
    global session
    global start_date
    global end_date
    # fund_util = FundUtil(start_date=date.today()-timedelta(days=120), end_date=str(date.today()))
    start_date = start_date=date.today()-timedelta(days=120)
    end_date=str(date.today())

def get_fund(fund_id):
    global session
    global start_date
    global end_date
    fund = Fund(fund_id, start_date, end_date)
    fund.update_data(session=session)
    return fund

def fetch_data(fund_id_list):
    with multiprocessing.Pool(initializer=init_process) as pool:
        fund_sets = pool.map(get_fund,
                             fund_id_list)
    return fund_sets

if __name__ == '__main__':
    fund_id_list = [
        '519002',
        '161818',
        '001069'
    ]
    fetch_data(fund_id_list)
 