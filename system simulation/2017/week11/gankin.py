def sim(principal=30000000, duration=12 * 30, annual_interest_rate=0.02, semiannual_payment=300000):
    monthly_interest_rate = annual_interest_rate / 12
    balance = principal

    for month in range(1, duration + 1):
        interest = balance * monthly_interest_rate
        payment = ((principal - (duration // 6 * semiannual_payment)) / duration)
        balance -= payment

        if month % 6 == 0:
            balance -= semiannual_payment

        print(month, balance, payment, interest, payment + interest)


if __name__ == '__main__':
    sim()
