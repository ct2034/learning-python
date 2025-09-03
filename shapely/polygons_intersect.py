from shapely import Polygon
import shapely.plotting
import shapely
from matplotlib import pyplot as plt

if __name__ == "__main__":
    # Defining two shapes to cut one with another
    dough = Polygon(
        [
            [0, 0],
            [0, 4],
            [4, 4],
            [4, 0],
        ]
    )
    cutter = Polygon(
        [
            [1, 3],
            [3, 5],
            [5, 3],
            [3, 1],
        ]
    )

    # A \ B
    dough_cut = dough - cutter
    # would also work:
    # dough_cut = shapely.difference(dough, cutter)
    
    # A ∩ B
    cookie = dough & cutter
    # would also work:
    # cookie = shapely.intersection(dough, cutter)

    f, axs = plt.subplots(2, 2)
    axs = axs.flatten()
    for ax, p_str in zip(axs, ["dough", "cutter", "dough_cut", "cookie"]):
        p = locals()[p_str]
        ax.set_title(p_str)
        ax.set_aspect(1)
        ax.set_xlim(-.5, 5.5)
        ax.set_ylim(-.5, 5.5)
        shapely.plotting.plot_polygon(p, ax)

    plt.show()
