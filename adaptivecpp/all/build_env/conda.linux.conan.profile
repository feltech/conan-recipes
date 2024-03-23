[settings]
arch=x86_64
build_type=Release
compiler=clang
compiler.cppstd=23
compiler.libcxx=libstdc++11
compiler.version=18
os=Linux

[buildenv]
CC={{ os.getenv("CONDA_PREFIX") }}/bin/clang
CXX={{ os.getenv("CONDA_PREFIX") }}/bin/clang++
LD={{ os.getenv("CONDA_PREFIX") }}/bin/mold
# The deprecated FindCUDA.cmake module doesn't look in this stubs directory
# without a hint. Used e.g. by oneMKL.
CUDA_LIB_PATH={{ os.getenv("CONDA_PREFIX") }}/lib/stubs

[tool_requires]
# Speed things up with Ninja
ninja/1.11.1

[conf]
tools.build:sysroot={{ os.getenv("CONDA_BUILD_SYSROOT") }}
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "{{ os.getenv("CONDA_PREFIX") }}/bin/clang", "cpp": "{{ os.getenv("CONDA_PREFIX") }}/bin/clang++"}


# For bug in gettext (if needed somewhere as a build requirement) with Clang>=16
# Alternative solution is to use libgettext (see below)
#tools.build:cflags=["-Wno-error=incompatible-function-pointer-types", "-Wno-error=implicit-function-declaration"]
#
#[replace_tool_requires]
# Clang 16 introduced warnings-as-error for a couple of warnings in gettext 0.21.
#gettext/0.21: libgettext/0.22
