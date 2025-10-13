import optuna

import numpy as np

import matplotlib.pyplot as plt


def my_function(x: float, y: float) -> float:
    assert 0.0 <= x <= 1.0
    assert 0.0 <= y <= 1.0
    return (
        0.9
        * np.exp(-((x - 0.2) ** 2 + (y - 0.3) ** 2) / 0.04)  # wide peak near (0.2,0.3)
        + 0.9
        * np.exp(-((x - 0.7) ** 2 + (y - 0.8) ** 2) / 0.04)  # wide peak near (0.7,0.8)
        + 0.9
        * np.exp(
            -((x - 0.8) ** 2 + (y - 0.2) ** 2) / 0.06
        )  # narrow peak near (0.8,0.2)
        + 1.0
        * np.exp(
            -((x - 0.35) ** 2 + (y - 0.75) ** 2) / 0.01
        )  # narrow peak near (0.35,0.75)
    )


def objective(trial: optuna.Trial) -> float:
    x = trial.suggest_float("x", 0.0, 1.0)
    y = trial.suggest_float("y", 0.0, 1.0)
    return my_function(x, y)


if __name__ == "__main__":
    # quick 2d plot of the objective function
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    for x, y in zip(X.flatten(), Y.flatten()):
        Z[np.where((X == x) & (Y == y))] = my_function(x, y)
    plt.style.use("bmh")
    plt.contourf(X, Y, Z, levels=10, cmap="viridis", alpha=0.6)
    plt.colorbar()

    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.QMCSampler(),
    )
    study.optimize(objective, n_trials=128, timeout=10, n_jobs=1)

    optimization_path = []
    for t in study.trials:
        x = t.params["x"]
        y = t.params["y"]
        z = t.value
        optimization_path.append((x, y, z))
    optimization_path = np.array(optimization_path)
    plt.scatter(
        optimization_path[:, 0],
        optimization_path[:, 1],
        c="r",
        s=5,
        label="Sampled Points",
    )
    plt.plot(
        study.best_params["x"],
        study.best_params["y"],
        "g*",
        markersize=15,
        label="Best Parameter",
    )
    plt.legend()

    print("Best trial:")
    t = study.best_trial
    print(f"  Value: {t.value}")
    print("  Params: ")
    for key, value in t.params.items():
        print(f"    {key}: {value}")

    plt.show()
