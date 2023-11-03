import torch
import torch.nn.functional as F
from pylon.constraint import constraint
from pylon.brute_force_solver import SatisfactionBruteForceSolver


class Net(torch.nn.Module):
    def __init__(self, w=None):
        super().__init__()
        if w is not None:
            self.w = torch.nn.Parameter(torch.tensor(w).float().view(6, 1))
        else:
            self.w = torch.nn.Parameter(torch.rand(6, 1))

    def forward(self, x):
        return torch.matmul(self.w, x).view(3, 2)


# Our constraint function accepts a decoding tensor of
# shape (batch_size, ...) and is expected to return
# a tensor fo shape (batch_size, )
def xor(y):
    return (y[:, 0] != y[:, 1]) and (y[:, 1] == y[:, 2])


if __name__ == "__main__":
    # Create network and optimizer
    net = Net(w=[[-1, 1, 0, 0, 0, 0]])
    opt = torch.optim.SGD(net.parameters(), lr=0.1)

    # Input and label
    x = torch.tensor([1.])
    y = torch.tensor([0, 0, 1])

    xor_cons = constraint(xor, SatisfactionBruteForceSolver())

    # training loop
    y0, y1, y2 = [], [], []
    plot_loss = []
    for _ in range(500):
        opt.zero_grad()
        y_logit = net(x)
        loss = F.cross_entropy(y_logit[2:], y[2:])
        # Pylon expect tensors of shape (batch_size, ...)
        loss += xor_cons(y_logit.unsqueeze(0))
        loss.backward()
        y_prob = torch.softmax(y_logit, dim=-1)
        y0.append(y_prob[0, 1].data)
        y1.append(y_prob[1, 1].data)
        y2.append(y_prob[2, 1].data)
        plot_loss.append(loss.data)
        opt.step()



    import matplotlib.pyplot as plt
    plt.plot(y0, label='y0')
    plt.plot(y1, label='y1')
    plt.plot(y2, label='y2')
    plt.plot(plot_loss, label='loss')
    plt.legend()
    plt.show()
