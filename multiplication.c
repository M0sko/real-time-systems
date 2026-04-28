#include <stdint.h>

uint64_t multiply(uint64_t a, uint64_t b) {
    uint64_t res = 0;
    for(int i = 0; i < 10000; i++) {
        res += (a * b);
    }
    return res;
}