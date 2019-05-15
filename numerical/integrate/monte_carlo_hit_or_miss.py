import math
import random
import time
def monte_carlo_hit_or_miss(f, lowerLimit, upperLimit, acceptableError, maxIterations = 100000):
   """
   title::
      Monte Carlo Hit or Miss

   description::
   This method will produce 10000 (numberiteration) random x values and pass them through the function and also add them to a list.
   It will then compare 10000 random y values to the y values passed through the function. This will then calculate whether the point
   hit or missed the functions curve. It then uses that to determine the area using the monte carlo formula

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

   yList = []
   NumberIterations = 10000
   hits = 0
   error = 1
   
   
   while error > acceptableError or NumberIterations < 10 or hits == NumberIterations:
     if NumberIterations > maxIterations:
        raise RuntimeError ('Max Iterations Exceeded')

     for i in range(NumberIterations):
       x = random.random()
       yList.append(f(x))
       randomy = random.random()
       y = f(x)
       if randomy <= y:
         hits += 1.0
       yMax = max(yList)
       ratio = float(hits) / NumberIterations
     error = (2.0 / 3.0) * (upperLimit - lowerLimit) * yMax * math.sqrt((ratio * (1 - ratio)) / 10000)
   area = ratio * (upperLimit - lowerLimit) * yMax
   return area  



if __name__ == "__main__":

   import math
   import numerical.integrate
   import time

   def f(x):
      return math.sqrt(x)

   lowerLimit = 0.0
   upperLimit = 1.0
   for acceptableError in (0.1, 0.01, 0.001, 0.0001):
      startTime = time.time()
      area = numerical.integrate.monte_carlo_hit_or_miss(f,
                                                         lowerLimit,
                                                         upperLimit,
                                                         acceptableError)
      print('Elapsed time = {0:.6f} [s]'.format(time.time() - startTime))
      print('With an acceptable error of {0:.10f}'.format(acceptableError))
      print('Area of f(x)=sqrt(x) over [{0}, {1}] = {2}'.format(lowerLimit,
                                                                upperLimit,
                                                                area))

