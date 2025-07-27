package com.practice.plantcare.plant;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PlantService {

    private final PlantRepository plantRepository;

    public Plant createPlant(Plant plant) {
        return plantRepository.save(plant);
    }

    public Plant getPlantById(Long id) {
        return plantRepository.findById(id).orElse(null);
    }

    public List<Plant> getAllPlants() {
        return plantRepository.findAll();
    }

    public Plant updatePlant(Long id, Plant plant) {
        Plant existingPlant = plantRepository.findById(id).orElse(null);
        if (existingPlant != null) {
            existingPlant.setNickname(plant.getNickname());
            existingPlant.setLatinName(plant.getLatinName());
            existingPlant.setUpdatedAt(plant.getUpdatedAt());
            existingPlant.setImagePath(plant.getImagePath());
            return plantRepository.save(existingPlant);
        }
        return null;
    }

    public void deletePlant(Long id) {
        plantRepository.deleteById(id);
    }
}
