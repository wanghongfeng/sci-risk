package com.sci.risk.model;

import java.util.Map;

public class AlgorithmInfo {
    private String name;
    private String version;
    private String endpoint;
    /** @deprecated 保留兼容，建议使用 paramsSchema */
    private String supportedParams;
    private String description;
    /** 一级分类: risk / plan / inventory / supply_chain */
    private String category;
    /** 二级分类: simulation / classification / assessment / ... */
    private String type;
    /** 算法展示名称（中文） */
    private String label;
    /** 输入参数 JSON Schema */
    private Map<String, Object> paramsSchema;
    /** 输出结果 JSON Schema */
    private Map<String, Object> outputSchema;
    private String status;
    private long registeredTime;

    public AlgorithmInfo() {}

    public AlgorithmInfo(String name, String version, String endpoint,
                         String supportedParams, String description) {
        this.name = name;
        this.version = version;
        this.endpoint = endpoint;
        this.supportedParams = supportedParams;
        this.description = description;
        this.label = description;
        this.status = "ONLINE";
        this.registeredTime = System.currentTimeMillis();
    }

    public AlgorithmInfo(String name, String version, String endpoint,
                         String description, String category, String type,
                         String label) {
        this(name, version, endpoint, "", description);
        this.category = category;
        this.type = type;
        this.label = label;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getEndpoint() { return endpoint; }
    public void setEndpoint(String endpoint) { this.endpoint = endpoint; }

    public String getSupportedParams() { return supportedParams; }
    public void setSupportedParams(String supportedParams) { this.supportedParams = supportedParams; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getLabel() { return label; }
    public void setLabel(String label) { this.label = label; }

    public Map<String, Object> getParamsSchema() { return paramsSchema; }
    public void setParamsSchema(Map<String, Object> paramsSchema) { this.paramsSchema = paramsSchema; }

    public Map<String, Object> getOutputSchema() { return outputSchema; }
    public void setOutputSchema(Map<String, Object> outputSchema) { this.outputSchema = outputSchema; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public long getRegisteredTime() { return registeredTime; }
    public void setRegisteredTime(long registeredTime) { this.registeredTime = registeredTime; }
}
