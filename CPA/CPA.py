import math
from math import sin,cos,asin,acos,sqrt,atan2,radians,pi,degrees


class Ship:
    def __init__(self, position, speed, heading):

        self.position = position
        self.speed = speed
        self.heading = heading


def ARPA_calculations(objectA, objectB, *args, **kwargs):

    if isinstance(objectA, Ship) == False or isinstance(objectB, Ship) == False :
        raise NameError('This function is only usable with Ship instances')

    pointA = objectA.position
    objectA_speed = objectA.speed
    vectorA_angle =objectA.heading
    pointB = objectB.position
    objectB_speed = objectB.speed
    vectorB_angle =objectB.heading

    posAatcpa = kwargs.get('posAatcpa', None)
    posBatcpa = kwargs.get('posBatcpa', None)

    #Calculation of relative object datas from object B to object A
    (vectorB_angle_relativ,objectB_speed_relative) = calculate_relative_vector(pointA,objectA_speed, vectorA_angle,pointB,objectB_speed, vectorB_angle)

    if ((objectA_speed == objectB_speed) and (vectorA_angle == vectorB_angle)) or (objectA_speed <= 0.001 and objectB_speed <= 0.001):

        print("Already at her minimum CPA") 
        cpa = round(calculate_distance(pointA,pointB), 2)
        
        return {'cpa': cpa,'tcpa': 0 }
    
    elif pointA == pointB :
        
        print("Objects in the same position") 
        return {'cpa': 0,'tcpa': 0 }
    
    else:

        #Check if the object is already at his minimum CPA
        if check_ship_going_away(pointA,vectorA_angle,pointB,vectorB_angle_relativ,objectB_speed_relative) == True :
            
            print("Ship going away, already at her minimum CPA") 
            cpa = round(calculate_distance(pointA,pointB), 3)

                
            return {'cpa': cpa,'tcpa': 0}
        
        else:
            
            #Calculation of the crossing lines position
            cp_position = calculate_cp_position (pointA,objectA_speed, vectorA_angle,pointB,objectB_speed, vectorB_angle,vectorB_angle_relativ,objectB_speed_relative)

            #Is the CPA position ahead or astern the ship's beam ?
            signe = calculate_CPA_sign(vectorA_angle,pointA, cp_position)

            cpa = round(calculate_distance(pointA,cp_position)* signe, 3)

            tcpa = (calculate_distance(pointB,cp_position) / objectB_speed_relative)*60.0

            latAcpa , lonAcpa = calculate_future_position(pointA,objectA_speed*tcpa/60, vectorA_angle)
            latBcpa , lonBcpa = calculate_future_position(pointB,objectB_speed*tcpa/60, vectorB_angle)

            return {'cpa': cpa , 'tcpa':tcpa}

def check_ship_going_away(pointA,vectorA_angle,pointB,vectorB_angle_relativ,objectB_speed_relative):
    
    #Check if the objects are getting away from each other at the initial conditions

    if calculate_distance(pointA, calculate_future_position(pointB,0.0001*objectB_speed_relative, vectorB_angle_relativ)) < calculate_distance(pointA, pointB):
        return False
    else:
        return True
    
        
def calculate_cp_position (pointA, objectA_speed, vectorA_angle, pointB, objectB_speed, vectorB_angle, vectorB_angle_relative, objectB_speed_relative):

    #Calculation of objects' positions one hour later
    pointA2 = calculate_future_position(pointA,objectA_speed, vectorA_angle)
    pointB2 = calculate_future_position(pointB,objectB_speed, vectorB_angle)

    #Calculation of the angle of the perpendicular line to the relative vector (r_ppl_a)
    lat1A = pointA[0]
    lon1A = pointA[1]
    lat2A = pointA2[0] 
    lon2A = pointA2[1]

    dlonA = lon2A-lon1A
    dlatA = lat2A-lat1A

    lat1B = pointB[0]
    lon1B = pointB[1]
    lat2B = pointB2[0]
    lon2B = pointB2[1]

    dlonB = lon2B-lon1B
    dlatB = lat2B-lat1B

    dlonAR = dlonB-dlonA
    dlatAR =dlatB-dlatA
    
    #To get a r_ppl_a between 0deg and 360deg
    if (dlonAR >0 and dlatAR >0) or (dlonAR <0 and dlatAR <0):

        r_ppl_a = (vectorB_angle_relative-90) % 360

    else:

        r_ppl_a = (vectorB_angle_relative+90) % 360

    #print r_ppl_a
        
    return calculate_cross_path_position(pointA, r_ppl_a, pointB, vectorB_angle_relative)

    
def calculate_CPA_sign(vectorA_angle,pointA, cp_position):
    
    CPA_point_relative_bearing = calculate_relative_bearing(vectorA_angle, calculate_bearing(pointA, cp_position) )

    if (CPA_point_relative_bearing >90) and (CPA_point_relative_bearing <270):
        return  -1
    else:
        return  1   

def calculate_relative_vector(pointA,objectA_speed, vectorA_angle,pointB,objectB_speed, vectorB_angle):
    
    pointB2 = calculate_future_position(pointB,objectB_speed, vectorB_angle)
    pointA2 = calculate_future_position(pointA,objectA_speed, vectorA_angle)
    vectorA_angle_opp = calculate_bearing(pointA2, pointA)
    pointA3 = calculate_future_position(pointB2,objectA_speed, vectorA_angle_opp)

    vectorB_angle_relative = calculate_bearing(pointB,pointA3)
    objectB_speed_relative = calculate_distance(pointB,pointA3)
    
    return (vectorB_angle_relative,objectB_speed_relative)


def calculate_distance(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    #With Haversine formulae
    
    lat1 = radians(pointA[0])
    lon1 = radians(pointA[1])
    lat2 = radians(pointB[0])
    lon2 = radians(pointB[1])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a= sin(dlat/2.)**2 + cos(lat1)*cos(lat2)*sin(dlon/2.)**2
    c = 2*asin(sqrt(a))
    distance = 6378.137*c/1.852

    return distance

def calculate_bearing(pointA, pointB):
    
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)* cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x,y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180deg to + 180deg which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below

    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def calculate_relative_bearing(own_object_heading, object_bearing):

    a= own_object_heading - object_bearing

    if a > 0 :
        relative_bearing = 360-a
    else :
        relative_bearing= -a

    return relative_bearing

def calculate_future_position(pointA, object_speed, vector_angle):

    object_speed = object_speed*1.852

    lat1 = radians(pointA[0])
    lon1 = radians(pointA[1])
    vector_angle = radians(vector_angle)

    lat2 = asin(sin(lat1)*cos(object_speed/6378.137)+cos(lat1)*sin(object_speed/6378.137)*cos(vector_angle))
    lon2 = lon1+ atan2(sin(vector_angle)*sin(object_speed/6378.137)*cos(lat1),cos(object_speed/6378.137)-sin(lat1)*sin(lat2))

    return(round(degrees(lat2),7), round(degrees(lon2),7)) 

def calculate_cross_path_position(pointA, bearing1,pointB, bearing2):

    lat1 = radians(pointA[0])
    lon1 = radians(pointA[1])
    lat2 = radians(pointB[0])
    lon2 = radians(pointB[1])
    bearing1 = radians(bearing1)
    bearing2 = radians(bearing2)

    dlon = lon2-lon1
    dlat = lat2-lat1

    r= 2*asin(sqrt(sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2))

    ta = acos((sin(lat2)-sin(lat1)*cos(r))/(sin(r)*cos(lat1)))
    tb = acos((sin(lat1)-sin(lat2)*cos(r))/(sin(r)*cos(lat2)))

    if sin(dlon)>0:
        t12=ta
        t21=2*pi-tb

    else:
        t12=2*pi-ta
        t21=tb

    a1= (bearing1-t12 +pi) % (2*pi)-pi
    a2 = (t21- bearing2+pi) % (2*pi)-pi

    a3=acos(-cos(a1)*cos(a2)+sin(a1)*sin(a2)*cos(r))

    y=atan2(sin(r)*sin(a1)*sin(a2),cos(a2)+cos(a1)*cos(a3))
    lat3=asin(sin(lat1)*cos(y)+cos(lat1)*sin(y)*cos(bearing1))
    dlon13 = atan2(sin(bearing1)*sin(y)*cos(lat1),cos(y)-sin(lat1)*sin(lat3))
    lon3 = (lon1 + dlon13 + pi) % (2*pi) - pi

    return( round(degrees(lat3),5),round(degrees(lon3),5))

def dms_to_dd(degrees, minutes=0, seconds=0):
    
    if degrees >= 0:
        decimal = degrees + minutes/60.0 + seconds/3600.0
    else:
        decimal = degrees - minutes/60.0 - seconds/3600.0

    return decimal

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Navigational ARPA calculator",epilog="By E.Maufay")
    
    group1 = parser.add_mutually_exclusive_group()  

    group1.add_argument("-t", "--test", action="store_true",help="Proceed a test run")

    args = parser.parse_args()

    if args.test:
        print("Some tests :") 
        print("objectA = Ship((39,2),12,80)") 
        objectA = Ship((39,2),12,80)
        print("objectB = Ship((39.5,3),20,320)") 
        objectB = Ship((39.5,3),20,320)
        print("results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)") 
        results = ARPA_calculations(objectA, objectB)
        print() 
        print(results) 
        
    else:
        parser.print_help()

    
