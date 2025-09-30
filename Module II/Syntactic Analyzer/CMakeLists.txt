cmake_minimum_required(VERSION 4.0)
project(Syntactic_Analyzer)

set(CMAKE_CXX_STANDARD 20)

add_executable(Syntactic_Analyzer main.cpp
        sintactico.cpp
        sintactico.hpp)
