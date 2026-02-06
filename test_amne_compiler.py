from amne_compiler import AMNECompiler


def test_amne_compiler_outputs_expected_structure():
    compiler = AMNECompiler()
    result = compiler.compile("אמת והשגה מופשטת", ["שכל", "אור", "מציאות"])

    assert "metadata" in result
    assert "bytecode" in result
    assert "validation" in result
    assert len(result["metadata"]["signature"]) == 8
    assert result["bytecode"]["op"] in {"INTELLECT_FIRE", "NULL_OP"}
    assert 0.0 <= result["validation"]["telos_score"] <= 1.0
