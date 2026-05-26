cmake_minimum_required(VERSION 3.8)
project(shelf_bringup)

find_package(ament_cmake REQUIRED)

# Resources: launch files, params, worlds, models.
install(DIRECTORY
  launch
  config
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

# Mission node.
install(PROGRAMS
  scripts/orchestrator.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
