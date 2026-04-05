package com.sci.risk.model;

import java.util.Map;

public class AlgorithmExecuteRequest {
    private Integer tariffRate;
    private String callbackUrl;
    private Map<String, String> additionalParams;

    public AlgorithmExecuteRequest() {}

    public Integer getTariffRate() { return tariffRate; }
    public void setTariffRate(Integer tariffRate) { this.tariffRate = tariffRate; }
    public String getCallbackUrl() { return callbackUrl; }
    public void setCallbackUrl(String callbackUrl) { this.callbackUrl = callbackUrl; }
    public Map<String, String> getAdditionalParams() { return additionalParams; }
    public void setAdditionalParams(Map<String, String> additionalParams) { this.additionalParams = additionalParams; }
}
