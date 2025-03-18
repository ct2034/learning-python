import tensorboard as tb
import numpy as np
from torch.utils.tensorboard import SummaryWriter
import os
from datetime import datetime

for _ in range(10):

    # Create a SummaryWriter to write data to TensorBoard
    writer = SummaryWriter(
        log_dir=os.path.join(
            os.path.dirname(__file__),
            "logs",
            datetime.now().strftime("%y-%m-%d_%H:%M:%S.%f"),
        )
    )
    n_data = np.random.randint(500, 1000)

    # Generate some example data
    x = np.linspace(0, 4 * np.pi, n_data)
    t = np.linspace(0, 1, n_data)
    y = np.sin(x)

    # Log the data to TensorBoard
    for i in range(len(x)):
        writer.add_scalar(
            tag="Sine Wave", scalar_value=y[i], global_step=i, walltime=t[i]
        )
        # writer.add_scalar("Time", t[i], i)

    # Store hyperparameters
    config = {"n_data": n_data}
    metrics = {"mean_sine_wave": np.mean(y[:200])}
    writer.add_hparams(config, metrics)

    # Close the writer
    writer.close()

# In a terminal, run
# tensorboard --logdir=logs --port=6006
