from shapely import Polygon
import shapely.plotting
from matplotlib import pyplot as plt

if __name__ == "__main__":
    # Defining a square with some points in a line that don't add information apart form the corners.
    sq = Polygon(
        [
            [0, 0],
            [0, 1],
            [0, 2],
            [0, 3],
            [0, 4],
            [0, 5],
            [5, 5],
            [5, 0],
        ]
    )

    # This should still remove the useless points in a line
    sq_smpl_0 = sq.simplify(tolerance=0.0)
    assert sq != sq_smpl_0

    # This should do nothing different than simply removing *the useless points in a line*
    sq_smpl_5 = sq.simplify(tolerance=0.5)
    assert sq_smpl_0 == sq_smpl_5

    # This should also do nothing different than simply removing *the useless points in a line*
    sq_smpl_15 = sq.simplify(tolerance=1.5)
    assert sq_smpl_0 == sq_smpl_15

    f, axs = plt.subplots(2, 2)
    axs = axs.flatten()
    for ax, p_str in zip(axs, ["sq", "sq_smpl_0", "sq_smpl_5", "sq_smpl_15"]):
        p = locals()[p_str]
        ax.set_title(p_str)
        shapely.plotting.plot_polygon(p, ax)

    # Looking at something to simplify geometrically
    notch = Polygon(
        [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 2],
            [0, 2],
            [0, 5],
            [5, 5],
            [5, 0],
        ]
    )

    # This should not change anything because the feature is larger
    notch_smpl_0 = notch.simplify(tolerance=0.0)
    assert notch == notch_smpl_0

    # This should *still* not change anything because the feature is larger
    notch_smpl_5 = notch.simplify(tolerance=0.5)
    assert notch_smpl_0 == notch_smpl_5

    # This *should* remove the feature because it has edges of lenght 1
    notch_smpl_15 = notch.simplify(tolerance=1.5)
    assert notch_smpl_0 != notch_smpl_15

    f, axs = plt.subplots(2, 2)
    axs = axs.flatten()
    for ax, p_str in zip(
        axs, ["notch", "notch_smpl_0", "notch_smpl_5", "notch_smpl_15"]
    ):
        p = locals()[p_str]
        ax.set_title(p_str)
        shapely.plotting.plot_polygon(p, ax)

    plt.show()
