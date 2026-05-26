cmake_minimum_required(VERSION 3.8)
project(shelf_bringup)

find_package(ament_cmake REQUIRED)

# Resources: launch files and params.
# (worlds/models/scripts are added in later checkpoints.)
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
