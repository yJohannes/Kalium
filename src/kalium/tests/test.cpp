#include <string>
#include <cstdlib>
#include <cstring>
#include <iostream>

extern "C"
{
    int add(int a, int b)
    {
        return a + b;
    }

    const char* strink(const char* s)
    {
        std::cout << "Dawg";
        // std::string str(s);
        return s;
    }

    // const char* double_string(const char* s)
    // {
    //     std::string str(s);
    //     str += str;
    //     return strdup(str.c_str());
    // }

    // void free_string(const char* s)
    // {
    //     free((void*)s); // void pointer -- generic pointer type that can point to any type
    // }
}

// g++ -shared -o test.dll -fPIC -std=c++17 test.cpp

// g++ -shared -o test.dll -fPIC test.cpp


// g++ -shared -o test.dll test.cpp -static-libstdc++ -static-libgcc

// g++ -o test.exe test.cpp -static-libstdc++ -static-libgcc
// g++ -shared -o test.dll -fPIC test.cpp -static-libgcc -static-libstdc++



