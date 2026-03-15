from runner import run_code

c_code = """
#include <stdio.h>
int main() {
    printf("Hello from C Engine!\\n");
    return 0;
}
"""

python_code = """
print("Hello from Python Engine!")
"""

java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java Engine!");
    }
}
"""

cpp_code = """
#include <iostream>
using namespace std;
int main() {
    cout << "Hello from C++ Engine!" << endl;
    return 0;
}
"""

print("C:", run_code(c_code, "c").strip())
print("Python:", run_code(python_code, "python").strip())
print("Java:", run_code(java_code, "java").strip())
print("C++:", run_code(cpp_code, "cpp").strip())
