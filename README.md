# Naive implementation of Procedural Voronoi Foams for Additive Manufacturing

#### Noli Manzoni, Nicky Zimmerman

## Execution

To execute the code please first install the following Python 3.7 packages:

- joblib
- numpy
- open3d
- pymesh (only for voxelization)

Then to create a simple foam on a 1x1x1 cube you can execute `tests.py` (it takes around 2 minutes on a MacBook pro 2018). If you want to gerate more complex foams you can change the parameters and load the correct voxelize shape (see the models directory). Moreover, you need to change the neighborhood limit parameter in the `subdivision.py` file.

To generated random seeds only you can execute `seeds_generation.py`

To voxelize a mesh you can execute `voxelization.py`

## Results
All the results are available under the directory `results` (the corresponding input meshes are located under `models`)

![results](https://github.com/raikilon/voronoi-foams/blob/master/results/results.gif)



