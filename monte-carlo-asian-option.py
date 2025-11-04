import numpy as np

'''
What is Asian option: Asian Option looks at the averge price of the underlying asset over a certain period of time
rather than the price at maturity to determine the payoff. This feature makes Asian options less
susceptible to market manipulation and price volatility.
思路：调整资产的概率：通过蒙特卡洛模拟足够多的资产价格路径，每次路径的分布概率通过人为调整，满足
风险中性分布概率。通过足够多次的模拟，最终获得符合要求的期权价格。
'''

def Binary_tree(S, K, r, up, down, steps):
    '''
    Inputs
    S = Current stock Price
    K = Strike Price
    r = risk free interest rate
    up = increase rate for up movement
    down = decrease rate for down movement

    Output
    # call_price = value of the option 
    '''
    # Use risk-neutral probability with gross returns: U=1+up, D=1+down, R=1+r
    U = 1 + up
    D = 1 + down
    R = 1 + r
    Pu = (R - D) / (U - D)  # risk-neutral probability for up movement
    Pd = 1 - Pu  # risk neutral probability for down movement
    # Four step binomial tree
    # Cuuuu = max(0, S * (1 + up) ** 4 - K)  # call option value at up-up-up-up state
    # Cuuud = max(0, S * (1 + up) ** 3 * (1 + down) - K)  # call option value at up-up-up-down state
    # Cuudd = max(0, S * (1 + up)**2 * (1 + down) ** 2 - K)  # call option value at up-up-down-down state
    # Cuddd = max(0, S * (1 + up) * (1 + down) ** 3 - K)  # call option value at up-down-down-down state
    # Cdddd = max(0, S * (1 + down) ** 4 - K)  # call option value at down-down-down-down state
    
    n_steps = steps
    n_paths = 2 ** n_steps  # number of possible paths
    expected_payoff = 0.0
    for i in range(n_paths):
        binary_path = format(i, f'0{n_steps}b') # Generate four binary representation of i (different possible combinations)
        
        # Reset for each path
        stock_price = S 
        path_prices = [S]  # Start with initial price
        
        # Calculate price path
        for move in binary_path:
            if move == '1':
                stock_price = stock_price * (1 + up)
            else:
                stock_price = stock_price * (1 + down)
            path_prices.append(stock_price)
        
        avg_price = np.mean(path_prices) 
        #compare the average price with strike price, if avg price > strike price, return the difference between them, else return 0 (no excercise)
        call_values_end_of_the_term = max(0, avg_price - K)
        
        # Calculate risk-neutral probability for this specific path
        n_ups = binary_path.count('1')
        n_downs = n_steps - n_ups
        risk_neu_prob = (Pu ** n_ups) * (Pd ** n_downs)

        # Accumulate expected payoff under risk-neutral measure
        expected_payoff += call_values_end_of_the_term * risk_neu_prob

    # Discount expected payoff back to present value (discrete compounding)
    option_price = expected_payoff / (R ** n_steps)
    return option_price
    


def Monte_Carlo_Asian(initial, exercise, up, down, interest, periods, runs):
    '''
    Monte Carlo simulation for Asian options using adjusted probabilities in a binomial tree framework.
    
    Inputs:
    initial = Current stock price
    exercise = Strike price
    up = Up movement rate
    down = Down movement rate
    interest = Risk-free interest rate
    periods = Number of time periods (1+periods=total steps)
    runs = Number of simulation paths
    
    Returns:
    option_price = Estimated option price
    '''
    Pu = (interest - down) / (up - down)  # risk neutral probability for up movement
    Pd = 1 - Pu  # risk neutral probability for down movement
    payoffs = [] # total call option payoffs for all runs
    for _ in range(runs):
        #initialize price and price path to aggregate before each run
        stock_price = initial
        path_prices = [initial]
        
        for _ in range(periods):
            if np.random.rand() > Pd:
                stock_price *= (1 + up)
            else:
                stock_price *= (1 + down)
            path_prices.append(stock_price)
        
        avg_price = np.mean(path_prices)
        payoff = max(0, avg_price - exercise)
        payoffs.append(payoff)
    
    option_price = np.exp(-interest * periods) * np.mean(payoffs) # Discounted expected payoff
    
    return option_price

        
            

# Test the functions
if __name__ == "__main__":
    # Parameters
    S = 100  # Current stock price
    K = 100  # Strike price
    T = 1    # Time to maturity
    r = 0.05 # Risk-free rate
    up = 0.2 # Up movement
    down = -0.3 # Down movement
    
    price = Binary_tree(S, K, r, up, down, 4)
    prince_mc = Monte_Carlo_Asian(S, K, up, down, r, 4, 10000)
    print(f"Binary Tree Asian Option Price: {price:.2f}")
    print(f"Monte Carlo Asian Option Price: {prince_mc:.2f}")

