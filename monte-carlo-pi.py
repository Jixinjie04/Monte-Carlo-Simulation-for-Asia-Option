import random
import matplotlib.pyplot as plt
import numpy as np
def estimate_pi(num_samples):
    inside_circle = 0
    for i in range(num_samples):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        if x**2+y**2 <=1:
            inside_circle += 1
    pi_estimate = 4 * (inside_circle/num_samples)
    return pi_estimate
    
pi = estimate_pi(100000)
print(f"Estimated value of Pi: {pi}")   


num_samples = 10000
x = np.random.uniform(0, 1, num_samples)
y = np.random.uniform(0, 1, num_samples)
plt.plot(x,y,'k.',markersize=1)

t=np.linspace(0,np.pi/2,100)
plt.plot(np.cos(t),np.sin(t),'r-')

#set the axis limits and labels
plt.xlim(0,1)
plt.ylim(0,1)
plt.xlabel('x')
plt.ylabel('y')

plt.title('Monte Carlo Pi Estimation')
plt.show()