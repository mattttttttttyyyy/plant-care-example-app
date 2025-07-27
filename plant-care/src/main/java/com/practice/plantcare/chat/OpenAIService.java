package com.practice.plantcare.chat;

import com.practice.plantcare.plant.Plant;
import com.practice.plantcare.plant.PlantService;
import lombok.RequiredArgsConstructor;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class OpenAIService {

    private final ChatClient chatClient;
    private final ChatMemory chatMemory;
    private final PlantService plantService;

    public String sendMessage(Long plantId, String message, MultipartFile imageFile) throws IOException {
        Plant plant = plantService.getPlantById(plantId);

        UserMessage userMessage = new UserMessage(message);
        chatMemory.add(plantId.toString(), userMessage);

        String response = chatClient.prompt()
                .user(message)
                .system(systemSpec -> {
                    systemSpec.text("You are a helpful AI assistant specializing in plant care. You will provide advice based on the user\'s questions and the history of their plant.");
                    systemSpec.param("plantNickname", plant.getNickname());
                    systemSpec.param("plantLatinName", plant.getLatinName());
                })
                .call()
                .content();

        AssistantMessage aiMessage = new AssistantMessage(response);
        chatMemory.add(plantId.toString(), aiMessage);

        return response;
    }

    public List<String> getHistory(Long plantId) {
        return chatMemory.get(plantId.toString()).stream()
                .map(m -> {
                    if (m instanceof UserMessage) {
                        return "user: " + ((UserMessage) m).getText();
                    } else if (m instanceof AssistantMessage) {
                        return "ai: " + ((AssistantMessage) m).getText();
                    } else {
                        return m.getMessageType().name().toLowerCase() + ": " + m.toString();
                    }
                })
                .collect(Collectors.toList());
    }
}
