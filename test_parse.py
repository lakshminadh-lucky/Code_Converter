import sys
from parsers.c_parser import parse_c
from ir.ir_builder import build_ir
from generators.python_generator import generate_python

c_code = """
#include <stdbool.h> 
#include <stdio.h>   

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void bubbleSort(int arr[], int n) {
    int i, j;
    bool swapped;
    for (i = 0; i < n - 1; i++) {
        swapped = false;
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
}

void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Unsorted array: ");
    printArray(arr, n);

    bubbleSort(arr, n);

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}
"""
try:
    nodes = parse_c(c_code)
    ir = build_ir(nodes, "c")
    from generators.java_generator import generate_java
    from generators.c_generator import generate_c
    from generators.cpp_generator import generate_cpp
    from flowchart import generate_flowchart
    from utils import explain_ir_step_by_step
    
    print("JAVA:")
    print(generate_java(ir))
    print("---")
    print("C:")
    print(generate_c(ir))
    print("---")
    print("CPP:")
    print(generate_cpp(ir))
    print("---")
    print("FLOWCHART DOT:")
    print(generate_flowchart(ir).source)
    print("---")
    print("STEPS:")
    print(explain_ir_step_by_step(ir))
except Exception as e:
    import traceback
    traceback.print_exc()
