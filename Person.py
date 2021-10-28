from random import randint
import time

class MyPerson:
    tracks = []
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def going_UP(self,mid_start,mid_end,x_line_up,x_line_down):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end and self.tracks[-2][0]<=1200 and self.tracks[-2][0]>599 and self.tracks[-1][0]<=1200 and self.tracks[-1][0]>599:
                    print("tracs up : self.tracks[-1][1] :",self.tracks[-1][1],"self.tracks[-2][1] :",self.tracks[-2][1])
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end,x_line_up,x_line_down):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start and self.tracks[-2][0]<=1300 and self.tracks[-2][0]>0 and self.tracks[-1][0]<=1300 and self.tracks[-1][0]>0:
                    print("tracs down : self.tracks[-1][1] :", self.tracks[-1][1], "self.tracks[-2][1] :",
                          self.tracks[-2][1])
                    print(self.tracks)
                    state = '1'
                    self.dir = 'down'
                    # time.sleep(3)
                    return True
            else:
                return False
        else:
            return False

    def deneme(self,mid_start,mid_end,x_line_up,x_line_down):



        if len(self.tracks) >= 2:
            try:

                self.x_son = self.tracks[-1][0]
                print("x_son :",self.x_son)

                self.t = ((400-self.tracks[-2][1])*4)
                print("t :",self.t)

                self.ilk_y = self.tracks[-2][1]
                print("ilk_y :", self.ilk_y)

                self.son_y = self.tracks[-1][1]
                print("son_y :", self.son_y)

                self.x_ilk = self.tracks[-2][0]
                print("x_ilk :", self.x_ilk)



            except Exception as e:
                print(e)
            if self.state == '0':
                if self.x_son <= (self.t+3) and self.x_son >=(self.t-10) and self.x_ilk<=1000 and self.x_ilk>0 and self.x_son<=1000 and self.x_son>0 and self.son_y<=400 and self.son_y>154 and self.ilk_y<=400 and self.ilk_y>154  and self.ilk_y>self.son_y:
                    print("tracs capraz : self.tracks[-1][1] :", self.tracks[-1][1], "self.tracks[-2][1] :",
                          self.tracks[-2][1])
                    print(self.tracks)
                    state = '1'
                    self.dir = 'capraz'
                    # time.sleep(1)
                    return True
            else:
                return False
        else:
            return False



    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
class MultiPerson:
    def __init__(self, persons, xi, yi):
        self.persons = persons
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False

