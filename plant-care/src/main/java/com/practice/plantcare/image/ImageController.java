package com.practice.plantcare.image;

import com.practice.plantcare.plant.Plant;
import com.practice.plantcare.plant.PlantService;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.io.IOException;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/images")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class ImageController {

    private final ImageStorageService imageStorageService;
    private final PlantService plantService;

    @PostMapping("/upload/{plantId}")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file, @PathVariable Long plantId) {
        String fileName = imageStorageService.storeFile(file, String.valueOf(plantId));

        String fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
                .path("/api/images/download/")
                .path(fileName)
                .toUriString();

        Plant plant = plantService.getPlantById(plantId);
        if (plant != null) {
            plant.setImagePath(fileDownloadUri);
            plant.setUpdatedAt(LocalDateTime.now());
            plantService.updatePlant(plantId, plant);
        }

        return ResponseEntity.ok(fileDownloadUri);
    }

    @GetMapping("/download/{fileName:.+}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String fileName) throws IOException {
        Resource resource = imageStorageService.loadFileAsResource(fileName);

        String contentType = "application/octet-stream";

        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(contentType))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
                .body(resource);
    }
}
