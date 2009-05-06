import math

from compsoc.events.models import *
from collections import defaultdict
from django.contrib.auth.models import User

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = int(x)
        self.y = int(y)
        
    def __getitem__(self, key):
        if( key == 0):
            return self.x
        elif( key == 1):
            return self.y
        else:
            raise Exception("Invalid key to Point")
        
    def __setitem__(self, key, value):
        if( key == 0):
            self.x = value
        elif( key == 1):
            self.y = value
        else:
            raise Exception("Invalid key to Point")
        
    def __unicode__(self):
        return u'(%s,%s)' % (self.x,self.y)
    
    def distance(self, point2):
        """Returns the distance between to another point"""
        # this is to insert gutters between tables
        self_x = self.x + (self.x/2)
        point2_x = point2.x + (point2.x/2)
        return math.sqrt( ( (self_x-point2_x)**2 + (self.y-point2.y)**2) )
        
def ave(points):
    return reduce(lambda x,y:x+y,points)/len(points)

def distance_matrix():
    """
        Calculates a mapping from users onto distances
    """
    # Build lookup map
    # TODO: remove duplicate computations
    # weight score by frequency
    lookup = defaultdict(lambda: defaultdict(lambda: []))
    for event in Event.objects.all():
        seating = SeatingRevision.objects.filter(event=event).order_by('-number')
        if seating:
            latest = seating[0]
            cache = {}
            for s in latest.seating_set.all():
                cache[s.user] = Point(s.col,s.row)
            for user in cache.keys():
                for other in cache.keys():
                    if other != user:
                        lookup[user][other].append(cache[user].distance(cache[other]))
    
    results = defaultdict(lambda:{})
    
    # Average distances
    for user,others in lookup.items():
        for other,values in others.items():
            results[user][other] = ave(values)

    return results

def closest_person():
    distances = distance_matrix()
    results = []
    for user,others in distances.items():
        other,score = sorted(others.items(),key=lambda (u,v):v)[0]
        results.append((user,other,score))
    return results

