package com.sci.risk.repository;

import com.sci.risk.model.entity.Menu;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public class MenuRepository {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public MenuRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    private static final RowMapper<Menu> MENU_ROW_MAPPER = new RowMapper<Menu>() {
        @Override
        public Menu mapRow(ResultSet rs, int rowNum) throws SQLException {
            Menu menu = new Menu();
            menu.setMenuId(rs.getString("menu_id"));
            menu.setMenuName(rs.getString("menu_name"));
            menu.setMenuCode(rs.getString("menu_code"));
            menu.setParentId(rs.getString("parent_id"));
            menu.setRoutePath(rs.getString("route_path"));
            menu.setIcon(rs.getString("icon"));
            menu.setSortOrder(rs.getObject("sort_order") != null ? rs.getInt("sort_order") : 0);
            menu.setIsVisible(rs.getBoolean("is_visible"));
            menu.setPermission(rs.getString("permission"));
            menu.setComponent(rs.getString("component"));

            java.sql.Timestamp createdAt = rs.getTimestamp("created_at");
            if (createdAt != null) {
                menu.setCreatedAt(createdAt.toLocalDateTime());
            }
            java.sql.Timestamp updatedAt = rs.getTimestamp("updated_at");
            if (updatedAt != null) {
                menu.setUpdatedAt(updatedAt.toLocalDateTime());
            }
            return menu;
        }
    };

    public List<Menu> findAll() {
        String sql = "SELECT * FROM menu ORDER BY sort_order ASC, menu_id ASC";
        return jdbcTemplate.query(sql, MENU_ROW_MAPPER);
    }

    public List<Menu> findByParentId(String parentId) {
        String sql = "SELECT * FROM menu WHERE parent_id = ? ORDER BY sort_order ASC";
        return jdbcTemplate.query(sql, MENU_ROW_MAPPER, parentId);
    }

    public List<Menu> findRootMenus() {
        String sql = "SELECT * FROM menu WHERE parent_id = '0' OR parent_id IS NULL ORDER BY sort_order ASC";
        return jdbcTemplate.query(sql, MENU_ROW_MAPPER);
    }

    public Menu findById(String menuId) {
        String sql = "SELECT * FROM menu WHERE menu_id = ?";
        List<Menu> results = jdbcTemplate.query(sql, MENU_ROW_MAPPER, menuId);
        return results.isEmpty() ? null : results.get(0);
    }

    public Menu findByMenuCode(String menuCode) {
        String sql = "SELECT * FROM menu WHERE menu_code = ?";
        List<Menu> results = jdbcTemplate.query(sql, MENU_ROW_MAPPER, menuCode);
        return results.isEmpty() ? null : results.get(0);
    }

    public int insert(Menu menu) {
        String sql = "INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component) " +
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        return jdbcTemplate.update(sql,
            menu.getMenuId(),
            menu.getMenuName(),
            menu.getMenuCode(),
            menu.getParentId() != null ? menu.getParentId() : "0",
            menu.getRoutePath(),
            menu.getIcon(),
            menu.getSortOrder() != null ? menu.getSortOrder() : 0,
            menu.getIsVisible() != null ? menu.getIsVisible() : true,
            menu.getPermission(),
            menu.getComponent()
        );
    }

    public int update(Menu menu) {
        String sql = "UPDATE menu SET menu_name = ?, menu_code = ?, parent_id = ?, route_path = ?, icon = ?, " +
                     "sort_order = ?, is_visible = ?, permission = ?, component = ?, updated_at = CURRENT_TIMESTAMP " +
                     "WHERE menu_id = ?";
        return jdbcTemplate.update(sql,
            menu.getMenuName(),
            menu.getMenuCode(),
            menu.getParentId(),
            menu.getRoutePath(),
            menu.getIcon(),
            menu.getSortOrder(),
            menu.getIsVisible(),
            menu.getPermission(),
            menu.getComponent(),
            menu.getMenuId()
        );
    }

    public int deleteById(String menuId) {
        String sql = "DELETE FROM menu WHERE menu_id = ?";
        return jdbcTemplate.update(sql, menuId);
    }

    public int count() {
        String sql = "SELECT COUNT(*) FROM menu";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class);
        return count != null ? count : 0;
    }

    public boolean existsById(String menuId) {
        String sql = "SELECT COUNT(*) FROM menu WHERE menu_id = ?";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class, menuId);
        return count != null && count > 0;
    }
}
