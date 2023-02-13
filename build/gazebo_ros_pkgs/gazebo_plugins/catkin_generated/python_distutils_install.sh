#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/khang/youbot_ws/src/gazebo_ros_pkgs/gazebo_plugins"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/khang/youbot_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/khang/youbot_ws/install/lib/python2.7/dist-packages:/home/khang/youbot_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/khang/youbot_ws/build" \
    "/usr/bin/python2" \
    "/home/khang/youbot_ws/src/gazebo_ros_pkgs/gazebo_plugins/setup.py" \
     \
    build --build-base "/home/khang/youbot_ws/build/gazebo_ros_pkgs/gazebo_plugins" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/khang/youbot_ws/install" --install-scripts="/home/khang/youbot_ws/install/bin"
