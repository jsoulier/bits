# GeoNames

GeoNames is a lightweight, offline, city search library for C++ applications.
It loads the [geonames.org](https://geonames.org) dataset into a ~4 MB in-memory database and supports name prefixing (e.g. "ott" finds Ottawa, "van" finds Vancouver).
The average query takes ~0.3 ms on my machine.

### Example

```c++
#include <geonames.hpp>

#include <cstdio>
#include <vector>

int main()
{
    std::vector<GeoNames> results;
    GeoNamesQuery(results, 8, "new york");
    for (const GeoNames& result : results)
    {
        std::printf("Found \"%s\" at %f,%f\n", result.Location.c_str(), result.Latitude, result.Longitude);
    }
    return 0;
}
```

```
>>> Found "New York, New York, United States" at 40.714272,-74.005966
>>> Found "Brooklyn, Kings, New York, United States" at 40.650101,-73.949577
```

### CMake

Add the following to your `CMakeLists.txt`:

```cmake
add_subdirectory(<path>)
target_link_libraries(<name> PRIVATE geonames::geonames)
```

### Generation

Run `generate.py` to download the [geonames.org](https://geonames.org) dataset and rebuild the database.
Use `--lang` to generate for a different language (e.g. `fr` for French)
