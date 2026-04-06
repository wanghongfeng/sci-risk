package com.sci.risk.service;

import com.sci.risk.model.AlgorithmInfo;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
public class AlgorithmRegistryService {
    private static final Logger log = LoggerFactory.getLogger(AlgorithmRegistryService.class);

    @Value("${app.algorithm.registry-url:http://localhost:5000}")
    private String registryUrl;

    @Value("${app.algorithm.sync-interval:60000}")
    private long syncInterval;

    private final Map<String, AlgorithmInfo> registry = new ConcurrentHashMap<>();
    private final RestTemplate restTemplate = new RestTemplate();

    @PostConstruct
    public void init() {
        syncAlgorithms();
    }

    @Scheduled(fixedDelayString = "${app.algorithm.sync-interval:60000}")
    public void syncAlgorithms() {
        try {
            String algorithmsUrl = registryUrl + "/algorithms?includeRemote=true";
            @SuppressWarnings("unchecked")
            Map<String, Object> response = restTemplate.getForObject(algorithmsUrl, Map.class);

            if (response == null || !response.containsKey("algorithms")) {
                log.warn("Failed to sync algorithms: invalid response from registry");
                return;
            }

            @SuppressWarnings("unchecked")
            List<Map<String, Object>> algorithms = (List<Map<String, Object>>) response.get("algorithms");

            registry.clear();

            for (Map<String, Object> algo : algorithms) {
                AlgorithmInfo info = convertToAlgorithmInfo(algo);
                info.setStatus("ONLINE");
                info.setRegisteredTime(System.currentTimeMillis());
                registry.put(info.getName(), info);
            }

            log.info("Synced {} algorithms from registry center", registry.size());

            String categoriesUrl = registryUrl + "/categories";
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> categories = (List<Map<String, Object>>) restTemplate.getForObject(categoriesUrl, List.class);
            if (categories != null) {
                log.info("Synced {} categories from registry center", categories.size());
            }

        } catch (Exception e) {
            log.error("Failed to sync algorithms from registry center: {}", e.getMessage());
        }
    }

    private AlgorithmInfo convertToAlgorithmInfo(Map<String, Object> algo) {
        AlgorithmInfo info = new AlgorithmInfo();
        info.setName((String) algo.get("name"));
        info.setVersion((String) algo.get("version"));
        info.setDescription((String) algo.get("description"));
        info.setCategory((String) algo.get("category"));
        info.setType((String) algo.get("type"));
        info.setLabel((String) algo.get("label"));

        Object endpoint = algo.get("endpoint");
        if (endpoint == null) {
            String name = info.getName();
            String slug = name != null ? name.split("-")[0] : "unknown";
            info.setEndpoint(registryUrl + "/" + slug + "/execute");
        } else {
            info.setEndpoint((String) endpoint);
        }

        @SuppressWarnings("unchecked")
        Map<String, Object> paramsSchema = (Map<String, Object>) algo.get("paramsSchema");
        info.setParamsSchema(paramsSchema);

        @SuppressWarnings("unchecked")
        Map<String, Object> outputSchema = (Map<String, Object>) algo.get("outputSchema");
        info.setOutputSchema(outputSchema);

        return info;
    }

    public Optional<AlgorithmInfo> getAlgorithm(String name) {
        return Optional.ofNullable(registry.get(name));
    }

    public List<AlgorithmInfo> getAllAlgorithms() {
        return new ArrayList<>(registry.values());
    }

    public List<AlgorithmInfo> getByCategory(String category) {
        return registry.values().stream()
                .filter(a -> category.equals(a.getCategory()))
                .collect(Collectors.toList());
    }

    public List<AlgorithmInfo> getByCategoryAndType(String category, String type) {
        return registry.values().stream()
                .filter(a -> category.equals(a.getCategory()) && type.equals(a.getType()))
                .collect(Collectors.toList());
    }

    public List<Map<String, Object>> getCategoryTree() {
        Map<String, Map<String, Object>> tree = new LinkedHashMap<>();
        for (AlgorithmInfo algo : registry.values()) {
            String cat = algo.getCategory();
            String typ = algo.getType();
            if (cat == null) continue;
            tree.computeIfAbsent(cat, k -> {
                Map<String, Object> node = new LinkedHashMap<>();
                node.put("category", k);
                node.put("label", categoryLabel(k));
                node.put("types", new LinkedHashMap<String, Object>());
                return node;
            });
            @SuppressWarnings("unchecked")
            Map<String, Map<String, Object>> types =
                    (Map<String, Map<String, Object>>) tree.get(cat).get("types");
            types.computeIfAbsent(typ, k -> {
                Map<String, Object> t = new LinkedHashMap<>();
                t.put("type", k);
                t.put("label", typeLabel(k));
                t.put("count", 0);
                return t;
            });
            types.get(typ).put("count", (int) types.get(typ).get("count") + 1);
        }
        return tree.values().stream().map(v -> {
            @SuppressWarnings("unchecked")
            Map<String, Map<String, Object>> types =
                    (Map<String, Map<String, Object>>) v.get("types");
            Map<String, Object> node = new LinkedHashMap<>(v);
            node.put("types", new ArrayList<>(types.values()));
            return node;
        }).collect(Collectors.toList());
    }

    public void updateStatus(String name, String status) {
        AlgorithmInfo algo = registry.get(name);
        if (algo != null) {
            algo.setStatus(status);
        }
    }

    public boolean isAlgorithmOnline(String name) {
        AlgorithmInfo algo = registry.get(name);
        return algo != null && "ONLINE".equals(algo.getStatus());
    }

    public String getRegistryUrl() {
        return registryUrl;
    }

    private String categoryLabel(String category) {
        switch (category) {
            case "risk": return "风险";
            case "plan": return "计划";
            case "inventory": return "库存";
            case "supply_chain": return "供应链";
            default: return category;
        }
    }

    private String typeLabel(String type) {
        if (type == null) return "";
        switch (type) {
            case "simulation": return "风险模拟";
            case "classification": return "风险分类";
            case "assessment": return "综合评估";
            case "order_simulation": return "订单模拟";
            case "production_transfer": return "转产规划";
            case "capacity_planning": return "产能规划";
            case "consumption": return "消耗模拟";
            case "replenishment": return "补货建议";
            case "shortage_risk": return "短缺风险";
            case "disruption": return "中断模拟";
            case "optimization": return "优化建议";
            default: return type;
        }
    }
}