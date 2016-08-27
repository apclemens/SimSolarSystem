import urllib2

def getAsteroidParam(html, paramName):
    for line in html:
        if '<param NAME="'+paramName+'" VALUE="' in line:
            break
    return '\n'+line.split(' VALUE="')[1].split('"')[0]

def getAsteroid(n):
    url = 'http://ssd.jpl.nasa.gov/sbdb.cgi?orb=1;sstr='+str(n)
    page = urllib2.urlopen(url)
    html = page.read().split('\n')
    for line in html:
        if 'param NAME="Name" VALUE="' in line:
            break
    name = line.split('param NAME="Name" VALUE="')[1].split('"')[0]
    print name
    info = name+'\n'+'Sun'
    #mass is not on jpl for some reason, get off of wolframalpha
    info += '\n0'
    #semi major axis
    info += '\n'+str(eval(getAsteroidParam(html,'a')))
    #eccentricity
    info += getAsteroidParam(html,'e')
    #argument of periapsis
    info += getAsteroidParam(html,'Peri')
    #long of ascending node
    info += getAsteroidParam(html,'Node')
    #inclination
    info += getAsteroidParam(html,'Incl')
    #mean anomaly
    info += getAsteroidParam(html,'M')
    return info

def getPlanets():
    url = 'http://ssd.jpl.nasa.gov/txt/p_elem_t2.txt'
    page = urllib2.urlopen(url)
    html = page.read().split('\n')
    copy = False
    lines = []
    for line in html:
        if list(set(line)) == ['-']:
            if copy:
                break
            copy = True
        else:
            if copy and line[0] != ' ':
                lines.append(line)
    ret = ''
    for line in lines:
        #for some reason jpl lists Earth as "EM Bary"...
        newLine = line.replace('EM Bary','Earth')
        while '  ' in newLine:
            newLine = newLine.replace('  ',' ')
        info = newLine.split(' ')
        ret += info[0] + '\n' + 'Sun' + '\n' + str(getMass(info[0])) + '\n'
        ret += str(eval(info[1])) + '\n'
        ret += info[2] + '\n'
        ret += info[5] + '\n'
        ret += info[6] + '\n'
        ret += info[3] + '\n'
        ret += info[4] + '\n\n'
    return ret

def getMass(name):
    url = 'http://ssd.jpl.nasa.gov/?planet_phys_par'
    page = urllib2.urlopen(url)
    html = page.read().split('\n')
    for line in html:
        if '<td align="left">'+name in line:
            break
    return html[html.index(line)+20].split('>')[1].split('<')[0]+'e24'

def getMoons():
    planets = ['Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
    linesToFind = {}
    for plan in planets:
        linesToFind['<a name="'+plan.lower()+'"> </a>'] = plan
    url = 'http://ssd.jpl.nasa.gov/?sat_elem'
    page = urllib2.urlopen(url)
    htmlStr = page.read()
    htmlStr = htmlStr.replace('</TD>','</TD>\n').replace('\n\n','\n')
    html = htmlStr.split('\n')
    currentPlanet = ''
    info = []
    currInfo = []
    i = -1
    for line in html:
        if i >= 0:
            i += 1
            if i == 1:
				currInfo.append(str(6.685e-9*eval(line.split('>')[1].split('<')[0])))
            else:
                currInfo.append(line.split('>')[1].split('<')[0])
            if i == 6:
                i = -1
                info.append(currInfo)
                currInfo = []
        if line in linesToFind.keys():
            currentPlanet = linesToFind[line]
        if '<TR ALIGN=right><TD ALIGN=left>' in line:
            currentMoon = line.split('<TR ALIGN=right><TD ALIGN=left>')[1].split('<')[0]
            currInfo.append(currentMoon)
            currInfo.append(currentPlanet)
            currInfo.append('0')
            i = 0
    ret = ''
    for moon in info:
        ret += '\n'.join(moon[:6])
        ret += '\n'+moon[8]+'\n'+moon[7]+'\n'+moon[6]+'\n\n'
    return ret

def main():
    f = open('keplerian.txt', 'w')

    # first add header and the Sun
    f.write('/*\nName\nObject this orbits around\nMass\nSemi-major axis (a)\nEccentricity (e)\nArgument of periapsis (w)\nLongitude of ascending node (omega)\nInclination (i)\nMean anomaly (M)\n*/\n\nSun\nnone\n1.989e30\n0\n1\n0\n0\n0\n0\n\n')
    #then the planets
    f.write(getPlanets())
    #then moons
    f.write(getMoons())
    #then asteroids
    for i in range(1,21):
        f.write(getAsteroid(i))
        f.write('\n\n')
    #TODO: kuiper belt, halley's comet, other things
    f.close()

if __name__ == '__main__':
    main()
