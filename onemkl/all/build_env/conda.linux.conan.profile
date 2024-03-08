[settings]
arch=x86_64
build_type=Release
compiler=clang
compiler.cppstd=20
compiler.libcxx=libstdc++11
# TODO(DF): Upgrade to clang 17 when https://github.com/conda-forge/clangdev-feedstock/issues/271
compiler.version=15
os=Linux

[buildenv]
CC={{ os.getenv("CONDA_PREFIX") }}/bin/clang
CXX={{ os.getenv("CONDA_PREFIX") }}/bin/clang++
CUDA_LIB_PATH={{ os.getenv("CONDA_PREFIX") }}/lib/stubs

[tool_requires]
# Speed things up with Ninja
ninja/1.11.1

[conf]
tools.build:sysroot={{ os.getenv("CONDA_BUILD_SYSROOT") }}
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "{{ os.getenv("CONDA_PREFIX") }}/bin/clang", "cpp": "{{ os.getenv("CONDA_PREFIX") }}/bin/clang++"}
