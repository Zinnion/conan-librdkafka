#include <string>
#include <iostream>
#include "librdkafka/rdkafkacpp.h"

int main()
{
 std::cout << RdKafka::version_str().c_str() << std::endl;
 return 0;
}
