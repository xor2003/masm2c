import jsonpickle

from masm2c import op
from masm2c.cpp import Cpp
from masm2c.parser import Parser
from masm2c.proc import Proc


RT_DATA_OFFSET = 1 << 0
RT_CODE_OFFSET = 1 << 1
RT_FAR_POINTER = 1 << 4


def _parser_with_data_symbols() -> Parser:
    parser = Parser([])
    parser.segments["_data"] = op.Segment("_data", 0x2000)
    parser.symbols.set_global("_data", op.var(0, 0, name="_data", issegment=True))
    parser.symbols.set_global("target", op.var(1, 0x20, name="target", segment="_data", elements=4))
    parser.symbols.set_global("target2", op.var(1, 0x30, name="target2", segment="_data", elements=4))
    return parser


def test_runtime_pointer_evidence_renders_near_data_offset() -> None:
    parser = _parser_with_data_symbols()
    parser.runtime_pointer_meta = {
        0x2010: [
            {
                "SourceAddr": "0x2010",
                "TargetAddr": "0x2020",
                "Size": 2,
                "Value": 0x20,
                "Flags": RT_DATA_OFFSET,
                "Count": 3,
            }
        ]
    }
    data = op.Data("ptr", "dw", op.DataType.NUMBER, [0x20], 1, 2)
    data.runtime_linear_addr = 0x2010

    rendered, decl = Cpp(parser).produce_c_data_number(data)

    assert rendered == "offset(_data,target)"
    assert decl == "dw ptr"


def test_runtime_pointer_evidence_renders_far_data_offset() -> None:
    parser = _parser_with_data_symbols()
    parser.runtime_pointer_meta = {
        0x2010: [
            {
                "SourceAddr": "0x2010",
                "TargetAddr": "0x2020",
                "Size": 4,
                "Value": 0x02000020,
                "Flags": RT_FAR_POINTER,
                "Count": 1,
            }
        ]
    }
    data = op.Data("ptr", "dd", op.DataType.NUMBER, [0x02000020], 1, 4)
    data.runtime_linear_addr = 0x2010

    rendered, _decl = Cpp(parser).produce_c_data_number(data)

    assert rendered == "far_offset(_data,target)"


def test_runtime_pointer_evidence_renders_array_entries_by_source_address() -> None:
    parser = _parser_with_data_symbols()
    parser.runtime_pointer_meta = {
        0x2010: [{"TargetAddr": "0x2020", "Size": 2, "Value": 0x20, "Flags": RT_DATA_OFFSET, "Count": 1}],
        0x2012: [{"TargetAddr": "0x2030", "Size": 2, "Value": 0x30, "Flags": RT_DATA_OFFSET, "Count": 1}],
    }
    data = op.Data("table", "dw", op.DataType.ARRAY, [0x20, 0x30], 2, 4)
    data.runtime_linear_addr = 0x2010

    rendered, decl = Cpp(parser).produce_c_data_array(data)

    assert rendered == "{offset(_data,target),offset(_data,target2)}"
    assert decl == "dw table[2]"


def test_runtime_pointer_evidence_renders_code_offset_low_word() -> None:
    parser = _parser_with_data_symbols()
    proc = Proc("handler", real_seg=0x123, real_offset=0x45)
    parser.symbols.set_global("handler", proc)
    parser.runtime_pointer_meta = {
        0x2010: [
            {
                "SourceAddr": "0x2010",
                "TargetAddr": "0x1275",
                "Size": 2,
                "Value": 0x45,
                "Flags": RT_CODE_OFFSET,
                "Count": 2,
            }
        ]
    }
    data = op.Data("codeptr", "dw", op.DataType.NUMBER, [0x45], 1, 2)
    data.runtime_linear_addr = 0x2010

    rendered, _decl = Cpp(parser).produce_c_data_number(data)

    assert rendered == "(m2c::khandler & 0xffff)"


def test_parse_rt_info_loads_pointer_and_data_evidence_with_decimal_keys(tmp_path) -> None:
    runtime_json = tmp_path / "sample.json"
    runtime_json.write_text(
        jsonpickle.encode(
            {
                "Code": {},
                "Jumps": [],
                "Data": {
                    "8208": {"ValueClassMask": RT_DATA_OFFSET},
                },
                "PointerEvidence": {
                    "1": {
                        "SourceAddr": "0x2010",
                        "TargetAddr": "8208",
                        "Size": 2,
                        "Value": 0x20,
                        "Flags": RT_DATA_OFFSET,
                    },
                },
                "AccessSites": {
                    "1": {
                        "Csip": "0x1234",
                        "MinAddr": "8208",
                        "MaxAddr": "8210",
                    },
                },
            },
            unpicklable=False,
        )
    )

    parser = Parser([])
    parser.parse_rt_info(str(runtime_json.with_suffix("")))

    assert 8208 in parser.runtime_data_meta
    assert parser.runtime_pointer_meta[0x2010][0]["TargetAddr"] == "8208"
    assert parser.runtime_access_site_meta[0x1234][0]["MinAddr"] == "8208"
