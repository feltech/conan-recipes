import os

from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, replace_in_file


class oneMKLRecipe(ConanFile):
    name = "onemkl"
    version = "develop"
    package_type = "library"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def requirements(self):
        self.requires("adaptivecpp/develop")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/oneapi-src/oneMKL.git", target=".")
        git.folder = "."
        git.checkout(commit=self.version)
        # Don't report warnings in compilation output due to oneMKL headers.
        replace_in_file(
            self,
            os.path.join(self.source_folder, "src", "CMakeLists.txt"),
            "set_target_properties(onemkl PROPERTIES EXPORT_NO_SYSTEM true)",
            "",
        )

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.folders.source, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.folders.source, self.export_sources_folder)
        copy(self, "src/*.cpp", self.folders.source, self.export_sources_folder)
        copy(self, "include/*.hpp", self.folders.source, self.export_sources_folder)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables.update(
            {
                "ENABLE_MKLCPU_BACKEND": False,
                "ENABLE_MKLGPU_BACKEND": False,
                "ENABLE_CUBLAS_BACKEND": True,
                "BUILD_FUNCTIONAL_TESTS": False,
                "BUILD_DOC": False,
                "BUILD_EXAMPLES": False,
                "TARGET_DOMAINS": "blas",
                "ONEMKL_SYCL_IMPLEMENTATION": "hipsycl",
                "HIPSYCL_TARGETS": "generic",
            }
        )
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.builddirs = [self.package_folder]
        self.cpp_info.set_property("cmake_find_mode", "none")
