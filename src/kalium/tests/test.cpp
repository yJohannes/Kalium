#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>

// g++ -shared -o libpair.dll test.cpp -static-libstdc++ -static-libgcc

// g++ -shared -o libpair.dll -fPIC test.cpp -lstdc++

extern "C"
{
    char* pair(const char* s, const char* left, const char* right, const char* left_to, const char* right_to) {
        int num_pairs = 0;
        int stack[100];  // Basic stack to keep track of pair numbers
        int stack_pos = 0;

        // Allocate memory for result string (you'll need to adjust size for large inputs)
        char* result = (char*) malloc(1000 * sizeof(char));
        if (!result) return NULL;  // Handle memory allocation failure
        int res_pos = 0;

        std::string str = "cat";
        std::cout << str << std::endl;

        int i = 0;
        while (s[i] != '\0') {
            if (strncmp(s + i, left, strlen(left)) == 0) {
                num_pairs++;
                stack[stack_pos++] = num_pairs;
                res_pos += sprintf(result + res_pos, "<%s%d>", left_to, num_pairs);
                i += strlen(left);
            } else if (strncmp(s + i, right, strlen(right)) == 0) {
                int current_number = stack[--stack_pos];
                res_pos += sprintf(result + res_pos, "<%s%d>", right_to, current_number);
                i += strlen(right);
            } else {
                result[res_pos++] = s[i++];
            }
        }
        result[res_pos] = '\0';  // Null-terminate the result string
        return result;
    }
}