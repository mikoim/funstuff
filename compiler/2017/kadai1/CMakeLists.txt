cmake_minimum_required(VERSION 3.7)
project(kadai1)

set(CMAKE_C_STANDARD 11)

find_package(BISON)
FIND_PACKAGE(FLEX)

BISON_TARGET(parser parser.y ${CMAKE_CURRENT_BINARY_DIR}/parser.c COMPILE_FLAGS --debug)
BISON_TARGET(parser2 parser2.y ${CMAKE_CURRENT_BINARY_DIR}/parser2.c COMPILE_FLAGS --debug)

add_executable(kadai1 ${BISON_parser_OUTPUTS})
add_executable(kadai2 ${BISON_parser2_OUTPUTS})

target_link_libraries(kadai2 m)
