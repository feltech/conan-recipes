cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(oneMKL CONFIG REQUIRED)
add_executable(example src/example.cpp)
add_sycl_to_target(TARGET example SOURCES src/example.cpp)
target_link_libraries(example PRIVATE MKL::onemkl)
