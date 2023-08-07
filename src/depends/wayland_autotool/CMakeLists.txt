cmake_minimum_required(VERSION 3.7.2)
project(wayland_autotool)
set(BIN_NAME wayland_autotool)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
find_package(Qt5 COMPONENTS Core Gui Widgets DBus Concurrent REQUIRED)
find_package(KF5Wayland)
set(Qt_LIBS
    Qt5::Core
    Qt5::Gui
    Qt5::Widgets
    Qt5::DBus
    Qt5::Concurrent
)
set(SOURCE_FILES 
        autotool.h
        autotool.cpp
	main.cpp
	)
add_executable(${BIN_NAME}
    ${SOURCE_FILES}
)
set_target_properties(${BIN_NAME}
	PROPERTIES
        CXX_STANDARD 11
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
)
target_include_directories(${BIN_NAME}
        PRIVATE
        ${X11_INCLUDE_DIR}
        ${SOURCE_FILES}
     #  service
)
target_link_libraries(${BIN_NAME} 
	${Qt_LIBS}
	KF5::WaylandClient
)

INSTALL(TARGETS ${BIN_NAME} DESTINATION bin)
