cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)
add_library(${PROJECT_NAME} STATIC test_package.cpp)
