import math
import random
def monte_carlo_average(f, lowerLimit, upperLimit, acceptableError, maxIterations = 100000):
   """
   title::
      Monte Carlo Average

   description::
   This method will produce random x values and pass them through the function. This will create a certain amount of y values over the
   range or bounds. The method then creates a sum of the y values and takes the average y value. The area can be calulated by multiplying 
   the average y value by the change in x value bounds.

   attributes::
   Function: f(x) provided in the test harness and allows it to be called
   Limits: Upper and lower limits that give bound in which to calculate values
   acceptableError: the allowed error for the calculations to be compared to
   MaxIterations : the maximum amount of times the for loop goes through, sets a cutoff for calculations
      
   author:
   Trevor Brashich

   copyright::
      Copyright (C) 2016, Rochester Institute of Technology
    """

    fAverageSum = 0
    fAverageSumSquared = 0
    error = 1
    NumberIterations = 0

    while error > acceptableError or NumberIterations < 10:
       NumberIterations += 1
       if NumberIterations > maxIterations:
          raise RuntimeError ('Max Iterations Exceeded')

       y = f(random.uniform(lowerLimit, upperLimit))
       fAverageSum = y + fAverageSum
       fAverageSumSquared = y**2 + fAverageSumSquared
       fAverage = fAverageSum / NumberIterations
       F2Average = fAverageSumSquared / NumberIterations
       error = (upperLimit - lowerLimit) * math.sqrt((F2Average - fAverage**2) / NumberIterations)
    area = (upperLimit - lowerLimit) * fAverage
    return area


if __name__ == '__main__':

   import math
   import numerical.integrate
   import time

   def f(x):
      return math.sqrt(x)

   lowerLimit = 0.0
   upperLimit = 1.0
   for acceptableError in (0.1, 0.01, 0.001, 0.0001):
      startTime = time.time()
      area = numerical.integrate.monte_carlo_average(f, 
                                                     lowerLimit, 
                                                     upperLimit, 
                                                     acceptableError)
      print('Elapsed time = {0:.6f} [s]'.format(time.time() - startTime))
      print('With an acceptable error of {0:.10f}'.format(acceptableError))
      print('Area of f(x)=sqrt(x) over [{0}, {1}] = {2}'.format(lowerLimit,
                                                                upperLimit,
                                                                area))

