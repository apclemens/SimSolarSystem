import math

masses = {'none':0}

def arctan2(y,x):
    if x>0:
        return math.atan(y/x)
    if y>=0 and x<0:
        return math.atan(y/x)+math.pi
    if y<0 and x<0:
        return math.atan(y/x)-math.pi
    if y>0 and x==0:
        return math.pi/2
    if y<0 and x==0:
        return -math.pi/2
    return 0

class ObjectInSpace:

    def __init__(self, info):
        global masses
        splitInfo = info.split('\n')
        self.name = splitInfo[0]
        self.relativeTo = splitInfo[1]
        self.mass = eval(splitInfo[2])
        self.a = eval(splitInfo[3])                 # semi-major axis
        self.e = eval(splitInfo[4])                 # eccentricity
        self.w = eval(splitInfo[5])*math.pi/180     # argument of periapsis
        self.omega = eval(splitInfo[6])*math.pi/180 # longitude of ascending node
        self.i = eval(splitInfo[7])*math.pi/180     # inclination
        self.M = eval(splitInfo[8])*math.pi/180     # mean anomaly
        self.mu = masses[self.relativeTo] * 1.993e-44

    def __repr__(self):
        try:
            return self.name+'\n'+str(self.mass)+'\n'+'\n'.join([str(i) for i in self.position])+'\n'+'\n'.join([str(i) for i in self.velocity])
        except:
            self.getCartesian()
            return self.__repr__()

    def getCartesian(self):
        if self.name == 'Sun':
            self.position = (0.0,0.0,0.0)
            self.velocity = (0.0,0.0,0.0)
            return
        # solve Kepler's Equation M=E-e*sin(E) for E
        E = self.M
        while abs(E-self.e*math.sin(E)-self.M) > .001:
            E = E - (E-self.e * math.sin(E)-self.M)/(1-self.e*math.cos(E))
        # obtain true anomaly
        v = 2*arctan2(math.sqrt(1+self.e)*math.sin(E/2),
                      math.sqrt(1-self.e)*math.cos(E/2))
        # use eccentric anomaly to get distance to central body
        r = self.a*(1-self.e*math.cos(E))
        # calculate orbital frame position and velocity
        orbFramePos = (r*math.cos(v),r*math.sin(v),0)
        o = math.sqrt(self.mu*self.a)/r  # orbital frame coefficient
        orbFrameVel = (-o*math.sin(E),o*math.sqrt(1-self.e**2)*math.cos(E),0.0)
        # calculate inertial frame position and velocity
        self.position = [orbFramePos[0]*(math.cos(self.w)*math.cos(self.omega)-math.sin(self.w)*math.cos(self.i)*math.sin(self.omega)) - orbFramePos[1]*(math.sin(self.w)*math.cos(self.omega)+math.cos(self.w)*math.cos(self.i)*math.sin(self.omega)),
                         orbFramePos[0]*(math.cos(self.w)*math.sin(self.omega)+math.sin(self.w)*math.cos(self.i)*math.cos(self.omega)) + orbFramePos[1]*(math.cos(self.w)*math.cos(self.i)*math.cos(self.omega)-math.sin(self.w)*math.sin(self.omega)),
                         orbFramePos[0]*(math.sin(self.w)*math.sin(self.i)) + orbFramePos[1]*(math.cos(self.w)*math.sin(self.i))]
        self.velocity = [orbFrameVel[0]*(math.cos(self.w)*math.cos(self.omega)-math.sin(self.w)*math.cos(self.i)*math.sin(self.omega)) - orbFrameVel[1]*(math.sin(self.w)*math.cos(self.omega)+math.cos(self.w)*math.cos(self.i)*math.sin(self.omega)),
                         orbFrameVel[0]*(math.cos(self.w)*math.sin(self.omega)+math.sin(self.w)*math.cos(self.i)*math.cos(self.omega)) + orbFrameVel[1]*(math.cos(self.w)*math.cos(self.i)*math.cos(self.omega)-math.sin(self.w)*math.sin(self.omega)),
                         orbFrameVel[0]*(math.sin(self.w)*math.sin(self.i)) + orbFrameVel[1]*(math.cos(self.w)*math.sin(self.i))]

    def correctCartesian(self, against):
        # we calculated the cartesian coordinates with respect to
        # the object it is orbiting.  We must add the coordinates for that
        # to get it with respect to the sun.
        for i in range(3):
            self.position[i] += against.position[i]
            self.velocity[i] += against.velocity[i]

def main():
    global masses
    f = open('keplerian.txt', 'r')
    l = f.read().split('\n\n')
    f.close()
    l.pop(0)
    while '' in l:
        l.remove('')

    for objInfo in l:
        splitInfo = objInfo.split('\n')
        masses[splitInfo[0]] = eval(splitInfo[2])

    f = open('cartesian.txt', 'w')
    objects = {}
    for objInfo in l:
        name = objInfo.split('\n')[0]
        objects[name] = ObjectInSpace(objInfo)
        objects[name].getCartesian()
        if name != 'Sun':
            objects[name].correctCartesian(objects[objects[name].relativeTo])
        f.write(objects[name].__repr__())
        f.write('\n\n')
    f.close()

if __name__ == '__main__':
    main()
