import math
pi = math.pi
class Blackbody(object):
        
   @property
   def wavelength(self):
     return self._wavelength

   @wavelength.setter
   def wavelength(self, wavelength):
     self.wavelength = wavelength

   @property
   def temperature(self):
     return self._temperature
    
   @temperature.setter
   def temperature(self, temperature):
     self.temperature = temperature



   def __init__(self, wavelength, temperature):
                self._wavelength = wavelength
                self._absolute_temperature = temperature
                self._c1 = (3.74151e+8)
                self._c2 = (1.43879e+4)
                self._a = (2.89776855e+3)

   def __repr__(self):
                wavelengthstr = str(self._wavelength)
                temperaturestr = str(self._absolute_temperature)
                test = ("[wavelength = {0} microns, temperature = {1}K]".format(wavelengthstr, temperaturestr))
                return test

   def radiance(self):
                radiance = self._c1/ (((math.exp((self._c2)/ (self._wavelength*self._absolute_temperature))) - 1.0) *\
                pi*(self._wavelength**5.0))
                return radiance

   def peak_wavelength(self):
                return (self._a/self._absolute_temperature)


   def spectral_radiance(self, wavelengths):
                radiances = []
                lowerlimit = 8
                upperlimit = 14
                for i in range(0,1000, 1):
                  self._wavelength = lowerlimit + i*.006
                  r = self.radiance()
                #  radiances.append(L)
              #  for i in range(n):
              #   L = ((i/float(n-1)) * (upperlimit-lowerlimit) + lowerlimit)
                # r = Blackbody(L, 300)
                radiances.append(L)
                return radiances            
    
if __name__ == '__main__':
   import radiometry
   import matplotlib.pyplot
   import matplotlib.backends.backend_agg
   import matplotlib
   bb = Blackbody(10, 300)
   print(bb)
   print('L = {0} [W / m^2 / sr / micron]'.format(bb.radiance()))
   print('Peak wavelength = {0} [microns]'.format(bb.peak_wavelength()))
   
   wavelengths = []
   n = 1000
   lowerlimit = 8
   upperlimit = 14
   for i in range(n):
     wavelengths.append((i/float(n-1)) * (upperlimit-lowerlimit) + lowerlimit)


   figureTitle ='Blackbody Radiance'
   figure = matplotlib.pyplot.figure(figureTitle)

   canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(figure)

   axes = figure.add_subplot(1, 1, 1)
   axes.plot(wavelengths, bb.spectral_radiance(wavelengths))
   axes.set_xlabel('Wavelength (microns)')
   axes.set_ylabel('Radiance (W / m**2 / sr / micron')
   axes.set_title('Spectral Radiance')
   axes.set_xlim([7, 15])
   axes.set_ylim([7, 10])
   axes.grid()  

   matplotlib.pyplot.show()

   filename = 'Blackbody.eps'
   canvas.print_figure(filename)    


