cmake_minimum_required(VERSION 3.8)
project(CntrlL)

set(CMAKE_C_STANDARD 99)

find_package(BISON)
find_package(FLEX)

BISON_TARGET(Parser CntrlL.y ${CMAKE_CURRENT_BINARY_DIR}/parser.c COMPILE_FLAGS "-dvy")
FLEX_TARGET(Scanner CntrlL.l ${CMAKE_CURRENT_BINARY_DIR}/scanner.c COMPILE_FLAGS "-l")
ADD_FLEX_BISON_DEPENDENCY(Scanner Parser)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_executable(CntrlL ${BISON_Parser_OUTPUTS} ${FLEX_Scanner_OUTPUTS} NameTable.c SymTable.c JumpChain.c LabelDef.c VSM.c MainFunc.c)

target_link_libraries(CntrlL fl)
