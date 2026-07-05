#pragma once

#include <imgui.h>

#include <optional>
#include <vector>

#include "geo_names.hpp"

inline std::optional<GeoNames> ImGuiGeoNames(char* fuzzy, int count, int maxResults = 8)
{
    thread_local std::vector<GeoNames> results;
    if (ImGui::InputText("Location", fuzzy, count))
    {
        GetGeoNames(results, maxResults, fuzzy);
    }
    std::optional<GeoNames> result;
    for (int i = 0; i < results.size(); i++)
    {
        ImGui::PushID(i);
        if (ImGui::Selectable(results[i].Location.c_str()))
        {
            result.emplace(results[i]);
        }
        ImGui::PopID();
    }
    return result;
}
