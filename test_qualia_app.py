import numpy as np

from qualia_app import fuse_architectures


def test_fuse_architectures_with_tensor():
    tensor = np.random.rand(1, 4, 4, 4, 1)
    result = fuse_architectures("אמת והשגה מופשטת", ["שכל", "אור"], tensor)

    assert "compilation" in result
    assert "tensor" in result
    assert 0.0 <= result["fused_score"] <= 1.0
    assert result["tensor"]["shape"] == (1, 2, 2, 2)
