from qdp_python import *


'''
=====================================================
option contract details:
 
option type: Double One Touch

start date = 2018/1/3
maturity date = 2019/1/3
barrier : 80%
high_barrier: 120%
knock out as coupon , 10% annualized by Act365() convention
knock out observation : monthly

other variables:

spot = 100
valuation date = start date
volatility = 30%
risk free rate = 3%
dividend yield = 1%
=================================================================

Pricing result comparison details:
quad pv = 3.74560560260911
mc pv = 3.741268379019219
relative error = (quad pv / mc pv - 1) * 100 = 0.12%

'''


calendar = China()
day_counter = Bus244()
start_date = Date(2018, 1, 3)
maturity_date = Date(2019, 1, 3)
spot = 100

barrier_type = BarrierType.DoubleOneTouch

# construct knock out coupon
coupon_rate = InterestRate(0.1)

coupon = Coupon(start_date, spot, coupon_rate)

observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3),
                     Date(2018, 6, 4), Date(2018, 7, 3), Date(2018, 8, 3), Date(2018, 9, 3),
                     Date(2018, 10, 8), Date(2018, 11, 5), Date(2018, 12, 3), Date(2019, 1, 3)]

barrier = Barrier(observation_dates, 80, barrier_type, 120)

hit_payoff = CashOrNothingPayoff(PayoffType.Call, 120, coupon) + CashOrNothingPayoff(PayoffType.Put, 80, coupon)

unhit_payoff = CashOrNothingPayoff(PayoffType.Call, 80, 0)

option = BarrierOption(spot,
                       start_date,
                       maturity_date,
                       barrier,
                       hit_payoff,
                       unhit_payoff)

risk_free_rate = 0.03
dividend_yield = 0.01
volatility = 0.3

process = BlackScholesProcess(start_date, spot, risk_free_rate, dividend_yield, volatility, day_counter)

engine = MonteCarloEngine(process, 1000000)

npv = option.pv(engine)
print(npv)


