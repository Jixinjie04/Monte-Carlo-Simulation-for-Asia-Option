import numpy as np
import pandas as pd



'''
What is Asian option: Asian Option looks at the averge price of the underlying asset over a certain period of time
rather than the price at maturity to determine the payoff. This feature makes Asian options less
susceptible to market manipulation and price volatility.
思路：调整资产的概率：通过蒙特卡洛模拟足够多的资产价格路径，每次路径的分布概率通过人为调整，满足
风险中性分布概率。通过足够多次的模拟，最终获得符合要求的期权价格。
'''

def Binary_tree(S,K,r,up,down):
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
    Pu = (1 + r - (1 + down)) / ((1 + up) - (1 + down))  # risk neutral probability for up movement
    Pd = 1 - Pu  # risk neutral probability for down movement
    # Four step binomial tree
    # Cuuuu = max(0, S * (1 + up) ** 4 - K)  # call option value at up-up-up-up state
    # Cuuud = max(0, S * (1 + up) ** 3 * (1 + down) - K)  # call option value at up-up-up-down state
    # Cuudd = max(0, S * (1 + up)**2 * (1 + down) ** 2 - K)  # call option value at up-up-down-down state
    # Cuddd = max(0, S * (1 + up) * (1 + down) ** 3 - K)  # call option value at up-down-down-down state
    # Cdddd = max(0, S * (1 + down) ** 4 - K)  # call option value at down-down-down-down state
    
    n_steps = 4
    n_paths = 2**n_steps  # 16 possible paths for 4 steps
    call_prices = [] # Keep track of how much you pay for to have the right to use the option
    
    # Lists to store data for dataframe
    all_paths = []
    all_avgs = []
    all_probs = []
    
    for i in range(n_paths):
        binary_path = format(i, f'0{n_steps}b')
        
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
        
        # Calculate risk-neutrality probability for each path
        n_ups = binary_path.count('1')
        n_downs = n_steps - n_ups
        risk_neu_prob = Pu**n_ups * Pd**n_downs
        
        call_prices.append(call_values_end_of_the_term * risk_neu_prob)
        
        # Store data for dataframe
        all_paths.append(binary_path)
        all_avgs.append(avg_price)
        all_probs.append(risk_neu_prob)
        
        print(f"Path: {binary_path}, Prices: {[f'{p:.2f}' for p in path_prices]}, Avg: {avg_price:.2f}, Probability:{risk_neu_prob:.4f}")
    
    # Create dataframe
    # df = pd.DataFrame({
    #     'Path': all_paths,
    #     'T1': path_prices[0],
    #     'T2': path_prices[1],
    #     'T3': path_prices[2],
    #     'T4': path_prices[3],
    #     'Avg': all_avgs,
    #     'Probability': all_probs
    # })
    
    # # Calculate option price
    # option_price = np.sum(call_prices) / ((1 + r) ** n_steps)
    
    # return option_price, df

