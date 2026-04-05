package com.sci.risk.config;

import com.sci.risk.model.AlgorithmInfo;
import com.sci.risk.service.AlgorithmRegistryService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AlgorithmInitConfig {

    @Value("${app.algorithm.tariff-endpoint:http://localhost:5000/tariff}")
    private String tariffEndpoint;

    @Value("${app.algorithm.scenario-endpoint:http://localhost:5000/scenario}")
    private String scenarioEndpoint;

    @Value("${app.algorithm.ml-endpoint:http://localhost:5001/ml}")
    private String mlEndpoint;

    @Bean
    public CommandLineRunner initAlgorithms(AlgorithmRegistryService registry) {
        return args -> {
            // ── 风险分类 > 风险模拟 ──────────────────────────────────────
            registry.register(new AlgorithmInfo(
                "tariff-risk-algorithm",
                "1.0.0",
                tariffEndpoint,
                "关税风险模拟算法",
                "risk",
                "simulation",
                "关税风险模拟"
            ));

            // ── 风险分类 > 风险分类定义 ────────────────────────────────
            registry.register(new AlgorithmInfo(
                "risk-scenarios-algorithm",
                "1.0.0",
                scenarioEndpoint,
                "风险场景分析算法",
                "risk",
                "classification",
                "风险场景分析"
            ));

            // ── 风险分类 > ML综合评估 ──────────────────────────────────
            registry.register(new AlgorithmInfo(
                "risk-ml-algorithm",
                "1.0.0",
                mlEndpoint,
                "基于机器学习的供应链风险预测算法",
                "risk",
                "assessment",
                "ML风险评估"
            ));

            System.out.println("=== 算法注册完成 ===");
            registry.getAllAlgorithms().forEach(a ->
                System.out.println(String.format("- [%s/%s] %s -> %s",
                    a.getCategory(), a.getType(), a.getName(), a.getEndpoint()))
            );
        };
    }
}
