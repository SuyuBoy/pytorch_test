import torch
import torchvision.models as models
import os

# 创建一个简单的示例神经网络，这里使用的是预训练的ResNet18模型
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
    

# models = Controller()
load_path = os.path.join('saved_models', f'model_{2}.pth')
model = Controller()
model.load_state_dict(torch.load(load_path))
# 定义输入示例
dummy_input = torch.randn(1,26)

# 指定保存的文件名
onnx_filename = "model.onnx"

# 使用torch.onnx.export将模型保存为ONNX格式
torch.onnx.export(model, dummy_input, onnx_filename, verbose=True)
