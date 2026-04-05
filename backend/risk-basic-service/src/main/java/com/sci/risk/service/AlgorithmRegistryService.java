package com.sci.risk.service;

import com.sci.risk.model.AlgorithmInfo;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
public class AlgorithmRegistryService {
    private final Map<String, AlgorithmInfo> registry = new ConcurrentHashMap<>();

    public void register(AlgorithmInfo algorithm) {
        // 如果是自注册（category/type 为空），保留已有的 category/type/label 信息
        AlgorithmInfo existing = registry.get(algorithm.getName());
        if (existing != null) {
            if (algorithm.getCategory() == null || algorithm.getCategory().isBlank()) {
                algorithm.setCategory(existing.getCategory());
            }
            if (algorithm.getType() == null || algorithm.getType().isBlank()) {
                algorithm.setType(existing.getType());
            }
            if (algorithm.getLabel() == null || algorithm.getLabel().isBlank()) {
                algorithm.setLabel(existing.getLabel());
            }
        }
        // 注册即在线
        algorithm.setStatus("ONLINE");
        algorithm.setRegisteredTime(System.currentTimeMillis());
        registry.put(algorithm.getName(), algorithm);
        System.out.println("Algorithm registered: " + algorithm.getName());
    }

    public Optional<AlgorithmInfo> getAlgorithm(String name) {
        return Optional.ofNullable(registry.get(name));
    }

    public List<AlgorithmInfo> getAllAlgorithms() {
        return new ArrayList<>(registry.values());
    }

    /**
     * 按一级分类过滤算法列表
     */
    public List<AlgorithmInfo> getByCategory(String category) {
        return registry.values().stream()
                .filter(a -> category.equals(a.getCategory()))
                .collect(Collectors.toList());
    }

    /**
     * 按一级+二级分类过滤
     */
    public List<AlgorithmInfo> getByCategoryAndType(String category, String type) {
        return registry.values().stream()
                .filter(a -> category.equals(a.getCategory()) && type.equals(a.getType()))
                .collect(Collectors.toList());
    }

    /**
     * 获取两级分类树（供前端分类导航使用）
     */
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
