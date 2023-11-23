import torch
import multiprocessing
import gamelogic
import random
import torch.cuda
import copy
import os


# 
device = 'cpu'
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# 控制器神经网络
class Controller(torch.nn.Module):
    def __init__(self):
        super(Controller, self).__init__()
        self.fc1 = torch.nn.Linear(26, 100).to(device) #输入层
        self.fc2 = torch.nn.Linear(100, 100).to(device) #中间层
        self.fc3 = torch.nn.Linear(100, 20).to(device) #中间层
        self.fc4 = torch.nn.Linear(20, 4).to(device)  #输出层
        self.score : int = 0
        
    
    #前向传播
    def forward(self, x : torch.Tensor):
        x = x.to(device)
        x = torch.nn.functional.relu(self.fc1(x)) 
        x = torch.nn.functional.relu(self.fc2(x))
        x = torch.nn.functional.relu(self.fc3(x))
        x = self.fc4(x)
        return x # 进行输出归一化
    
    #玩游戏
    def Play_game(self):
        game = gamelogic.Game()
        game_output_pad = game.OutputTenser()
        game_output_pad.append(1)
        iflive : bool = True 
    
        while iflive: 
            game_output_pad_tensor = torch.tensor(game_output_pad,dtype=torch.float32).view(-1)
            output_direction = self.forward(game_output_pad_tensor)
            output_direction_int = torch.argmax(output_direction).item() + 1
            iflive, self.score, game_output_pad = game.Game_for_AI(output_direction_int)
            game_output_pad.append(output_direction_int)
            # game.Printself()
            # print (torch.argmax(output_direction).item())
        del game
    
    #变异操作
    def mutate(self, mutation_rate=0.03):
        for param in self.parameters():
            # print(param.data)
            if param.requires_grad: #只有参与梯度计算的参数才需要被变异
                param.data += mutation_rate * torch.randn_like(param.data)
                # print(param.data)
        # for param in self.parameters():
        #     # print(param.data)
        #     if param.requires_grad: #只有参与梯度计算的参数才需要被变异
        #         mask = (torch.rand_like(param.data) < mutation_rate).int()
        #         param.data = mask * torch.rand_like(param.data)*mutation_rate + param.data
        #         # print (param.data)
        #         param.data = param.data
                # print(param.data)


class GA:

    def __init__(self, population : int  = 100, finaltimes : int= 100000, floder = 'saved_models', rate_of_excell = 0.70, random_of_last = 0.05) -> None:
        self.population = population
        self.nowtimes = 0
        self.load_folder = floder
        self.save_folder = floder
        self.finaltimes = finaltimes
        self.keep_rate = 0.1
        self.rate_of_excell = rate_of_excell
        self.random_of_last = random_of_last
        pass

    # 这里调整 最好的占比
    def select_parents(self, last_population : list[Controller]) -> list[Controller]:
        size = len (last_population)
        sorted_objects = sorted(last_population, key=lambda x : x.score, reverse=True)
        
        rate_of_excell = self.rate_of_excell
        random_of_last = self.random_of_last

        sorted_objects_best = sorted_objects[: int(size*rate_of_excell)] # 20%最好的
        for i in range(int(random_of_last * size)):
            sorted_objects_best.append(random.choice(sorted_objects[int(size*rate_of_excell):])) #随机找10%
        return sorted_objects_best
    
    def uniform_crossover(self, other_networks):
        # 创建子代网络
        child_network = Controller()
        size = len(other_networks)
        
        i  = j = 0

        while i == j:
            i = random.randrange(0,size,1)
            j = random.randrange(0,size,1)

        for childpara, param1, param2 in zip(child_network.parameters(),other_networks[i].parameters(), other_networks[j].parameters()):
            mask = (torch.rand_like(param1.data) < 0.5).int()
            tenser = mask * param1.data + (1 - mask) * param2.data
            childpara.data = tenser

        return child_network

    def single_point_crossover(self, other_networks : list[Controller]):
        # Get the state dictionaries of the parents
        size = len(other_networks)
        
        i  = j = 0

        while i == j:
            i = random.randrange(0,size,1)
            j = random.randrange(0,size,1)

        parent1_state_dict = other_networks[i].state_dict()
        parent2_state_dict = other_networks[j].state_dict()

        # Choose a random crossover point
        crossover_point = torch.randint(0, len(parent1_state_dict), (1,)).item()

        # Create a new state dictionary for the child
        child_state_dict = {}

        # Copy parameters from parent1 to the crossover point
        for i, (key, value) in enumerate(parent1_state_dict.items()):
            if i < crossover_point:
                child_state_dict[key] = value
            else:
                break

        # Copy parameters from parent2 after the crossover point
        for i, (key, value) in enumerate(parent2_state_dict.items()):
            if i >= crossover_point:
                child_state_dict[key] = value

        # Create a new child model and load its state dictionary
        child = Controller()
        child.load_state_dict(child_state_dict)


        return child

    def massive_play(self, children : list [Controller], result_queue):
        processes = []
        for i in range(self.population):
            process = multiprocessing.Process(target=worker_process, args=(children[i], i, result_queue))
            processes.append(process)
            # 启动线程
        for process in processes:
            process.start()

        # 等待所有线程完成
        for process in processes:
            process.join()

    def load_Chlid(self) -> list[Controller]:
        ret : list[Controller] = []
        for i in range(self.population):
            load_path = os.path.join(self.load_folder, f'model_{i}.pth')
            children = Controller()
            children.load_state_dict(torch.load(load_path))
            ret.append(children)
        return ret
    
    def copy_child(self) -> list[Controller]:
        ret : list[Controller] = []
        i = 0
        for i in range(self.population):
            load_path = os.path.join(self.load_folder, f'model_{i}.pth')
            if os.path.isfile(load_path) == False:
                break
            children = Controller()
            dict = torch.load(load_path)
            children.load_state_dict(dict)
            ret.append(children)
        for j in range(self.population - i):
            load_path = os.path.join(self.load_folder, f'model_{0}.pth')
            children = Controller()
            dict = torch.load(load_path)
            children.load_state_dict(dict)
            ret.append(children)
        return ret
    
    def CreatChildren(self) -> list[Controller]:
        ret : list[Controller] = []
        for i in range(self.population):
            children = Controller()
            ret.append(children)
        return ret
    
    def Print_each(self, parents : list [Controller]):
        for i in range(5):
            print ("times", self.nowtimes, parents[i].score)
            avg = sum(obj.score for obj in parents) / len(parents)
            avg = round(avg, 2)
        print ("avg =", avg)
        print()

    def Generate_new(self, best : list [Controller]) -> list [Controller]:
        new : list [Controller] = []
        for i in range(int(self.population*(1-self.keep_rate))):
            new.append(self.uniform_crossover(best))
            new[i].mutate()
        for i in range(int(self.population*self.keep_rate)):
            new.append(best[i])
        return new
    
    def Save_model(self, children : list [Controller]):
        # save_folder = 'saved_models'
        if self.nowtimes % 50 == 0 and self.nowtimes != 0:
            for i, model in enumerate(children):
                save_path = os.path.join(self.save_folder, f'model_{i}.pth')
                torch.save(model.state_dict(), save_path)
            

    def genetic_algorithm(self):




        pass

    def GALoop(self):
        # models = self.CreatChildren()
        models = self.copy_child()
        result_queue = multiprocessing.Queue()

        while self.finaltimes > self.nowtimes:
            # result_queue =''
            self.massive_play(models, result_queue)
            # scores = [0] * self.population
            for _ in range(self.population):
                index, score = result_queue.get()
                models[index].score = score

            parents : list[Controller] = []
            parents = self.select_parents(models)
            self.Print_each(parents)
            models = self.Generate_new(parents)
            self.Save_model(parents)
            # torch.cuda.empty_cache()
            self.nowtimes += 1
            

def worker_process(model, index, result_queue):
    model.Play_game()
    result_queue.put((index, model.score))

if __name__ == "__main__":
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # multiprocessing.set_start_method('spawn')
    # multiprocessing.resource_tracker._remove_resources()

    ai = GA(rate_of_excell= 0.70, random_of_last= 0.05)
    ai.GALoop()
