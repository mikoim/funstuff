cmake_minimum_required(VERSION 3.8)
project(FuncL)

set(CMAKE_C_STANDARD 99)

find_package(BISON)
find_package(FLEX)

BISON_TARGET(Parser FuncL.y ${CMAKE_CURRENT_BINARY_DIR}/parser.c COMPILE_FLAGS "-dvy")
FLEX_TARGET(Scanner FuncL.l ${CMAKE_CURRENT_BINARY_DIR}/scanner.c COMPILE_FLAGS "-l")
ADD_FLEX_BISON_DEPENDENCY(Scanner Parser)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_executable(FuncL ${BISON_Parser_OUTPUTS} ${FLEX_Scanner_OUTPUTS} NameTable.c SymTable.c SymTable.h JumpChain.c LabelDef.c VSM.c VSM.h MainFunc.c)

target_link_libraries(FuncL fl)
