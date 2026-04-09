package com.sci.risk.model.entity;

import java.time.LocalDateTime;
import java.util.List;

public class Menu {
    private String menuId;
    private String menuName;
    private String menuCode;
    private String parentId;
    private String routePath;
    private String icon;
    private Integer sortOrder;
    private Boolean isVisible;
    private String permission;
    private String component;
    private List<Menu> children;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Menu() {}

    public Menu(String menuId, String menuName, String menuCode, String parentId, String routePath,
                String icon, Integer sortOrder, Boolean isVisible, String permission, String component) {
        this.menuId = menuId;
        this.menuName = menuName;
        this.menuCode = menuCode;
        this.parentId = parentId;
        this.routePath = routePath;
        this.icon = icon;
        this.sortOrder = sortOrder;
        this.isVisible = isVisible;
        this.permission = permission;
        this.component = component;
    }

    public String getMenuId() { return menuId; }
    public void setMenuId(String menuId) { this.menuId = menuId; }
    public String getMenuName() { return menuName; }
    public void setMenuName(String menuName) { this.menuName = menuName; }
    public String getMenuCode() { return menuCode; }
    public void setMenuCode(String menuCode) { this.menuCode = menuCode; }
    public String getParentId() { return parentId; }
    public void setParentId(String parentId) { this.parentId = parentId; }
    public String getRoutePath() { return routePath; }
    public void setRoutePath(String routePath) { this.routePath = routePath; }
    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Boolean getIsVisible() { return isVisible; }
    public void setIsVisible(Boolean isVisible) { this.isVisible = isVisible; }
    public String getPermission() { return permission; }
    public void setPermission(String permission) { this.permission = permission; }
    public String getComponent() { return component; }
    public void setComponent(String component) { this.component = component; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    public List<Menu> getChildren() { return children; }
    public void setChildren(List<Menu> children) { this.children = children; }
}
