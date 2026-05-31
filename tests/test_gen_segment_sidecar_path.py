from masm2c.gen import Gen


def test_segment_sidecar_path_replaces_uppercase_asm_suffix() -> None:
    assert Gen.segment_sidecar_path('/tmp/CGA_STUB.ASM') == '/tmp/CGA_STUB.seg'


def test_segment_sidecar_path_replaces_mixed_case_lst_suffix() -> None:
    assert Gen.segment_sidecar_path('/tmp/FILE.LsT') == '/tmp/FILE.seg'


def test_segment_sidecar_path_appends_seg_for_other_extensions() -> None:
    assert Gen.segment_sidecar_path('/tmp/blob.bin') == '/tmp/blob.bin.seg'
