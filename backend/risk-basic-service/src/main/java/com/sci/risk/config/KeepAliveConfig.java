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

    @Value("${app.algorithm.tariff-endpoint:http://localhost:5000/tariff/execute}")
    private String tariffEndpoint;

    @Value("${app.algorithm.scenario-endpoint:http://localhost:5000/scenario/execute}")
    private String scenarioEndpoint;

    private final RestTemplate restTemplate = new RestTemplate();

    @Bean
    public CommandLineRunner keepAliveTask() {
        return args -> {
            System.out.println("=== Keep-Alive 配置完成 ===");
            System.out.println("关税算法: " + tariffEndpoint);
            System.out.println("场景算法: " + scenarioEndpoint);
        };
    }

    @Scheduled(fixedRate = 780000)
    public void pingAlgorithmServices() {
        pingService(tariffEndpoint, "关税算法");
        pingService(scenarioEndpoint, "场景算法");
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
