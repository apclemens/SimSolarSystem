# SimSolarSystem

Runge-Kutta numerical simulation of our Solar System.
Currently includes the Sun, planets (and Pluto), moons, and 20 objects in the asteroid belt.

Should be run in this order:
 * populateKepler.py (scrapes Keplerian coordinates of objects from Jet Propulsion Laboratory's website)
 * convertToCartesian.py (converts the coordinates from Keplerian to Cartesian)
 * system.py (runs the simulation)
 * draw.py (draws images and creates a video)

Here are the results for different values of delta t.  You can see that when delta t is high, the simulation is not very precise and the moons start flying everywhere.  It takes a very small value of delta t for the moons to have a stable orbit around the planets.

| delta t | Result (inner) | Result (outer) |
| :------------- | :--------- | :--------- |
| 1 minute | http://i.imgur.com/gUAJfMi.gif | http://i.imgur.com/Hrb0Ul6.gif |
| 5 minutes | http://i.imgur.com/cXYWHdQ.gif | http://i.imgur.com/VEwUoxI.gif |
| 15 minutes | http://i.imgur.com/XirxJQk.gif | http://i.imgur.com/XLRz0OB.gif |
| 30 minutes | http://i.imgur.com/PRG3U8c.gif | http://i.imgur.com/eqyIN3s.gif |
| 1 hour | http://i.imgur.com/BIu4ZqL.gif | http://i.imgur.com/jY27FA3.gif |
| 3 hours | http://i.imgur.com/8F0OJmO.gif | http://i.imgur.com/yGszUDp.gif |
| 6 hours | http://i.imgur.com/pGRqE22.gif | http://i.imgur.com/zMgB3ex.gif |
| 12 hours | http://i.imgur.com/AtvIwUZ.gif | http://i.imgur.com/VXeQpYI.gif |
| 1 day | http://i.imgur.com/hRzfNyM.gif | http://i.imgur.com/Y8aFRHa.gif |
