// Generated by gencpp from file gazebo_msgs/SensorPerformanceMetric.msg
// DO NOT EDIT!


#ifndef GAZEBO_MSGS_MESSAGE_SENSORPERFORMANCEMETRIC_H
#define GAZEBO_MSGS_MESSAGE_SENSORPERFORMANCEMETRIC_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace gazebo_msgs
{
template <class ContainerAllocator>
struct SensorPerformanceMetric_
{
  typedef SensorPerformanceMetric_<ContainerAllocator> Type;

  SensorPerformanceMetric_()
    : name()
    , sim_update_rate(0.0)
    , real_update_rate(0.0)
    , fps(0.0)  {
    }
  SensorPerformanceMetric_(const ContainerAllocator& _alloc)
    : name(_alloc)
    , sim_update_rate(0.0)
    , real_update_rate(0.0)
    , fps(0.0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _name_type;
  _name_type name;

   typedef double _sim_update_rate_type;
  _sim_update_rate_type sim_update_rate;

   typedef double _real_update_rate_type;
  _real_update_rate_type real_update_rate;

   typedef double _fps_type;
  _fps_type fps;





  typedef boost::shared_ptr< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> const> ConstPtr;

}; // struct SensorPerformanceMetric_

typedef ::gazebo_msgs::SensorPerformanceMetric_<std::allocator<void> > SensorPerformanceMetric;

typedef boost::shared_ptr< ::gazebo_msgs::SensorPerformanceMetric > SensorPerformanceMetricPtr;
typedef boost::shared_ptr< ::gazebo_msgs::SensorPerformanceMetric const> SensorPerformanceMetricConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace gazebo_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'sensor_msgs': ['/opt/ros/kinetic/share/sensor_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'trajectory_msgs': ['/opt/ros/kinetic/share/trajectory_msgs/cmake/../msg'], 'gazebo_msgs': ['/home/khang/youbot_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
{
  static const char* value()
  {
    return "01762ded18cfe9ebc7c8222667c99547";
  }

  static const char* value(const ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x01762ded18cfe9ebULL;
  static const uint64_t static_value2 = 0xc7c8222667c99547ULL;
};

template<class ContainerAllocator>
struct DataType< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
{
  static const char* value()
  {
    return "gazebo_msgs/SensorPerformanceMetric";
  }

  static const char* value(const ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string name\n\
float64 sim_update_rate\n\
float64 real_update_rate\n\
float64 fps\n\
";
  }

  static const char* value(const ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.name);
      stream.next(m.sim_update_rate);
      stream.next(m.real_update_rate);
      stream.next(m.fps);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SensorPerformanceMetric_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::gazebo_msgs::SensorPerformanceMetric_<ContainerAllocator>& v)
  {
    s << indent << "name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.name);
    s << indent << "sim_update_rate: ";
    Printer<double>::stream(s, indent + "  ", v.sim_update_rate);
    s << indent << "real_update_rate: ";
    Printer<double>::stream(s, indent + "  ", v.real_update_rate);
    s << indent << "fps: ";
    Printer<double>::stream(s, indent + "  ", v.fps);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GAZEBO_MSGS_MESSAGE_SENSORPERFORMANCEMETRIC_H
