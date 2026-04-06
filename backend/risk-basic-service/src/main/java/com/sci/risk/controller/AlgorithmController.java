package com.sci.risk.controller;

import com.sci.risk.model.AlgorithmInfo;
import com.sci.risk.service.AlgorithmRegistryService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/algorithm")
@CrossOrigin(origins = "*")
@Tag(name = "算法管理", description = "算法发现、分类与状态管理接口")
public class AlgorithmController {

    private final AlgorithmRegistryService algorithmRegistry;

    @Autowired
    public AlgorithmController(AlgorithmRegistryService algorithmRegistry) {
        this.algorithmRegistry = algorithmRegistry;
    }

    @Operation(summary = "获取算法列表",
            description = "从算法注册中心获取所有已注册的算法服务列表，支持按 category 和 type 过滤")
    @ApiResponse(responseCode = "200", description = "成功",
            content = @Content(mediaType = "application/json",
                    array = @ArraySchema(schema = @Schema(implementation = AlgorithmInfo.class))))
    @GetMapping("/list")
    public List<AlgorithmInfo> getAlgorithmList(
            @Parameter(description = "一级分类 (risk / plan / inventory / supply_chain)")
            @RequestParam(required = false) String category,
            @Parameter(description = "二级分类 (simulation / classification / ...)")
            @RequestParam(required = false) String type) {
        if (category != null && type != null) {
            return algorithmRegistry.getByCategoryAndType(category, type);
        }
        if (category != null) {
            return algorithmRegistry.getByCategory(category);
        }
        return algorithmRegistry.getAllAlgorithms();
    }

    @Operation(summary = "获取两级分类树", description = "返回从算法注册中心同步的两级分类结构，供前端分类导航使用")
    @GetMapping("/categories")
    public List<Map<String, Object>> getCategoryTree() {
        return algorithmRegistry.getCategoryTree();
    }

    @Operation(summary = "获取算法详情", description = "根据算法名称获取特定算法的详细信息")
    @GetMapping("/{name}")
    public AlgorithmInfo getAlgorithm(@PathVariable String name) {
        return algorithmRegistry.getAlgorithm(name).orElse(null);
    }

    @Operation(summary = "更新算法状态", description = "更新指定算法的在线状态（ONLINE / OFFLINE）")
    @PutMapping("/{name}/status")
    public void updateAlgorithmStatus(
            @PathVariable String name,
            @RequestParam String status) {
        algorithmRegistry.updateStatus(name, status);
    }

    @Operation(summary = "健康检查", description = "检查算法服务是否在线")
    @GetMapping("/{name}/health")
    public boolean isAlgorithmOnline(@PathVariable String name) {
        return algorithmRegistry.isAlgorithmOnline(name);
    }

    @Operation(summary = "手动同步算法列表", description = "从算法注册中心手动同步算法列表")
    @PostMapping("/sync")
    public Map<String, Object> syncAlgorithms() {
        int count = algorithmRegistry.getAllAlgorithms().size();
        return Map.of(
            "status", "success",
            "message", "算法同步完成",
            "algorithmCount", count
        );
    }
}