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

[tool_requires]
# Speed things up with Ninja
ninja/1.11.1

[conf]
tools.build:sysroot={{ os.getenv("CONDA_BUILD_SYSROOT") }}
tools.cmake.cmaketoolchain:generator=Ninja

# For bug in gettext (if needed somewhere as a build requirement) with Clang>=16
# Alternative solution is to use libgettext (see below)
#tools.build:cflags=["-Wno-error=incompatible-function-pointer-types", "-Wno-error=implicit-function-declaration"]
#
#[replace_tool_requires]
# Clang 16 introduced warnings-as-error for a couple of warnings in gettext 0.21.
#gettext/0.21: libgettext/0.22
