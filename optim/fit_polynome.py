import torch
import numpy as np
from matplotlib import pyplot as plt


if __name__ == "__main__":
    # ground truth
    true_poly_params = np.array([1, -2, 4, 1])
    
    def poly_fun(x, params):
        y = torch.tensor(0., dtype=float)
        deg = len(params)
        for i in range(deg):
            exponent = deg - 1
            y += params[i] * x ** exponent
        return y
    x_pl = np.linspace(-2., 2., 100)
    y_pl = np.array(list(map(
        lambda x: poly_fun(x, true_poly_params),
        x_pl)))
    plt.plot(x_pl, y_pl)

    # data
    n_smpl = 100
    xs = torch.rand(n_smpl)
    ys = torch.tensor(list(map(
        lambda x: poly_fun(x, true_poly_params),
        xs)))
    plt.plot(xs, ys, 'x')

    # model
    params_to_learn = torch.ones_like(
        torch.tensor(true_poly_params),
        requires_grad=True,
        dtype=float)

    # optimizer
    optim = torch.optim.SGD([params_to_learn], lr=0.01)

    # training
    n_epochs = 1000
    for epoch in range(n_epochs):
        optim.zero_grad()
        y_hat = torch.tensor(list(map(
            lambda x: poly_fun(x, params_to_learn),
            xs)))
        print(y_hat)
        print(ys)
        loss = torch.mean((y_hat - ys) ** 2)
        loss.requires_grad_(True)
        loss.backward()
        optim.step()
        if epoch % 100 == 0:
            print('epoch: {}, loss: {}'.format(epoch, loss.item()))

    print('true params: {}'.format(true_poly_params))
    print('learned params: {}'.format(params_to_learn))

    plt.show()