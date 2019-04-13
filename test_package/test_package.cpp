#include <string>
#include "rdkafkacpp_int.h"

int main()
{
 version_str();
 return 0;
}

std::string RdKafka::version_str () {
  return std::string(rd_kafka_version_str());
}}
