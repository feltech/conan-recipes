import os

from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy


class AdaptiveCppRecipe(ConanFile):
    name = "adaptivecpp"
    version = "develop"
    package_type = "library"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def requirements(self):
        self.requires("boost/1.84.0")
        self.requires("llvm-openmp/17.0.6")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")
        self.options["boost"].without_atomic = False  # Required for filesystem
        self.options["boost"].without_context = False  # Required for AdaptiveCpp / fiber
        self.options["boost"].without_fiber = False  # Required for AdaptiveCpp
        self.options["boost"].without_filesystem = False  # Required for fiber
        self.options["boost"].without_system = False  # Required for filesystem

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/AdaptiveCpp/AdaptiveCpp.git", target=".")
        git.folder = "."
        git.checkout(commit=self.version)

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.folders.source, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.folders.source, self.export_sources_folder)
        copy(self, "src/*.cpp", self.folders.source, self.export_sources_folder)
        copy(self, "include/*.hpp", self.folders.source, self.export_sources_folder)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["WITH_CUDA_BACKEND"] = True
        tc.cache_variables["WITH_ROCM_BACKEND"] = False
        tc.cache_variables["WITH_LEVEL_ZERO_BACKEND"] = False
        tc.cache_variables["WITH_OPENCL_BACKEND"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        # Must re-configure for llvmspirvtranslator install location.
        cmake.configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.builddirs = [self.package_folder]
        # Add SYCL CMake config file, so that `find_package(SYCL) works (e.g. for oneMKL).
        self.cpp_info.set_property("cmake_file_name", "SYCL")
        self.cpp_info.set_property("cmake_build_modules", [
            "lib/cmake/hipSYCL/hipsycl-config.cmake",
            "lib/cmake/OpenSYCL/opensycl-config.cmake",
            "lib/cmake/AdaptiveCpp/adaptivecpp-config.cmake"
        ])
        self.cpp_info.set_property("cmake_target_name", "SYCL::SYCL")
        # self.cpp_info.set_property("cmake_find_mode", "none")
