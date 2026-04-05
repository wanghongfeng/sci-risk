package com.sci.risk.model;

public class SimulationTask {
    private String taskId;
    private Integer tariffRate;
    private String status;
    private String currentStatus;
    private Object result;
    private long startTime;
    private String algorithmName;

    public SimulationTask() {}

    public SimulationTask(String taskId, Integer tariffRate) {
        this.taskId = taskId;
        this.tariffRate = tariffRate;
        this.status = "PENDING";
        this.startTime = System.currentTimeMillis();
    }

    public SimulationTask(String taskId, String scenarioType) {
        this.taskId = taskId;
        this.status = "PENDING";
        this.startTime = System.currentTimeMillis();
    }

    public String getTaskId() { return taskId; }
    public void setTaskId(String taskId) { this.taskId = taskId; }
    public Integer getTariffRate() { return tariffRate; }
    public void setTariffRate(Integer tariffRate) { this.tariffRate = tariffRate; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getCurrentStatus() { return currentStatus; }
    public void setCurrentStatus(String currentStatus) { this.currentStatus = currentStatus; }
    public Object getResult() { return result; }
    public void setResult(Object result) { this.result = result; }
    public long getStartTime() { return startTime; }
    public void setStartTime(long startTime) { this.startTime = startTime; }
    public String getAlgorithmName() { return algorithmName; }
    public void setAlgorithmName(String algorithmName) { this.algorithmName = algorithmName; }
}
