package com.practice.plantcare.plant;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Plant {

    @Id
    @GeneratedValue
    private Long id;

    private String nickname;
    private String latinName;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String imagePath;
}
