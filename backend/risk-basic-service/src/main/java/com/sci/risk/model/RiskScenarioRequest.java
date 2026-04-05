package com.sci.risk.model;

public class RiskScenarioRequest {
    private String scenarioType;

    public RiskScenarioRequest() {}

    public RiskScenarioRequest(String scenarioType) {
        this.scenarioType = scenarioType;
    }

    public String getScenarioType() {
        return scenarioType;
    }

    public void setScenarioType(String scenarioType) {
        this.scenarioType = scenarioType;
    }
}