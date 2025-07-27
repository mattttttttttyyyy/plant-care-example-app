package com.practice.plantcare.plant;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/plants")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class PlantController {

    private final PlantService plantService;

    @PostMapping
    public Plant createPlant(@RequestBody Plant plant) {
        return plantService.createPlant(plant);
    }

    @GetMapping("/{id}")
    public Plant getPlantById(@PathVariable Long id) {
        return plantService.getPlantById(id);
    }

    @GetMapping
    public List<Plant> getAllPlants() {
        return plantService.getAllPlants();
    }

    @PutMapping("/{id}")
    public Plant updatePlant(@PathVariable Long id, @RequestBody Plant plant) {
        return plantService.updatePlant(id, plant);
    }

    @DeleteMapping("/{id}")
    public void deletePlant(@PathVariable Long id) {
        plantService.deletePlant(id);
    }
}
