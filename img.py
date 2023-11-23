import gamelogic 
import torch
import time
import os

# import tenserokay

class Controller(torch.nn.Module):
    def __init__(self):
        super(Controller, self).__init__()
        self.fc1 = torch.nn.Linear(26, 100) #输入层
        self.fc2 = torch.nn.Linear(100, 100) #中间层
        self.fc3 = torch.nn.Linear(100, 20) #中间层
        self.fc4 = torch.nn.Linear(20, 4)  #输出层
        self.score : int = 0
        # self.to(device)
    
    #前向传播
    def forward(self, x : torch.Tensor):
        # x = x.to(device)
        x = torch.nn.functional.relu(self.fc1(x)) 
        x = torch.nn.functional.relu(self.fc2(x))
        x = torch.nn.functional.relu(self.fc3(x))
        x = self.fc4(x)
        return x # 进行输出归一化
    


class Window:
    import tkinter
    Message=0
    state = True
    
    def __init__(self, name = "Game", Realgame : gamelogic.Game = None, floder = 'saved_models'):
        self.waittime = 300
        self.winRoot = self.tkinter.Tk()
        self.winRoot.title('Ai Teaches You Play Game')
        self.winRoot.geometry('600x600')
        self.buttons = self.tkinter.Frame()
        if Realgame == None:
            self.game = gamelogic.Game()
        else :
            self.game = Realgame
        self.folder = floder
        self.lastKey = 0
            # self.ai = tenserokay.Ai(RealGame=Realgame)
            
        def btn1Messctl():
            self.Message = 1
            self.Buttons_ctrl()
            
        def btn2Messctl():
            self.Message = 3
            self.Buttons_ctrl()

        def btn3Messctl():
            self.Message = 4
            self.Buttons_ctrl()

        def btn4Messctl():
            self.Message = 2
            self.Buttons_ctrl()

        self.scorepad = self.tkinter.Label(self.winRoot, text="0")
        self.board = self.tkinter.Canvas(self.winRoot, bg = 'white', width=500, height=500)
        self.btn1 = self.tkinter.Button(self.buttons,text=' on  ',bg='white',command = btn1Messctl)
        self.btn2 = self.tkinter.Button(self.buttons,text='left ',bg='white',command = btn2Messctl)
        self.btn3 = self.tkinter.Button(self.buttons,text='right',bg='white',command = btn3Messctl)
        self.btn4 = self.tkinter.Button(self.buttons,text='under',bg='white',command = btn4Messctl)

        self.btn1.grid(row=0,column=1)
        self.btn2.grid(row=1,column=0)
        self.btn4.grid(row=1,column=1)
        self.btn3.grid(row=1,column=2)
        self.scorepad.pack(side = self.tkinter.TOP, anchor=self.tkinter.E)
        self.buttons.pack(side=self.tkinter.BOTTOM, anchor=self.tkinter.E)
        self.board.pack(side=self.tkinter.TOP, anchor=self.tkinter.W)
        self.Generate_img(self.game.Output())


    def windowLoop(self):
        def additional_code():
            # model = Controller()
            
            game_output_pad = self.game.OutputTenser()

            game_output_pad.append(self.lastKey)
 
            game_output_pad_tensor = torch.tensor(game_output_pad,dtype=torch.float32).view(-1)
            output_direction = model.forward(game_output_pad_tensor)

            # print(output_direction)
            output_direction_int = torch.argmax(output_direction).item() + 1
            iflive, self.score, game_output_pad = self.game.Game_for_AI(output_direction_int)

            self.Generate_img(self.game.Output())
            self.scorepad.config(text=str(self.game.get_score()))
            self.lastKey = output_direction_int


            if iflive == False:
                del self.game
                self.game = gamelogic.Game()
                self.winRoot.after(self.waittime+1000, additional_code)
                self.lastKey = 1
                return
            self.winRoot.after(self.waittime, additional_code)


        self.winRoot.after(self.waittime, additional_code)
        load_path = os.path.join('saved_models', f'model_{2}.pth')
        model = Controller()
        model.load_state_dict(torch.load(load_path))
        for param in model.parameters():
            print(param)
                
        self.winRoot.mainloop()

    def Generate_img(self, board:list[list[gamelogic.Game_elements]]):
        
        boundary_size = 5
        point_size = 40

        block_size = 100 

        self.board.create_rectangle(1,1,500,500,fill="white")
        for i in range(len(board)):
            for j in range (len(board[i])):
                if board[j][i].name  == "Wall":
                    self.board.create_rectangle(block_size*i+boundary_size,block_size*j+boundary_size,\
                                                block_size*(i+1)-boundary_size,block_size*(j+1)-boundary_size,fill="grey")
                if board[j][i].name  == "User": 
                    self.board.create_oval(block_size*i+boundary_size,block_size*j+boundary_size,\
                                                block_size*(i+1)-boundary_size,block_size*(j+1)-boundary_size,fill="green")
                if board[j][i].name  == "Points": 
                    self.board.create_oval(block_size*i+point_size,block_size*j+point_size,\
                                                block_size*(i+1)-point_size,block_size*(j+1)-point_size,fill="red")
                if board[j][i].name  == "GreatWall":
                    self.board.create_rectangle(block_size*i+boundary_size,block_size*j+boundary_size,\
                                                block_size*(i+1)-boundary_size,block_size*(j+1)-boundary_size,fill="black")
                    
        self.scorepad.config(text=str(self.game.get_score()))
                    
        return 

    def Buttons_ctrl(self):
        if self.state == True:
            if self.game.Game_input(self.Message) == False:
                print ("don't same")
            else:
                self.state = self.game.Game_logic()
            self.Generate_img(self.game.Output())
        return
    
def receive_data():
    
    pass
        
realgame = gamelogic.Game()
game = Window(Realgame=realgame)


game.windowLoop()



# print ("okay")


