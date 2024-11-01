import argparse
import os.path
import subprocess
from datetime import datetime

def exec_clang_tidy(file_list, op_dir, inc_path, c_cpp):
    for input_file in file_list:
        if os.path.exists(input_file):
            output_file = os.path.join(op_dir, input_file.split("/")[-1].split(".")[0] + ".yaml")
            # clang-tidy file --checks=* -- -I{include_path} -std=c11/c++11
            # optional: --header-filter=.* --system-headers
            command = ["clang-tidy", input_file, f"-export-fixes={output_file}", "--checks=*", "--", f"-I{inc_path}",
                       f"-std={c_cpp}11", ""]
            print(f"Executing: {command}")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Error:{result.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="This scripts automate the static analysis using clang-tidy")
    parser.add_argument("-p", "--path", required=True, help="Path of the C/C++ source code: ")
    parser.add_argument("-i", "--include", required=True, help="Include path:provide the path of testcasesupport "
                                                      "e.g. juliet/C/testcasesupport")
    parser.add_argument("-o", "--output", required=False, help="Path to store the output")
    args = parser.parse_args()
    input_path = args.path
    if not os.path.exists(input_path):
        print(f"Invalid path{input_path}")
        exit(-1)
    output_dir = args.output if args.output is not None and os.path.exists(args.output) else "./Output"
    output_dir = output_dir + datetime.now().strftime("_%m-%d-%Y_%H_%M_%S")
    os.mkdir(output_dir)

    # Get the list of files to run
    res = subprocess.run(["find", input_path, "-type", "f", "-name", "*.c"], capture_output=True, text=True)
    c_file_list = res.stdout.split("\n")
    exec_clang_tidy(c_file_list,output_dir,args.include,"c")
    res = subprocess.run(["find", input_path, "-type", "f", "-name", "*.cpp"], capture_output=True, text=True)
    cpp_file_list = res.stdout.split("\n")
    exec_clang_tidy(cpp_file_list, output_dir, args.include, "c++")
    print(f"Please find the output in ${output_dir}.")