cmake_minimum_required(VERSION 3.20)
project(Syntactic_Analyzer CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Paths to sibling modules (quotes handle spaces in folder names)
set(LEX_DIR      "${CMAKE_CURRENT_SOURCE_DIR}/../Lexical Analyzer")
set(CODEGEN_DIR  "${CMAKE_CURRENT_SOURCE_DIR}/../Code Generator")

# Executable: add THIS module's sources + the needed deps' .cpp files
add_executable(Syntactic_Analyzer
        "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/sintactico.cpp"
        "${LEX_DIR}/lexico.cpp"
        "${CODEGEN_DIR}/genera.cpp"
)

# Header search paths (so you can keep #include "lexico.hpp" / "genera.hpp")
target_include_directories(Syntactic_Analyzer PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}"
        "${LEX_DIR}"
        "${CODEGEN_DIR}"
)

# Warnings (optional but recommended)
if (MSVC)
    target_compile_options(Syntactic_Analyzer PRIVATE /W4)
else()
    target_compile_options(Syntactic_Analyzer PRIVATE -Wall -Wextra -Wpedantic)
endif()
