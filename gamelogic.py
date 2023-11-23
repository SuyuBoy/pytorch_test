import random




class Game_elements:
    User = ["User", 1, True, False, False]
    Wall = ["Wall", 2, True, True,  False]
    GreatWall = ["GreatWall", 3, False, True, False]
    Points = ["Points", 4, True, False, True]
    Air = ["Air", 5, True, False, True]
    Bomb = ["Bomb", 6, True, True, True]

    def __init__(self, build : list):
        self.name : str = build[0]
        self.id : int= build[1]
        self.MoveAble : bool = build[2]
        self.CleanAble : bool= build[3]
        self.ThroughAble : bool= build[4]
        self.tempMoveable : bool= 0
        if self.MoveAble == True:
            self.tempMoveable : bool= True
        self.scores : int = 1
        return 
    
    def score_plus(self, Nowscore : int) -> int:
        return Nowscore + self.scores
    
    def Clean(self, Nowscore : int):
        if self.name == "Wall" or self.name == "GreatWall":
            return Game_elements(Game_elements.Points), Nowscore
        if self.name == "Points":
            return Game_elements(Game_elements.Air), Nowscore + 5
        
class Game:
    def __init__(self):
        #one as Player
        self.__GamePad :list[list[Game_elements]] = \
        [[0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]] 
        self.__Sizecol = len(self.__GamePad)
        self.__Sizerow = len(self.__GamePad[0])
        for i in range(self.__Sizecol):
            for j in range(self.__Sizerow):
                self.__GamePad[i][j]= Game_elements(Game_elements.Air)
        self.__GamePad[2][2] = Game_elements(Game_elements.User)
        self.__GamePad[1][2] = Game_elements(Game_elements.Wall)
        self.__UserPosi : list = [2,2]
        self.__lastposi : list = [0,0]
        self.__StopPunish = 2
        self.__samekeyPunish = 1

        # print()

        self.__key = 0 # k {1,2,3,4} 上下左右
        self.__lastkey = 0
        # self.__Gamer_Posi = [2,2]
        self.__Score = 0
        return 
        
    def Game_logic(self):
        self.move_posi(self.__UserPosi)
        self.__key = 0
        ret = self.Gamepad_Cheak() # 任务是重置，消除，找到目前位置
        if ret == False:
            print ("False")
            return False
        # self.Printself()
        # print (self.__Score)
        return True
        
    def Gamepad_Cheak(self):

        User_posi = self.find_user_reset()
        if User_posi == self.__lastposi :
            self.__Score -= self.__StopPunish
        self.__lastposi = User_posi

        self.Generate_new() 
        
        self.cheak_clean_Board()

        #判断死亡 ：
        if self.Game_ifDead(User_posi) == True:
            return False

        return True

    def Generate_new(self):
        while True:
            i = random.randrange(0,5,1)
            j = random.randrange(0,5,1)
            ifbig = random.randrange(0,4,1)
            
            if ifbig != 0:
                New_BlocK = Game_elements(Game_elements.Wall)
            else:
                New_BlocK = Game_elements(Game_elements.GreatWall)
            

            
            New_Block_posi : list = [i,j]
            temp = self.Get_whatinPosi(New_Block_posi)

            if temp.name == "Air" or temp.name == "Points":
                self.__GamePad[i][j] = New_BlocK
                break
            else:
                continue

    def find_user_reset(self):
        User_posi : list = []
        #寻找user位置 
        for i in range(self.__Sizecol):
            for j in range(self.__Sizerow):
                if self.__GamePad[i][j].id  == 1 :#user
                    User_posi = [i,j]
                if self.__GamePad[i][j].MoveAble == True:
                    self.__GamePad[i][j].tempMoveable = True
                
        self.__UserPosi = User_posi
        return User_posi

    def cheak_clean_Board(self):
        row_for_clean : list = []
        col_for_clean : list = []
        
        #标记清理行
        for i in range(self.__Sizecol):
            count : int = 0
            for j in range(self.__Sizerow):
                if self.__GamePad[i][j].name == "Wall" \
                or self.__GamePad[i][j].name == "GreatWall":
                    count += 1
            if count == 5:
                row_for_clean.append(i)
            count = 0

        #标记清理列
        for i in range(self.__Sizerow):
            count : int = 0
            for j in range(self.__Sizecol):
                if self.__GamePad[j][i].name == "Wall" \
                or self.__GamePad[j][i].name == "GreatWall":
                    count += 1
            if count == 5:
                col_for_clean.append(i)
            count = 0

        for i in row_for_clean:
            for j in range(self.__Sizerow):
                self.__GamePad[i][j], self.__Score = self.__GamePad[i][j].Clean(self.__Score)

        for i in col_for_clean:
            for j in range(self.__Sizecol):
                self.__GamePad[j][i], self.__Score = self.__GamePad[j][i].Clean(self.__Score)

    def Game_ifDead(self, User_posi : list ):
        untop = True
        undown = True
        unleft = True
        unright = True
        if User_posi[0] == 0:
            untop = True
        else :
            posi = User_posi[0]
            while posi != 0:
                temp : Game_elements = self.__GamePad[posi - 1][User_posi[1]]
                if temp.MoveAble == False:
                    untop = True
                    break
                elif temp.ThroughAble == True:
                    untop = False
                    break
                else :
                    posi -= 1

        if User_posi[0] == self.__Sizecol-1:
            undown = True
        else :
            posi = User_posi[0]
            while posi != self.__Sizecol-1:
                temp : Game_elements = self.__GamePad[posi + 1][User_posi[1]]
                if temp.MoveAble == False:
                    undown = True
                    break
                elif temp.ThroughAble == True:
                    undown = False
                    break
                else:
                    posi += 1
            

        if User_posi[1] == 0:
            unleft = True
        else :
            posi = User_posi[1]
            while posi != 0:
                temp : Game_elements = self.__GamePad[User_posi[0]][posi-1]
                if temp.MoveAble == False:
                    unleft = True
                    break
                elif temp.ThroughAble == True:
                    unleft = False
                    break
                else:
                    posi -= 1
            

        if User_posi[1] == self.__Sizerow-1:
            unright = True
        else :
            posi = User_posi[1]
            while posi != self.__Sizerow-1:
                temp : Game_elements = self.__GamePad[User_posi[0]][posi+1]
                if temp.MoveAble == False:
                    unright = True
                    break
                elif temp.ThroughAble == True:
                    unright = False
                    break
                else:
                    posi += 1
        
            

        if untop == True and undown == True and unleft == True and unright == True:
            # print ("fail")
            # self.Printself()
            return True
        else :
            return False

    def Game_input(self, key):
        # if key == 'w':
        #     key = 1
        # if key == 'a':
        #     key = 3
        # if key == 's':
        #     key = 2
        # if key == 'd':
        #     key = 4
        if key == self.__lastkey:
            self.__Score -= 2
            return False
        
        self.__key = key
        self.__lastkey = key
        # self.__key = key
        return 

    def move_posi(self, ProcessPosi) -> list:
        # ProcessPosi = self.__UserPosi
        if self.__key == 0:
            return 
        if self.__key == 1:
            while True:
                if ProcessPosi[0] == 0: # 到头了
                    # self.__key = 0
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                forward = self.Get_whatinPosi([ProcessPosi[0]-1,ProcessPosi[1]])
                if forward.MoveAble == False or forward.tempMoveable == False:
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                if forward.ThroughAble == True:
                    self.replace(ProcessPosi, [ProcessPosi[0]-1,ProcessPosi[1]])
                    self.move_posi([ProcessPosi[0]-1,ProcessPosi[1]])
                    return
                else:
                    self.move_posi([ProcessPosi[0]-1,ProcessPosi[1]])
        if self.__key == 2:
            while True:
                if ProcessPosi[0] == 4: # 到头了
                    # self.__key = 0
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                forward = self.Get_whatinPosi([ProcessPosi[0]+1,ProcessPosi[1]])
                if forward.MoveAble == False or forward.tempMoveable == False:
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                if forward.ThroughAble == True:
                    self.replace(ProcessPosi, [ProcessPosi[0]+1,ProcessPosi[1]])
                    self.move_posi([ProcessPosi[0]+1,ProcessPosi[1]])
                    return
                else:
                    self.move_posi([ProcessPosi[0]+1,ProcessPosi[1]])
        if self.__key == 3:
            while True:
                if ProcessPosi[1] == 0: # 到头了
                    # self.__key = 0
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                forward = self.Get_whatinPosi([ProcessPosi[0],ProcessPosi[1]-1])
                if forward.MoveAble == False or forward.tempMoveable == False:
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                if forward.ThroughAble == True:
                    self.replace(ProcessPosi, [ProcessPosi[0],ProcessPosi[1]-1])
                    self.move_posi([ProcessPosi[0],ProcessPosi[1]-1])
                    return
                else:
                    self.move_posi([ProcessPosi[0],ProcessPosi[1]-1])
        if self.__key == 4:
            while True:
                if ProcessPosi[1] == 4: # 到头了
                    # self.__key = 0
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                forward = self.Get_whatinPosi([ProcessPosi[0],ProcessPosi[1]+1])
                if forward.MoveAble == False or forward.tempMoveable == False:
                    self.__GamePad[ProcessPosi[0]][ProcessPosi[1]].tempMoveable = False
                    return
                if forward.ThroughAble == True:
                    self.replace(ProcessPosi, [ProcessPosi[0],ProcessPosi[1]+1])
                    self.move_posi([ProcessPosi[0],ProcessPosi[1]+1])
                    return
                else:
                    self.move_posi([ProcessPosi[0],ProcessPosi[1]+1])
             
    def replace(self, posi_from : list , posi_to : list):
        temp = self.Get_whatinPosi(posi_to)
        if temp.name == "Points":
            self.__GamePad[posi_to[0]][posi_to[1]], self.__Score = temp.Clean(self.__Score)
            temp = self.Get_whatinPosi(posi_to)
        

        self.__GamePad[posi_to[0]][posi_to[1]] = self.Get_whatinPosi(posi_from)
        self.__GamePad[posi_from[0]][posi_from[1]] = temp
        return 

    def Get_whatinPosi(self, posi : list) -> Game_elements:
        return self.__GamePad[posi[0]][posi[1]]
    
    def Printself(self):
        for i in range(self.__Sizecol):
            for j in range(self.__Sizerow):
                print("{:<10}".format(self.__GamePad[i][j].name), end=" ")
            print ("")

    def Output(self):
        return self.__GamePad
        
    def get_score(self):
        return self.__Score
    
    def OutputTenser(self) -> list:
        ret : list = []
        for i in range(self.__Sizecol):
            for j in range(self.__Sizerow):
                ret.append(self.__GamePad[i][j].id)
        return ret
    
    def Game_for_AI(self, input : int):
        if self.__lastkey == input:
            self.__Score -= self.__samekeyPunish
        self.__lastkey = input
        self.__key = input
        self.move_posi(self.__UserPosi)
        self.__key = 0
        iflive = self.Gamepad_Cheak() # 任务是重置，消除，找到目前位置
        return iflive, self.__Score, self.OutputTenser()
        

# game1 = Game()
# game1.Printself()
# while True:
#     if game1.Game_logic() == False:
#         break
# # game1.move_posi([4,2])
# game1.
# game1.Printself()
# game1.move_posi([1,1])