#include <cstdio>

#include "geonames.hpp"

int main(int argc, char** argv)
{
    std::vector<GeoNames> results;
    GetGeoNames(results, 8, "ott");
    for (const GeoNames& result : results)
    {
        std::printf("Found \"%s\" at %f,%f\n", result.Location.c_str(), result.Latitude, result.Longitude);
    }
    return 0;
}