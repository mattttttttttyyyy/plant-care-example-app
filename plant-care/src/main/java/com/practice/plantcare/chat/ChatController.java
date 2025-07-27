package com.practice.plantcare.chat;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class ChatController {

    private final OpenAIService openAIService;

    @PostMapping("/message/{plantId}")
    public String sendMessage(@PathVariable Long plantId, @RequestPart("message") String message, @RequestPart(value = "image", required = false) MultipartFile image) throws IOException {
        return openAIService.sendMessage(plantId, message, image);
    }

    @GetMapping("/history/{plantId}")
    public List<String> getHistory(@PathVariable Long plantId) {
        return openAIService.getHistory(plantId);
    }
}
