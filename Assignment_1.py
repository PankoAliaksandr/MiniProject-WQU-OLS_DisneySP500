# Import libraries
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Class implementation
class Returns_Regression:
    # Constructor
    def __init__(self, stock, index, start_date, end_date, rf_rate):
        self.__stock = stock
        self.__index = index
        self.__start_date = start_date
        self.__end_date = end_date
        self.__rf_rate = rf_rate  # Risk free rate

        self.__stock_data = pd.DataFrame()
        self.__index_data = pd.DataFrame()
        self.__stock_monthly_returns = None
        self.__index_monthly_returns = None
        self.__model = None
        self.__fitted_values = None
        self.__excess_return = None

    def __download_data(self):
        # Stock data
        self.__stock_data = pdr.get_data_yahoo(
                self.__stock, self.__start_date, self.__end_date)
        # Index data
        self.__index_data = pdr.get_data_yahoo(
                self.__index, self.__start_date, self.__end_date)

    def __calculate_returns(self):
        # for period returns. Used to find monthly returns
        def total_return_from_returns(returns):
            return (returns + 1).prod() - 1
        # Stock daily returns
        stock_daily_returns = self.__stock_data['Adj Close'].pct_change()
        # Index monthly retunrs
        self.__stock_monthly_returns = stock_daily_returns.groupby((
                stock_daily_returns.index.year,
                stock_daily_returns.index.month)).apply(
                    total_return_from_returns)

        # Index daily returns
        index_daily_returns = self.__index_data['Adj Close'].pct_change()
        # Index monthly returns
        self.__index_monthly_returns = index_daily_returns.groupby((
                index_daily_returns .index.year,
                index_daily_returns .index.month)).apply(
                    total_return_from_returns)

    def __implement_model(self):
        explanatory_variable = sm.add_constant(
                self.__index_monthly_returns.values)
        model = sm.OLS(self.__stock_monthly_returns.values,
                       explanatory_variable)
        self.__model = model.fit()
        self.__fitted_values = self.__model.fittedvalues

    def __calculate_excess_return(self):
        # Annualized returns
        annualized_return = (self.__stock_monthly_returns + 1).prod() **\
                            (12.0/len(self.__stock_monthly_returns)) - 1
        self.__excess_return = annualized_return - self.__rf_rate

    def __visualize_results(self):
        # Plot the returns on Disney against returns on the S&P 500 index
        plt.plot(self.__stock_monthly_returns.values,
                 label="Disney returns")
        plt.plot(self.__index_monthly_returns.values,
                 label="S&P 500 index returns")
        plt.title("Disney VS S&P500 monthly returns")
        plt.legend()
        plt.show()

        # Model summary
        print self.__model.summary()

        # Plot actual and predicted Disney returns
        plt.plot(self.__stock_monthly_returns.values,
                 label="Disney actual returns")
        plt.plot(self.__fitted_values,
                 label="Disney predicted returns")
        plt.title("Disney Returns")
        plt.legend()
        plt.show()

        print 'Excess return is', self.__excess_return

    def main(self):
        self.__download_data()
        self.__calculate_returns()
        self.__implement_model()
        self.__calculate_excess_return()
        self.__visualize_results()


stock = 'DIS'
index = '^GSPC'
start_date = '2008-10-02'
end_date = '2013-09-30'
rf_rate = 0.003
regression_model = Returns_Regression(stock, index, start_date, end_date,
                                      rf_rate)
regression_model.main()
