cmake_minimum_required(VERSION 3.8)
project(shelf_bringup)

find_package(ament_cmake REQUIRED)

# Resources: launch files, params, worlds, models.
# (scripts are added in CP4.)
install(DIRECTORY
  launch
  config
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
