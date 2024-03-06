cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(AdaptiveCpp CONFIG REQUIRED)
add_executable(example src/example.cpp)
add_sycl_to_target(TARGET example SOURCES src/example.cpp)
