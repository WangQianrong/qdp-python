from time import time

from qdp_python import *

calendar = China()
day_counter = Bus244()
start_date = Date(2021, 2, 25)
maturity_date = Date(2022, 2, 25)
initial_spot = 6554.12

coupon_rate = InterestRate(0.2)

ko_coupon = Coupon(start_date, initial_spot, coupon_rate)
maturity_coupon = Coupon(start_date, initial_spot, coupon_rate)

ko_observation_dates = [Date(2021, 3, 25), Date(2021, 4, 26), Date(2021, 5, 25),
                        Date(2021, 6, 25), Date(2021, 7, 26), Date(2021, 8, 26),
                        Date(2021, 9, 27), Date(2021, 10, 25), Date(2021, 11, 25),
                        Date(2021, 12, 27), Date(2022, 1, 25), Date(2022, 2, 25)]

ko_barrier = Barrier(ko_observation_dates, 6554.12, BarrierType.UpOut)


ko_payoff = CashOrNothingPayoff(PayoffType.Call, ko_barrier, ko_coupon)

ki_observation_dates = []

d = start_date
while d <= maturity_date:
    if calendar.is_business_day(d):
        ki_observation_dates.append(d)
    d = d.next_day()


ki_barrier = Barrier(ki_observation_dates, 5243.29, BarrierType.DownIn)
# we can treat the participation rate as the annualizartion factor
ki_payoff = -VanillaPayoff(PayoffType.Put, 6554.12)

option = Snowball(initial_spot=initial_spot,
                  start_date=start_date,
                  maturity_date=maturity_date,
                  ko_barrier=ko_barrier,
                  ko_payoff=ko_payoff,
                  maturity_coupon=maturity_coupon,
                  ki_barrier=ki_barrier,
                  ki_payoff=ki_payoff,
                  ki_status=BarrierStatus.UnHit)

risk_free_rate = 0.03
dividend_yield = 0
volatility = 0.2

process = BlackScholesProcess(start_date, initial_spot, risk_free_rate, dividend_yield, volatility, day_counter)

stime = time()
engine = MonteCarloEngine(process, 100000)

npv = option.pv(engine)
print(npv/initial_spot*100)
print(time()-stime)
