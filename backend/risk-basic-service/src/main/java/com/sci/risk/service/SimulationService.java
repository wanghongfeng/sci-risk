package com.sci.risk.service;

import com.sci.risk.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class SimulationService {
    private final Map<String, SimulationTask> tasks = new ConcurrentHashMap<>();
    private final AlgorithmRegistryService algorithmRegistry;
    private final WebClient webClient;

    @Value("${app.callback-url:http://localhost:8080}")
    private String callbackBaseUrl;

    @Autowired
    public SimulationService(AlgorithmRegistryService algorithmRegistry) {
        this.algorithmRegistry = algorithmRegistry;
        this.webClient = WebClient.builder()
                .defaultHeader("Content-Type", "application/json")
                .build();
    }

    // ── 通用执行方法（推荐前端使用）──────────────────────────────────────

    /**
     * 通用算法执行入口。
     *
     * @param algorithmName 算法名称
     * @param params        算法参数（任意 JSON）
     * @param notification  通知上下文（可选，含 type / recipients / title）
     */
    public SimulationResponse executeAlgorithm(String algorithmName,
                                               Map<String, Object> params,
                                               Map<String, Object> notification) {
        String taskId = UUID.randomUUID().toString();
        SimulationTask task = new SimulationTask(taskId, algorithmName);
        task.setAlgorithmName(algorithmName);
        tasks.put(taskId, task);

        Optional<AlgorithmInfo> algoOpt = algorithmRegistry.getAlgorithm(algorithmName);
        if (algoOpt.isEmpty()) {
            task.setStatus("FAILED");
            task.setCurrentStatus("算法服务未注册: " + algorithmName);
            return new SimulationResponse(taskId, "FAILED", "算法服务未注册: " + algorithmName);
        }

        AlgorithmInfo algorithm = algoOpt.get();
        String callbackUrl = callbackBaseUrl + "/api/simulation/status";

        // 使用统一执行接口，将 params 作为独立字段传递
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("algorithmName", algorithmName);
        requestBody.put("taskId", taskId);
        requestBody.put("callbackUrl", callbackUrl);
        requestBody.put("params", params != null ? params : new HashMap<>());
        if (notification != null && !notification.isEmpty()) {
            requestBody.put("notification", notification);
        }

        try {
            // 优先调用统一入口 /algorithm/execute，降级到旧版 /execute
            String baseUrl = extractBaseUrl(algorithm.getEndpoint());
            String executeUrl = baseUrl + "/algorithm/execute";

            webClient.post()
                    .uri(executeUrl)
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(requestBody)
                    .retrieve()
                    .toEntity(Map.class)
                    .block();

            task.setStatus("EXECUTING");
            task.setCurrentStatus("算法执行中...");
            return new SimulationResponse(taskId, "EXECUTING", algorithmName + " 任务已启动");
        } catch (Exception e) {
            task.setStatus("FAILED");
            task.setCurrentStatus("调用算法服务失败: " + e.getMessage());
            return new SimulationResponse(taskId, "FAILED", "调用算法服务失败: " + e.getMessage());
        }
    }

    // ── 保留旧方法，内部委托给通用方法 ──────────────────────────────────

    public SimulationResponse startSimulation(Integer tariffRate) {
        Map<String, Object> params = new HashMap<>();
        params.put("tariffRate", tariffRate);
        return executeAlgorithm("tariff-risk-algorithm", params, null);
    }

    public SimulationResponse startRiskScenario(String scenarioType) {
        Map<String, Object> params = new HashMap<>();
        params.put("scenarioType", scenarioType);
        return executeAlgorithm("risk-scenarios-algorithm", params, null);
    }

    public SimulationResponse startMLRisk(Map<String, Object> mlParams) {
        return executeAlgorithm("risk-ml-algorithm", mlParams, null);
    }

    // ── 任务状态管理 ──────────────────────────────────────────────────────

    public void updateTaskStatus(String taskId, String status, int progress) {
        SimulationTask task = tasks.get(taskId);
        if (task != null) {
            task.setCurrentStatus(status);
            if (progress >= 100) {
                task.setStatus("COMPLETED");
            }
        }
    }

    public void updateTaskResult(String taskId, Object result) {
        SimulationTask task = tasks.get(taskId);
        if (task != null) {
            task.setResult(result);
            task.setStatus("COMPLETED");
        }
    }

    public SimulationTask getTask(String taskId) {
        return tasks.get(taskId);
    }

    public List<SimulationTask> getAllTasks() {
        return new ArrayList<>(tasks.values());
    }

    // ── 内部工具 ──────────────────────────────────────────────────────────

    /** 从 endpoint（如 http://localhost:5000/tariff）提取 base URL（http://localhost:5000） */
    private String extractBaseUrl(String endpoint) {
        if (endpoint == null) return "";
        // 去掉最后一个路径片段
        int idx = endpoint.lastIndexOf('/');
        if (idx > 8) {      // 保留 http:// 之后至少有 host
            return endpoint.substring(0, idx);
        }
        return endpoint;
    }
}
