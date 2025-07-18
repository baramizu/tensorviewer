import numpy as np

np.save("test_data_2d.npy", np.random.rand(9, 10))
np.save("test_data_3d.npy", np.random.rand(9, 10, 11))
np.save("test_data_4d.npy", np.random.rand(9, 10, 11, 12))

data_dict = {
    "2D Data": np.load("test_data_2d.npy"),
    "3D Data": np.load("test_data_3d.npy"),
    "4D Data": np.load("test_data_4d.npy"),
}

np.savez("test_data.npz", **data_dict)