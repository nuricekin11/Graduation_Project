#include <iostream>
#include "zmq.hpp"

#include <pthread.h>
#include "string.h"
#include <iostream>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <net/if.h>
#include <unistd.h>
#include <memory>
#include <stdexcept>
#include <array>

using namespace std;
class Messages {


public:
    string Hello = "Hello";
    string TV_Definition = "You are TV";
    string PC_Definition = "You are PC";
    string OK = "OK";
    string Ready_File = "Ready For File";
    string ERROR = "Wrong meesages";


};


string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    chdir("/applications/deneme/");
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

class Header {
public:
    const string TV_HEADER = "0000";
    const string PC_HEADER = "1111";


};

void getMacAddress(char * uc_Mac)
{
     int fd;

    struct ifreq ifr;
    char *iface = "eth0";
    char *mac;

    fd = socket(AF_INET, SOCK_DGRAM, 0);

    ifr.ifr_addr.sa_family = AF_INET;
    strncpy((char *)ifr.ifr_name , (const char *)iface , IFNAMSIZ-1);

    ioctl(fd, SIOCGIFHWADDR, &ifr);

    close(fd);

    mac = (char *)ifr.ifr_hwaddr.sa_data;

    //display mac address
    sprintf((char *)uc_Mac,(const char *)"%.2x:%.2x:%.2x:%.2x:%.2x:%.2x\n" , mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

}



//string Converter(zmq::message_t reply)

//{

//   string rpl = string(static_cast<char*>(reply.data()), reply.size());
//   return rpl;


//}



int main()
{   Messages Msg;
    Header Hdr;
    FILE * pFile;
    char public_key [41] = "(}EAs+&eUb(jhXS5R!wX*OU3w&j!I/XED$mXhh9p";
    char secret_key [41] ="]LnuTub7Wr1.vL}!U)#{]s&}7%dedh1@6?Z.1m0:";
    char server_key[41] =  "IpT-c3x72Y2ff%[J+b#xoc9dsZN@G?b6JmF&xJe9";
//    int rc = zmq_curve_keypair(public_key, secret_key);

    cout<<endl<<"public_key: "<<public_key;
    cout<<endl<<"private_key: "<<secret_key;
//    printf("Output: %d",rc);
    zmq::context_t context(1);
    zmq::socket_t worker(context, ZMQ_DEALER);
    worker.setsockopt(ZMQ_CURVE_PUBLICKEY,public_key);
    worker.setsockopt(ZMQ_CURVE_SECRETKEY,secret_key);
    worker.setsockopt(ZMQ_CURVE_SERVERKEY,server_key);
    char mac[32]={0};
    getMacAddress(mac);
    zmq::message_t TV_Definiton;
    zmq::message_t File;
    zmq::message_t Hello (5);
    zmq::message_t Ready_File (10);


    string Identity = Hdr.TV_HEADER +mac;
    cout<<endl<<"Identity Address: "<< Identity;
    char ID[Identity.length()+1];
    strcpy(ID,Identity.c_str());
    worker.setsockopt(ZMQ_IDENTITY,ID,strlen(ID));
    cout<<endl<< "Communication started";
    worker.connect("tcp://10.12.0.43:5571");
    cout<<endl<< "Communication started";
    memcpy( Hello.data(),"HELLO", 5);
//    string rpl3 = string(static_cast<char*>(Hello.data()), Hello.size());
    cout<<endl<<"Hello: ";
    worker.send(Hello);
    worker.recv(&TV_Definiton);
    string answer = string(static_cast<char*>(TV_Definiton.data()), TV_Definiton.size());
    cout<<endl<< answer;
//   cout <<endl<<Converter(TV_Definiton);
    memcpy( Ready_File.data(), "Ready File",10);
    worker.send(Ready_File);
    cout<<endl<<"File waiting...";
    worker.recv(&File);
    cout<<endl<<"File received";
//    char *buffer = static_cast<char*>(File.data());
//    string file_string = string(static_cast<char*>(File.data()), File.size());
//    cout<<endl<< "File Data: "<<file_string;
//    char file_info[file_string.length()+1];
//    strcpy(file_info,file_string.c_str());
//    cout<< endl<<"Char Deneme: "<<file_info;
//    cout <<endl << Converter(File);
    chdir("/applications/deneme/");
//    cout <<endl<<"Buffer: "<<*buffer;
//    cout<<endl<<"Buffer size: "<< sizeof(file_info);
    pFile = fopen("targetfile.bin","w+");

    fwrite(File.data(),8,File.size(),pFile);
    fclose(pFile);
    chdir("/applications/deneme/");
    system("chmod +x targetfile.bin");

    string fileReturn = exec("/applications/deneme/targetfile.bin");
    cout<<endl<< "FileReturn: "<<fileReturn;
    zmq::message_t File_Return (fileReturn.length()+1);
    char *fileRe = new char [fileReturn.length()+1];
    strcpy(fileRe,fileReturn.c_str());
    cout<<endl<<"File return char: "<<fileRe;
    memcpy(File_Return.data(),fileReturn.data(), fileReturn.size());
//    string File_Return_deneme = string(static_cast<char*>(File_Return.data()), File_Return.size());
//    cout<<endl<<"File Data: "<<File_Return.data();
//    cout<<endl<<"File Return Data:"<<File_Return_deneme;
//    cout<<endl<<"fileRe Size: "<<strlen(fileRe);
    worker.send(File_Return);





    return 0;
}
