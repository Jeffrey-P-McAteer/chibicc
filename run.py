
# Responsible for compiling stage0, then stage1 of chibicc

import subprocess
import tempfile
import shutil
import sys
import os
import tarfile
import io
import urllib.request

def find_ent_under(directory, check_fn):
    for dirent in os.listdir(directory):
        dirent_path = os.path.join(directory, dirent)
        if check_fn(dirent, dirent_path):
            return dirent_path
        if os.path.isdir(dirent_path):
            possible_match = find_ent_under(dirent_path, check_fn)
            if not (possible_match is None):
                return possible_match
    return None

c_compiler_exe = next(c for c in ['cc', 'gcc', 'clang'] if shutil.which(c) is not None)
print(f'c_compiler_exe = {c_compiler_exe}')
cpp_compiler_exe = next(c for c in ['cxx', 'g++', 'clang++'] if shutil.which(c) is not None)
print(f'cpp_compiler_exe = {cpp_compiler_exe}')

build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'build'))
os.makedirs(build_dir, exist_ok=True)

intel_pin_source_url = 'https://software.intel.com/sites/landingpage/pintool/downloads/pin-external-3.31-98869-gfa6f126a8-gcc-linux.tar.gz'
intel_pin_canary = find_ent_under(build_dir, lambda dirent, full_path: dirent == 'README')
if intel_pin_canary is None or not os.path.exists(intel_pin_canary):
    print(f'{intel_pin_canary} does not exist, downloading Intel Pin from {intel_pin_source_url}')
    with urllib.request.urlopen(intel_pin_source_url) as resp:
        tar_bytes = resp.read()
        ds = io.BytesIO(tar_bytes)
        with tarfile.open(fileobj=ds, mode='r:gz') as t:
            t.extractall(build_dir)
    print(f'Done, please re-start')
    sys.exit(1)
intel_pin_dir = os.path.dirname(intel_pin_canary)
print(f'intel_pin_dir = {intel_pin_dir}')

sys.exit(1)

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


