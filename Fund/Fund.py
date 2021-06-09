import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

from datetime import date, timedelta
from FundVisualizer import FundVisualizer

class Fund:
    def __init__(self, fund_id, start_date, end_date=str(date.today()), fetch_data=False):
        self.fund_id = fund_id
        self.start_date = start_date
        self.end_date = end_date
        if fetch_data:
            self.update_data()
    
    def update_data(self, session=None):
        self.data = self.get_fund(self.fund_id, start_date=self.start_date, end_date=self.end_date, session=session)

    @staticmethod
    def get_fund(code, start_date, end_date, page=1, per=40, session=None):
        def get_html(code, start_date, end_date, page=1, per=per, session=session):
            url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page={1}&sdate={2}&edate={3}&per={4}'.format(
                code, page, start_date, end_date, per)
            # print(url)
            rsp = requests.get(url) if session is None else session.get(url)
            html = rsp.text
            return html
        first_page_html = get_html(code, start_date, end_date, page, per)
        soup = BeautifulSoup(first_page_html, 'html.parser')
        pattern = re.compile('pages:(.*),')
        result = re.search(pattern, first_page_html).group(1)
        total_page = int(result)
    
    
        records = []
        current_page = 1
        while current_page <= total_page:
            html = get_html(code, start_date, end_date, current_page, per)
            soup = BeautifulSoup(html, 'html.parser')
            if current_page == 1:
                heads = []
                for head in soup.findAll("th"):
                    heads.append(head.contents[0])
            for row in soup.findAll("tbody")[0].findAll("tr"):
                row_records = []
                for record in row.findAll('td'):
                    val = record.contents
                    if val == []:
                        row_records.append(np.nan)
                    else:
                        row_records.append(val[0])
                records.append(row_records)
            current_page = current_page + 1

        np_records = np.array(records)
        fund_df = pd.DataFrame()
        for col, col_name in enumerate(heads):
            fund_df[col_name] = np_records[:, col]
    
    
        fund_df['净值日期'] = pd.to_datetime(fund_df['净值日期'], format='%Y/%m/%d')
        fund_df = fund_df.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
        fund_df = fund_df.set_index('净值日期')
    
        fund_df['单位净值'] = fund_df['单位净值'].astype(float)
        fund_df['累计净值'] = fund_df['累计净值'].astype(float)
        fund_df['日增长率'] = fund_df['日增长率'].str.strip('%').astype(float)
        return fund_df

if __name__ == '__main__':
    fund_id = '050026'
    # start_date ='2020-02-01'
    start_date = str(date.today() - timedelta(days=120))
    # end_date ='2020-06-01'
    fund = Fund(fund_id, start_date)

    viz = FundVisualizer()
    viz.plot(fund=fund)

    # print(fund_df)
    