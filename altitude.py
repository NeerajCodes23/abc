import pyModeS as pms
import matplotlib.pyplot as plt


file1 = open('data/five_min_data.txt', 'r')
Lines = file1.readlines()

# Strips the newline character
timing=[]
messages=[]
for line in Lines:
    x = line.split()
    if len(x)<2:
        continue
    if (len(x[1])!=30):
        continue
    
    
    x[1]=(x[1][1:29])
    if pms.df(x[1])!=17:
        continue
    # print(x[1])
    timing.append(float(x[0]))
    messages.append(x[1])

n=  len(timing)
alt= dict()
alt_time=dict()
icaos=[]
for i in range(n):
    msg= messages[i]
    t= timing[i]
    icao= pms.adsb.icao(msg)
    if icao not in icaos:
        icaos.append(icao)
    tc= pms.adsb.typecode(msg)
    # print(tc)

    if tc==11:
        
        if icao in alt:
            alt[icao].append(pms.adsb.altitude(msg))
            alt_time[icao].append(t)
        else:
            alt[icao]= [pms.adsb.altitude(msg)]
            alt_time[icao]=[t]
        # print("altitude: ",pms.adsb.altitude(msg)) 

alt_n= len(alt)
plt.figure(0)
plt.xlabel("time(sec)")
plt.ylabel("altitude(feet)")
plt.title("Altitude Variations")
for x in icaos:
    if x in alt:
        plt.plot(alt_time[x],alt[x])
        # print(alt_time[x])

changes=dict()
for x in icaos:
    if x in alt:
        ln= len(alt[x])
        for i in range(1,ln):
            if x in changes:
                changes[x].append(abs((alt[x][i]-alt[x][i-1])/(alt_time[x][i]-alt_time[x][i-1])))
            else:
                changes[x]=[abs((alt[x][i]-alt[x][i-1])/(alt_time[x][i]-alt_time[x][i-1]))]
        
print(changes)
plt.figure(1)

for x in icaos:
    if x in changes:
        plt.plot(changes[x])
        # print(alt_time[x])   
plt.show()

# print(alt)


