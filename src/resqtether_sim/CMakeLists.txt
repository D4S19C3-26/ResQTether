cmake_minimum_required(VERSION 3.8)
project(resqtether_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(
  DIRECTORY urdf worlds launch rviz
  DESTINATION share/${PROJECT_NAME}
)

# Install Python package (makes 'resqtether_sim' importable and registers console scripts)
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  resqtether_sim/signal_map_node.py
  resqtether_sim/mock_mission_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
