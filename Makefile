tv_clientmake: tv_client.cpp
	arm-linux-gnueabi-g++ -o tv_client tv_client.cpp /home/nuric/Desktop/USB/libzmq_static_arm/include/zmq.h /home/nuric/Desktop/USB/libzmq_static_arm/lib/libzmq.a -pthread -static-libstdc++
