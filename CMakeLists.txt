cmake_minimum_required(VERSION 3.24)
project(geo_names)

add_subdirectory(lib/sqlite3)
add_library(geo_names src/geo_names.cpp)
target_include_directories(geo_names PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(geo_names PRIVATE savepoint_sqlite3)
set_target_properties(geo_names PROPERTIES CXX_STANDARD 23)
