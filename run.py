
# Responsible for compiling stage0, then stage1 of chibicc

import subprocess
import tempfile
import shutil
import sys
import os

compiler_exe = next(c for c in ['cc', 'gcc', 'clang'] if shutil.which(c) is not None)
print(f'compiler_exe = {compiler_exe}')

print('Compiling pin-experiment-01')
subprocess.run([
    compiler_exe,
        '-o', 'pin_experiment_01.so',
        '-shared',
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


