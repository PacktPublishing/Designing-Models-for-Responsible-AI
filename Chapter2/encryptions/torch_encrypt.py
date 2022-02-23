import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import syft as sy
# Set everything up
hook = sy.TorchHook(torch)

alice = sy.VirtualWorker(id="alice", hook=hook)
bob = sy.VirtualWorker(id="bob", hook=hook)
james = sy.VirtualWorker(id="james", hook=hook)


# A Toy Dataset
data = torch.tensor([[0,0],[0,1],[1,0],[1,1.]])
target = torch.tensor([[0],[0],[1],[1.]])

# A Toy Model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, 2)
        self.fc2 = nn.Linear(2, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x
model = Net()



# We encode everything
data = data.fix_precision().share(bob, alice, crypto_provider=james, requires_grad=True)
target = target.fix_precision().share(bob, alice, crypto_provider=james, requires_grad=True)
model = model.fix_precision().share(bob, alice, crypto_provider=james, requires_grad=True)
print(data)


opt = optim.SGD(params=model.parameters(),lr=0.1).fix_precision()

for iter in range(20):
    # 1) erase previous gradients (if they exist)
    opt.zero_grad()

    # 2) make a prediction
    pred = model(data)

    # 3) calculate how much we missed
    loss = ((pred - target)**2).sum()

    # 4) figure out which weights caused us to miss
    loss.backward()

    # 5) change those weights
    opt.step()

    # 6) print our progress
    print(loss.get().float_precision())