cmake_minimum_required(VERSION 3.14)
project(MyCrowProject)

# Use vcpkg for dependencies
set(CMAKE_TOOLCHAIN_FILE "C:/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")

# Find Crow
find_package(Crow CONFIG REQUIRED)

# Create an executable
add_executable(my_app main.cpp)

# Link Crow
target_link_libraries(my_app PRIVATE Crow::Crow)
