cmake_minimum_required(VERSION 3.8)
project(ares1_description)
find_package(ament_cmake REQUIRED)
install(DIRECTORY urdf meshes launch config DESTINATION share/${PROJECT_NAME})
# Install mujoco placeholder at root share if exists
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/mujoco")
  install(DIRECTORY mujoco DESTINATION share/${PROJECT_NAME})
endif()
ament_package()
