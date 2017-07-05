def sim(principal=20000000, duration=240, annual_interest_rate=0.025, semiannual_payment=0):
    monthly_interest_rate = annual_interest_rate / 12
    balance = principal

    interest_history = [0]
    balance_history = [balance]
    total_payment = 0

    for month in range(1, duration + 1):
        interest = balance * monthly_interest_rate
        payment = ((principal - (duration // 6 * semiannual_payment)) / duration)
        balance -= payment

        if month % 6 == 0:
            balance -= semiannual_payment

        interest_history.append(interest)
        balance_history.append(balance)

        print(month, balance, payment, interest, payment + interest)

    return interest_history, balance_history


if __name__ == '__main__':
    i, b = sim()

    print(i)
    print(b)
