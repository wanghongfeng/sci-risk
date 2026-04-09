package com.sci.risk.service;

import com.sci.risk.model.entity.Menu;
import com.sci.risk.model.dto.MenuRequest;
import com.sci.risk.repository.MenuRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class MenuService {

    private final MenuRepository menuRepository;

    @Autowired
    public MenuService(MenuRepository menuRepository) {
        this.menuRepository = menuRepository;
    }

    public List<Menu> getAllMenus() {
        return menuRepository.findAll();
    }

    public List<Menu> getRootMenus() {
        return menuRepository.findRootMenus();
    }

    public List<Menu> getMenusByParentId(String parentId) {
        return menuRepository.findByParentId(parentId);
    }

    public Optional<Menu> getMenuById(String menuId) {
        return Optional.ofNullable(menuRepository.findById(menuId));
    }

    public Optional<Menu> getMenuByCode(String menuCode) {
        return Optional.ofNullable(menuRepository.findByMenuCode(menuCode));
    }

    public Menu createMenu(MenuRequest request) {
        if (request.getMenuId() == null || request.getMenuId().isEmpty()) {
            throw new IllegalArgumentException("菜单ID不能为空");
        }
        if (menuRepository.existsById(request.getMenuId())) {
            throw new IllegalArgumentException("菜单ID已存在: " + request.getMenuId());
        }

        Menu menu = new Menu(
            request.getMenuId(),
            request.getMenuName(),
            request.getMenuCode(),
            request.getParentId() != null ? request.getParentId() : "0",
            request.getRoutePath(),
            request.getIcon(),
            request.getSortOrder() != null ? request.getSortOrder() : 0,
            request.getIsVisible() != null ? request.getIsVisible() : true,
            request.getPermission(),
            request.getComponent()
        );

        menuRepository.insert(menu);
        return menuRepository.findById(request.getMenuId());
    }

    public Optional<Menu> updateMenu(String menuId, MenuRequest request) {
        Menu existingMenu = menuRepository.findById(menuId);
        if (existingMenu == null) {
            return Optional.empty();
        }

        if (request.getMenuName() != null) {
            existingMenu.setMenuName(request.getMenuName());
        }
        if (request.getMenuCode() != null) {
            existingMenu.setMenuCode(request.getMenuCode());
        }
        if (request.getParentId() != null) {
            existingMenu.setParentId(request.getParentId());
        }
        if (request.getRoutePath() != null) {
            existingMenu.setRoutePath(request.getRoutePath());
        }
        if (request.getIcon() != null) {
            existingMenu.setIcon(request.getIcon());
        }
        if (request.getSortOrder() != null) {
            existingMenu.setSortOrder(request.getSortOrder());
        }
        if (request.getIsVisible() != null) {
            existingMenu.setIsVisible(request.getIsVisible());
        }
        if (request.getPermission() != null) {
            existingMenu.setPermission(request.getPermission());
        }
        if (request.getComponent() != null) {
            existingMenu.setComponent(request.getComponent());
        }

        menuRepository.update(existingMenu);
        return Optional.of(existingMenu);
    }

    public boolean deleteMenu(String menuId) {
        if (!menuRepository.existsById(menuId)) {
            return false;
        }
        return menuRepository.deleteById(menuId) > 0;
    }

    public List<Menu> getMenuTree() {
        List<Menu> allMenus = menuRepository.findAll();
        return buildMenuTree(allMenus, "0");
    }

    private List<Menu> buildMenuTree(List<Menu> allMenus, String parentId) {
        return allMenus.stream()
            .filter(menu -> parentId.equals(menu.getParentId()))
            .peek(menu -> {
                List<Menu> children = buildMenuTree(allMenus, menu.getMenuId());
                if (!children.isEmpty()) {
                    menu.setChildren(children);
                }
            })
            .collect(Collectors.toList());
    }

    public int getMenuCount() {
        return menuRepository.count();
    }
}
