package com.practice.plantcare.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "file.upload")
@Data
public class FileStorageProperties {

    private String uploadDir;
}
