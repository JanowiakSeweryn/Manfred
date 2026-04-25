#include <iostream>
#include <fstream>
#include <string>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
#include <fcntl.h>

#define PORT 8080
#define BACKLOG 5

std::string GetBrowserHeader(std::string content);
std::string GetContent(const char * filename);

void send_signal(const std::string& message);
// int SendMsg(std::string req); later to implement for code quality

int main(){

    // std::string key = read_from_socket();
    int sock_n,sock_udp;
    //AF_INET
    sock_n = socket(AF_INET,SOCK_STREAM,0);
    struct sockaddr_in serwer;

    serwer.sin_family = AF_INET; //ipv6 addres
    serwer.sin_port = htons(PORT); 
    serwer.sin_addr.s_addr = INADDR_ANY;

    std::string content,header, webinfo;
    content = GetContent("index.html");
    header = GetBrowserHeader(content);
    webinfo = header+content;

    //geminy help me 
    int opt = 1;
    setsockopt(sock_n, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    bind(sock_n,(struct sockaddr *)&serwer,sizeof serwer);
    listen(sock_n,BACKLOG);

    std::cout << "Listening on " << PORT << "..." << std::endl;

    int iter = 0;

    while(true){

        std::cout << " .. loop_start ..\n ";

        int new_socket = accept(sock_n, nullptr, nullptr);


        char buffer[2048] = {0};
        // std::vector<char>buffer;
        recv(new_socket, buffer, 2048, 0);
        std::string request(buffer);

        if (request.find("GET /manfred_on") != std::string::npos) {

            std::string response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK";

            send(new_socket, response.c_str(), response.size(), 0);

            if (iter == 0) {
		        std::cout << "button_pressed! \n";
                iter ++;
                send_signal("PRESSED");
            }
            else{
		        std::cout << "button_pressed_again! \n";
                send_signal("NOT_PRESSED");
                iter = 0;
            }
        }
        else if(request.find("GET /open_manfred") != std::string::npos) {

            std::string response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK";

            send(new_socket, response.c_str(), response.size(), 0);
            system("python3 test.py Models/manfred_v1.6.pth & ");
        }

        send(new_socket,webinfo.c_str(), webinfo.size(), 0);

        close(new_socket);


    }


    return 0;
}
std::string GetBrowserHeader(std::string content){

    // 4. Create the HTTP Response Header
    //  ---------------- This is crucial! Browsers need this exact format ----------------

    std::string header = "HTTP/1.1 200 OK\r\n";
    header += "Content-Type: text/html\r\n";
    header += "Content-Length: " + std::to_string(content.size()) + "\r\n";
    header += "Connection: close\r\n\r\n";
    return header;
}

std::string GetContent(const char * filename){
    std::ifstream file(filename);
    std::string content((std::istreambuf_iterator<char>(file)), 
        std::istreambuf_iterator<char>());

    return content;
}


void send_signal(const std::string& message) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(5005); // Must match Python port
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    sendto(sock, message.c_str(), message.size(), 0, 
           (const struct sockaddr *)&servaddr, sizeof servaddr);
    
    close(sock);
}

