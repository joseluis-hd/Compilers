cmake_minimum_required(VERSION 4.0)
project(Lexical_Analyzer)

set(CMAKE_CXX_STANDARD 20)

add_executable(Lexical_Analyzer main.cpp
        lexico.cpp
        lexico.hpp)
