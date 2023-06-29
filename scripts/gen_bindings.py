import os
import subprocess

source_dir = os.path.join("native", "src")
cur_dir = os.getcwd()
base_path = os.path.join(cur_dir, source_dir)

# Get files in source_dir
files = os.listdir(source_dir)

# Filter bridge files
generated_files = [f for f in files if "generated" in f]
bridge_files = [f for f in files if "generated" not in f and f != "lib.rs"]

for f in generated_files:
    os.remove(os.path.join(source_dir, f))

for f in os.listdir(os.path.join(cur_dir, "lib")):
    if "bridge_generated" in f:
        os.remove(os.path.join(cur_dir, "lib", f))

ffi_file_path = os.path.join(cur_dir, "lib", "ffi.dart")
if(os.path.exists(ffi_file_path)):
    os.remove(ffi_file_path)

# Generate bindings
rust_input = ""
dart_output = ""
class_names = ""
rust_output = ""

ffi_imports = "import 'dart:ffi';\nimport 'dart:io' as io;\n\n"
ffi_contents = """
const _base = 'native';
final _dylibPath = io.Platform.isWindows ? '$_base.dll' : 'lib$_base.so';
final _dylib = io.Platform.isIOS || io.Platform.isMacOS
    ? DynamicLibrary.executable()
    : DynamicLibrary.open(_dylibPath);

"""

for f in bridge_files:
    # Get class name
    class_name = (f.split(".")[0]).title().replace("_", "")
    class_name_camel = class_name[0].lower() + class_name[1:]
    class_names += ' ' + class_name

    # Generate rust input
    rust_input += ' ' + os.path.join(base_path, f)

    # Generate dart output
    dart_filename = 'bridge_generated_' + class_name + ".dart"
    dart_output += ' ' +  os.path.join(cur_dir, "lib", dart_filename)

    # Generate rust output
    rust_output += ' ' + os.path.join(cur_dir, "native", "src", 'generated_' + class_name + '.rs')

    # Generate ffi file
    ffi_imports += f'import "{dart_filename}";\n'
    ffi_contents += f'final {class_name} {class_name_camel} = {class_name}Impl(_dylib);\n'

separator = ' '
command = f'flutter_rust_bridge_codegen {separator}--rust-input{rust_input} {separator}--dart-output{dart_output} {separator}--rust-output{rust_output} {separator}--class-name{class_names}'
print('Command: \n', command)
subprocess.run(command, shell=True)

ffi_file = ffi_imports + ffi_contents
f = open(ffi_file_path, "w")
f.write(ffi_file)
f.close()