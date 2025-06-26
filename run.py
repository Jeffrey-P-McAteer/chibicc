
# Responsible for compiling stage0, then stage1 of chibicc

import subprocess
import tempfile
import shutil
import sys
import os

c_compiler_exe = next(c for c in ['cc', 'gcc', 'clang'] if shutil.which(c) is not None)
print(f'c_compiler_exe = {c_compiler_exe}')
cpp_compiler_exe = next(c for c in ['cxx', 'g++', 'clang++'] if shutil.which(c) is not None)
print(f'cpp_compiler_exe = {cpp_compiler_exe}')

# TODO looks like https://www.mustakim.info/my-blogs/how-i-learned/intel_pin 
# has some good reference material, incl. using the tools directory and just running the collage of
# make instructions to build the intel tool. Pin appears to have cmake's level of API friendlieness
print('Compiling pin-experiment-01')
subprocess.run([
    cpp_compiler_exe,
        '-o', 'pin_experiment_01.so',
        '-shared',
        '-I/opt/pin/source/include/pin', # Will differ based on Pin install details, must contain pin.h
        '-I/opt/pin/source/include/pin/gen',
        '-I/opt/pin/extras/xed-intel64/include/xed',
        '-I/opt/pin/extras/crt/include',
        '-I/opt/pin/extras/crt/include/kernel/uapi',
        '-I/opt/pin/extras/components/include',
        '-L/opt/pin/intel64/lib',
        '-lpin', '-lpintool',
        'pin-experiment-01.cpp',
], check=True)

print(f'Compiling stage 0 using a normal compiler ({shutil.which('cc')} , {shutil.which('gcc')} , {shutil.which('clang')})')
subprocess.run(['make'], check=True)

with tempfile.TemporaryDirectory() as tmp_dir:
    print(f'Placing binaries within {tmp_dir}')
    for compiler_name in ['cc', 'gcc', 'clang']:
        shutil.copy('chibicc', os.path.join(tmp_dir, compiler_name))    

    new_path = tmp_dir+':'+os.environ.get('PATH', '')
    os.environ['PATH'] = new_path

    print(f'Cleaning repo')
    subprocess.run(['make', 'clean'], check=True)

    print(f'Compiling stage 1 using a chibicc compiler ({shutil.which('cc')} , {shutil.which('gcc')} , {shutil.which('clang')})')
    subprocess.run(['make'], check=True)


    input('Press enter key to exit...')


