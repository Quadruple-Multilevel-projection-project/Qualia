import pytest
import numpy as np
from model import cnn_5d_to_3d

def test_cnn_5d_to_3d_fixed():
    # Create sample 5D input data (batch, depth, height, width, channels)
    sample_input = np.random.rand(1, 10, 10, 10, 1)

    # This should now run without raising an exception
    try:
        cnn_5d_to_3d(sample_input)
    except Exception as e:
        pytest.fail(f"cnn_5d_to_3d raised an unexpected exception: {e}")
