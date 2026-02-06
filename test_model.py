import numpy as np
from model import cnn_5d_to_3d

def test_cnn_5d_to_3d_fixed():
    # Create sample 5D input data (batch, depth, height, width, channels)
    sample_input = np.random.rand(1, 10, 10, 10, 1)

    output = cnn_5d_to_3d(sample_input)
    assert output.shape == (1, 5, 5, 5)
