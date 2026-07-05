#include <print>
#include <string>
#include <vector>

#include "geo_names.hpp"

int main(int argc, char** argv)
{
    std::vector<GeoNames> results;
    GetGeoNames(results, 8, "ott");
    for (const GeoNames& result : results)
    {
        std::println("Found \"{}\"", result.Location);
    }
    return 0;
}