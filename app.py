
import streamlit as st

from parsers.python_parser import parse_python
from parsers.java_parser import parse_java
from parsers.c_parser import parse_c
from parsers.cpp_parser import parse_cpp

from ir.ir_builder import build_ir

from generators.python_generator import generate_python
from generators.java_generator import generate_java
from generators.c_generator import generate_c
from generators.cpp_generator import generate_cpp

from flowchart import generate_flowchart
from utils import explain_ir_step_by_step

st.set_page_config(page_title="Universal Code Converter", layout="wide")

st.title("Universal Programming Language Converter")

source_lang = st.sidebar.selectbox(
    "Source Language",
    ["python","java","c","cpp"]
)

target_lang = st.sidebar.selectbox(
    "Target Language",
    ["python","java","c","cpp"]
)

code = st.text_area("Enter Source Code", height=320)

parsed=None
ir=None

if code.strip():
    try:
        if source_lang=="python":
            parsed=parse_python(code)
        elif source_lang=="java":
            parsed=parse_java(code)
        elif source_lang=="c":
            parsed=parse_c(code)
        elif source_lang=="cpp":
            parsed=parse_cpp(code)

        ir=build_ir(parsed,source_lang)

    except Exception as e:
        st.error(f"Parsing Error: {e}")
from runner import run_code

col1, col2, col3, col4 = st.columns(4)

convert_btn = col1.button("Convert Code")
explain_btn = col2.button("Step-by-Step")
flow_btn = col3.button("Show Flowchart")
execute_btn = col4.button("Execute Code")

if convert_btn and ir:
    if target_lang=="python":
        result=generate_python(ir)
    elif target_lang=="java":
        result=generate_java(ir)
    elif target_lang=="c":
        result=generate_c(ir)
    elif target_lang=="cpp":
        result=generate_cpp(ir)

    st.subheader("Converted Code")
    st.code(result, language=target_lang)

if explain_btn and ir:
    st.subheader("Step-by-Step Explanation")
    steps=explain_ir_step_by_step(ir)
    for i,s in enumerate(steps,1):
        st.write(f"{i}. {s}")
if flow_btn and ir:
    st.subheader("Flowchart")
    chart=generate_flowchart(ir)
    st.graphviz_chart(chart)

if execute_btn and ir:
    if target_lang=="python":
        result=generate_python(ir)
    elif target_lang=="java":
        result=generate_java(ir)
    elif target_lang=="c":
        result=generate_c(ir)
    elif target_lang=="cpp":
        result=generate_cpp(ir)

    st.subheader("Execution Output")
    out_col1, out_col2 = st.columns(2)
    with out_col1:
        st.markdown(f"**Source ({source_lang}) Output**")
        source_out = run_code(code, source_lang)
        st.code(source_out, language="text")
    with out_col2:
        st.markdown(f"**Converted ({target_lang}) Output**")
        target_out = run_code(result, target_lang)
        st.code(target_out, language="text")
