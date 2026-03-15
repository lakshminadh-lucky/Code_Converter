import subprocess
import tempfile
import os

def run_code(code_str, language):
    """
    Executes the provided code string based on its language securely using temp files.
    Returns the combined stdout and stderr as a string.
    """
    if not code_str or not code_str.strip():
        return "No code to execute."

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            if language == "python":
                file_path = os.path.join(temp_dir, "main.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code_str)
                result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=10)
                return result.stdout + result.stderr

            elif language == "c":
                file_path = os.path.join(temp_dir, "main.c")
                exec_path = os.path.join(temp_dir, "main.exe") if os.name == 'nt' else os.path.join(temp_dir, "main")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code_str)
                
                # Compile C code
                compile_res = subprocess.run(["gcc", file_path, "-o", exec_path], capture_output=True, text=True)
                if compile_res.returncode != 0:
                    return f"Compilation Error:\n{compile_res.stderr}"
                
                # Execute C code
                exec_cmd = [exec_path] if os.name == 'nt' else ["./main"]
                result = subprocess.run(exec_cmd, capture_output=True, text=True, timeout=10, cwd=temp_dir)
                return result.stdout + result.stderr

            elif language == "cpp":
                file_path = os.path.join(temp_dir, "main.cpp")
                exec_path = os.path.join(temp_dir, "main.exe") if os.name == 'nt' else os.path.join(temp_dir, "main")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code_str)

                # Compile C++ code
                compile_res = subprocess.run(["g++", file_path, "-o", exec_path], capture_output=True, text=True)
                if compile_res.returncode != 0:
                    return f"Compilation Error:\n{compile_res.stderr}"

                # Execute C++ code
                exec_cmd = [exec_path] if os.name == 'nt' else ["./main"]
                result = subprocess.run(exec_cmd, capture_output=True, text=True, timeout=10, cwd=temp_dir)
                return result.stdout + result.stderr

            elif language == "java":
                file_path = os.path.join(temp_dir, "Main.java")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code_str)

                # Compile Java code
                compile_res = subprocess.run(["javac", file_path], capture_output=True, text=True, cwd=temp_dir)
                if compile_res.returncode != 0:
                    return f"Compilation Error:\n{compile_res.stderr}"

                # Execute Java code
                result = subprocess.run(["java", "Main"], capture_output=True, text=True, timeout=10, cwd=temp_dir)
                return result.stdout + result.stderr

            else:
                return f"Execution of {language} is not supported."

        except subprocess.TimeoutExpired:
            return "Execution Error: Time Limit Exceeded (10 seconds)."
        except Exception as e:
            return f"Execution Error: {str(e)}"
