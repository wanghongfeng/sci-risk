package com.sci.risk.controller;

import com.sci.risk.model.entity.Menu;
import com.sci.risk.model.dto.MenuRequest;
import com.sci.risk.service.MenuService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/menu")
@CrossOrigin(origins = "*")
@Tag(name = "菜单管理", description = "系统菜单维护接口")
public class MenuController {

    private final MenuService menuService;

    @Autowired
    public MenuController(MenuService menuService) {
        this.menuService = menuService;
    }

    @Operation(summary = "获取所有菜单", description = "获取系统中所有菜单列表，按排序字段排序")
    @ApiResponse(responseCode = "200", description = "成功获取菜单列表")
    @GetMapping("/list")
    public ResponseEntity<List<Menu>> getAllMenus() {
        List<Menu> menus = menuService.getAllMenus();
        return ResponseEntity.ok(menus);
    }

    @Operation(summary = "获取菜单树", description = "获取树形结构的菜单列表")
    @ApiResponse(responseCode = "200", description = "成功获取菜单树")
    @GetMapping("/tree")
    public ResponseEntity<List<Menu>> getMenuTree() {
        List<Menu> menuTree = menuService.getMenuTree();
        return ResponseEntity.ok(menuTree);
    }

    @Operation(summary = "获取根菜单", description = "获取所有顶级菜单（parent_id为0的菜单）")
    @ApiResponse(responseCode = "200", description = "成功获取根菜单列表")
    @GetMapping("/root")
    public ResponseEntity<List<Menu>> getRootMenus() {
        List<Menu> rootMenus = menuService.getRootMenus();
        return ResponseEntity.ok(rootMenus);
    }

    @Operation(summary = "获取子菜单", description = "根据父菜单ID获取子菜单列表")
    @ApiResponse(responseCode = "200", description = "成功获取子菜单列表")
    @GetMapping("/children/{parentId}")
    public ResponseEntity<List<Menu>> getChildrenMenus(
            @Parameter(description = "父菜单ID", required = true)
            @PathVariable String parentId) {
        List<Menu> children = menuService.getMenusByParentId(parentId);
        return ResponseEntity.ok(children);
    }

    @Operation(summary = "获取菜单详情", description = "根据菜单ID获取菜单详细信息")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "成功获取菜单详情"),
        @ApiResponse(responseCode = "404", description = "菜单不存在")
    })
    @GetMapping("/{menuId}")
    public ResponseEntity<Menu> getMenuById(
            @Parameter(description = "菜单ID", required = true)
            @PathVariable String menuId) {
        Optional<Menu> menu = menuService.getMenuById(menuId);
        return menu.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }

    @Operation(summary = "根据菜单代码获取菜单", description = "根据菜单代码获取菜单详细信息")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "成功获取菜单详情"),
        @ApiResponse(responseCode = "404", description = "菜单不存在")
    })
    @GetMapping("/code/{menuCode}")
    public ResponseEntity<Menu> getMenuByCode(
            @Parameter(description = "菜单代码", required = true)
            @PathVariable String menuCode) {
        Optional<Menu> menu = menuService.getMenuByCode(menuCode);
        return menu.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }

    @Operation(summary = "创建菜单", description = "创建新的菜单项")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "菜单创建成功"),
        @ApiResponse(responseCode = "400", description = "参数错误或菜单ID已存在")
    })
    @PostMapping
    public ResponseEntity<Map<String, Object>> createMenu(@RequestBody MenuRequest request) {
        try {
            Menu createdMenu = menuService.createMenu(request);
            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(Map.of(
                        "success", true,
                        "message", "菜单创建成功",
                        "data", createdMenu
                    ));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of(
                        "success", false,
                        "message", e.getMessage()
                    ));
        }
    }

    @Operation(summary = "更新菜单", description = "根据菜单ID更新菜单信息")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "菜单更新成功"),
        @ApiResponse(responseCode = "404", description = "菜单不存在")
    })
    @PutMapping("/{menuId}")
    public ResponseEntity<Map<String, Object>> updateMenu(
            @Parameter(description = "菜单ID", required = true)
            @PathVariable String menuId,
            @RequestBody MenuRequest request) {
        Optional<Menu> updatedMenu = menuService.updateMenu(menuId, request);
        if (updatedMenu.isPresent()) {
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "菜单更新成功",
                "data", updatedMenu.get()
            ));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of(
                    "success", false,
                    "message", "菜单不存在: " + menuId
                ));
    }

    @Operation(summary = "删除菜单", description = "根据菜单ID删除菜单")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "菜单删除成功"),
        @ApiResponse(responseCode = "404", description = "菜单不存在")
    })
    @DeleteMapping("/{menuId}")
    public ResponseEntity<Map<String, Object>> deleteMenu(
            @Parameter(description = "菜单ID", required = true)
            @PathVariable String menuId) {
        boolean deleted = menuService.deleteMenu(menuId);
        if (deleted) {
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "菜单删除成功"
            ));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of(
                    "success", false,
                    "message", "菜单不存在: " + menuId
                ));
    }

    @Operation(summary = "获取菜单数量", description = "获取系统中菜单的总数量")
    @ApiResponse(responseCode = "200", description = "成功获取菜单数量")
    @GetMapping("/count")
    public ResponseEntity<Map<String, Object>> getMenuCount() {
        int count = menuService.getMenuCount();
        return ResponseEntity.ok(Map.of(
            "count", count
        ));
    }
}
