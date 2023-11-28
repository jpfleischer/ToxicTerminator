cmake_minimum_required(VERSION 3.16)
project("toxicterminator")
set(CMAKE_CXX_STANDARD 17)

set(APP_SOURCE ".")
set(MODULE_SOURCE ".")
set(EXTERNALS "../../extern")

# pybind11
find_package(pybind11 REQUIRED)

# module
pybind11_add_module (
    pybind11module 
    ${MODULE_SOURCE}/trie.cpp
)


target_include_directories (
    pybind11module 
    PRIVATE ${MODULE_SOURCE}
)

# app
add_executable (
    pybind11app
    ${APP_SOURCE}/app.cpp
)

target_include_directories (
    pybind11app 
    PRIVATE ${APP_SOURCE}
    PRIVATE ${MODULE_SOURCE}
)

target_link_libraries(
    pybind11app
    PRIVATE pybind11::embed
)