#coding:utf-8

import matplotlib.pyplot as plt
import matplotlib
import platform


def setup_mpl():
    fonts_dict = {
        "Linux": "WenQuanYi Zen Hei",
        "Windows": "SimHei",
    }
    # print(platform.platform())
    for system in ["Linux", "Windows"]:
        if system in platform.platform():
            matplotlib.rcParams['font.sans-serif'] = fonts_dict[system]
            matplotlib.rcParams['font.family'] = fonts_dict[system]
            matplotlib.rcParams['axes.unicode_minus'] = False
            break
        

class FundVisualizer:
    def __init__(self):
        setup_mpl()        
        self.fig, self.axes = plt.subplots(nrows=2, ncols=1)

    def plot(self, fund, keys=['单位净值', '累计净值']):
        fund.data[keys].plot(ax=self.axes[0])
        fund.data['日增长率'].plot(ax=self.axes[1])
        plt.show() 