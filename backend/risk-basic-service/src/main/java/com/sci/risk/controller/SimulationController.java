package com.sci.risk.controller;

import com.sci.risk.model.*;
import com.sci.risk.service.AlgorithmRegistryService;
import com.sci.risk.service.SimulationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
@Tag(name = "模拟服务", description = "算法执行与任务管理接口")
public class SimulationController {

    private final SimulationService simulationService;
    private final AlgorithmRegistryService algorithmRegistry;

    @Autowired
    public SimulationController(SimulationService simulationService,
                                 AlgorithmRegistryService algorithmRegistry) {
        this.simulationService = simulationService;
        this.algorithmRegistry = algorithmRegistry;
    }

    // ── 通用执行入口（推荐）─────────────────────────────────────────────

    @Operation(summary = "通用算法执行",
            description = "按算法名称执行任意已注册算法，params 为 JSON 格式参数，"
                    + "notification 可选，包含 type / recipients / title")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "任务启动成功"),
            @ApiResponse(responseCode = "400", description = "参数错误"),
            @ApiResponse(responseCode = "404", description = "算法未注册")
    })
    @PostMapping("/simulation/execute")
    public ResponseEntity<SimulationResponse> executeAlgorithm(
            @RequestBody Map<String, Object> body) {
        String algorithmName = (String) body.get("algorithmName");
        if (algorithmName == null || algorithmName.isBlank()) {
            return ResponseEntity.badRequest()
                    .body(new SimulationResponse(null, "FAILED", "algorithmName 不能为空"));
        }
        if (!algorithmRegistry.isAlgorithmOnline(algorithmName)) {
            return ResponseEntity.status(404)
                    .body(new SimulationResponse(null, "FAILED", "算法未注册: " + algorithmName));
        }
        @SuppressWarnings("unchecked")
        Map<String, Object> params = (Map<String, Object>) body.getOrDefault("params", Map.of());
        @SuppressWarnings("unchecked")
        Map<String, Object> notification = (Map<String, Object>) body.get("notification");
        return ResponseEntity.ok(simulationService.executeAlgorithm(algorithmName, params, notification));
    }

    // ── 保留旧版专用接口（兼容）──────────────────────────────────────────

    @Operation(summary = "启动关税模拟（旧）", description = "保留兼容，推荐使用 /simulation/execute")
    @PostMapping("/simulation/start")
    public SimulationResponse startSimulation(@RequestBody SimulationRequest request) {
        if (request.getTariffRate() == null) {
            return new SimulationResponse(null, "FAILED", "关税税率不能为空");
        }
        return simulationService.startSimulation(request.getTariffRate());
    }

    @Operation(summary = "启动风险场景分析（旧）", description = "保留兼容，推荐使用 /simulation/execute")
    @PostMapping("/simulation/start-risk-scenario")
    public SimulationResponse startRiskScenario(@RequestBody RiskScenarioRequest request) {
        String scenarioType = request.getScenarioType();
        if (scenarioType == null || scenarioType.isBlank()) {
            return new SimulationResponse(null, "FAILED", "风险场景类型不能为空");
        }
        return simulationService.startRiskScenario(scenarioType);
    }

    @Operation(summary = "启动ML风险预测（旧）", description = "保留兼容，推荐使用 /simulation/execute")
    @PostMapping("/simulation/ml-risk")
    public SimulationResponse startMLRisk(@RequestBody Map<String, Object> mlParams) {
        return simulationService.startMLRisk(mlParams);
    }

    // ── 任务查询 ──────────────────────────────────────────────────────────

    @Operation(summary = "查询任务状态")
    @GetMapping("/simulation/status/{taskId}")
    public SimulationTask getTaskStatus(
            @Parameter(description = "任务ID", required = true)
            @PathVariable String taskId) {
        return simulationService.getTask(taskId);
    }

    @Operation(summary = "获取所有任务")
    @GetMapping("/simulation/tasks")
    public List<SimulationTask> getAllTasks() {
        return simulationService.getAllTasks();
    }

    // ── 算法回调接口 ──────────────────────────────────────────────────────

    @Operation(summary = "接收状态更新", description = "算法服务异步执行状态回调")
    @PostMapping("/simulation/status")
    public void receiveStatus(@RequestBody Map<String, Object> payload) {
        String taskId = (String) payload.get("taskId");
        String status = (String) payload.get("status");
        Object progressObj = payload.get("progress");
        int progress = progressObj instanceof Number ? ((Number) progressObj).intValue() : 0;
        simulationService.updateTaskStatus(taskId, status, progress);
    }

    @Operation(summary = "接收执行结果", description = "算法服务执行完成结果回调")
    @PostMapping("/simulation/result")
    public void receiveResult(@RequestBody Map<String, Object> payload) {
        String taskId = (String) payload.get("taskId");
        simulationService.updateTaskResult(taskId, payload);
    }
}
