package com.sci.risk.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.client.RestTemplate;

import java.net.HttpURLConnection;
import java.net.URL;

@Configuration
@EnableScheduling
public class KeepAliveConfig {

    @Value("${app.render.health-url:https://sci-risk.onrender.com/health}")
    private String renderHealthUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @Bean
    public CommandLineRunner keepAliveTask() {
        return args -> {
            System.out.println("=== Keep-Alive 配置完成 ===");
            System.out.println("Render Health URL: " + renderHealthUrl);
        };
    }

    @Scheduled(fixedRate = 600000)
    public void pingAlgorithmServices() {
        pingService(renderHealthUrl, "Render算法服务");
    }

    private void pingService(String endpoint, String serviceName) {
        try {
            URL url = new URL(endpoint.replace("/execute", "/health"));
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            int responseCode = connection.getResponseCode();
            System.out.println("[" + java.time.LocalDateTime.now() + "] Keep-Alive " + serviceName + ": " + responseCode);
            connection.disconnect();
        } catch (Exception e) {
            System.out.println("[" + java.time.LocalDateTime.now() + "] Keep-Alive " + serviceName + " ping failed: " + e.getMessage());
        }
    }
}
