#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif
#include <chrono>
#include <cstdio>
#include <string>
#include <vector>

#include "geonames.hpp"

static constexpr int kMaxResults = 8;

int main(int argc, char** argv)
{
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif
    std::string pattern;
    for (int i = 1; i < argc; i++)
    {
        if (!pattern.empty())
        {
            pattern += ' ';
        }
        pattern += argv[i];
    }
    if (pattern.empty())
    {
        std::fprintf(stderr, "usage: %s <pattern>\n", argv[0]);
        return 1;
    }
    std::vector<GeoNames> results;
    const std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    GeoNamesQuery(results, kMaxResults, pattern);
    const std::chrono::duration<double, std::milli> elapsed = std::chrono::steady_clock::now() - start;
    for (const GeoNames& result : results)
    {
        std::printf("Found \"%s\" at %f,%f\n", result.Location.c_str(), result.Latitude, result.Longitude);
    }
    std::printf("%zu result(s) in %.3f ms\n", results.size(), elapsed.count());
    return results.empty() ? 1 : 0;
}
