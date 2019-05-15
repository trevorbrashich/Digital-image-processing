import radiometry



def bb_temperature(wavelength, radiance, epsilon = 1e-8 ):
  bb = radiometry.Blackbody(wavelength, radiance)
  Tlow = 0.0
  Thigh = 6000.0  
  temperature = (Thigh + Tlow) / 2
  while (Thigh - Tlow) > epsilon:
   temperature = (Thigh + Tlow) / 2
   bb.absolute_temperature = temperature
   if bb.radiance() > radiance:
    Thigh = temperature
   else:
    Tlow = temperature
  return temperature



if __name__ == '__main__':

   import radiometry

   wavelength = 10 # microns
   trueTemperature = 300 # Kelvin

   bb = radiometry.Blackbody(wavelength, trueTemperature)
   radiance = bb.radiance()

   temperature = radiometry.bb_temperature(wavelength, radiance, epsilon=1e-6)
   print('T = {0} [K]'.format(temperature))
   print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
   print('at {0} [microns]'.format(wavelength))

   temperature = radiometry.bb_temperature(wavelength, radiance, epsilon=1e-2)
   print('T = {0} [K]'.format(temperature))
   print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
   print('at {0} [microns]'.format(wavelength))

   temperature = radiometry.bb_temperature(wavelength, radiance)
   print('T = {0} [K]'.format(temperature))
   print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
   print('at {0} [microns]'.format(wavelength))


