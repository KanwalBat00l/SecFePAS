# Install script for directory: /home/kanwal/OpenCheetah/deps/eigen/Eigen

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/kanwal/OpenCheetah/build")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/Eigen" TYPE FILE FILES
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Cholesky"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/CholmodSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Core"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Dense"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Eigen"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Eigenvalues"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Geometry"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Householder"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/IterativeLinearSolvers"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Jacobi"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/LU"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/MetisSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/OrderingMethods"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/PaStiXSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/PardisoSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/QR"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/QtAlignedMalloc"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SPQRSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SVD"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/Sparse"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SparseCholesky"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SparseCore"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SparseLU"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SparseQR"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/StdDeque"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/StdList"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/StdVector"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/SuperLUSupport"
    "/home/kanwal/OpenCheetah/deps/eigen/Eigen/UmfPackSupport"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/Eigen" TYPE DIRECTORY FILES "/home/kanwal/OpenCheetah/deps/eigen/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

