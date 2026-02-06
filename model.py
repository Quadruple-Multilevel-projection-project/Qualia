import numpy as np


def cnn_5d_to_3d(input_data: np.ndarray) -> np.ndarray:
    """
    Reduce 5D tensor (batch, depth, height, width, channels) into a 3D signal.

    This is a lightweight, dependency-free approximation that mimics a
    convolution + pooling style reduction without requiring TensorFlow.
    """
    if input_data.ndim != 5:
        raise ValueError("input_data must be a 5D tensor")

    # Simple reduction: mean over channels, then average-pool by factor 2.
    reduced = input_data.mean(axis=-1)
    depth, height, width = reduced.shape[1:]
    trimmed = reduced[
        :,
        : depth - (depth % 2),
        : height - (height % 2),
        : width - (width % 2),
    ]
    depth, height, width = trimmed.shape[1:]
    pooled = trimmed.reshape(
        reduced.shape[0],
        depth // 2,
        2,
        height // 2,
        2,
        width // 2,
        2,
    ).mean(axis=(2, 4, 6))

    return pooled
