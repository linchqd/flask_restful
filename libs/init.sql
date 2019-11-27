-- user permissions 用户权限
INSERT INTO permissions (id, name, `desc`) VALUES (101, 'user_post', '添加用户');
INSERT INTO permissions (id, name, `desc`) VALUES (102, 'user_delete', '删除用户');
INSERT INTO permissions (id, name, `desc`) VALUES (103, 'user_put', '更新用户');
INSERT INTO permissions (id, name, `desc`) VALUES (104, 'user_patch', '修改用户');
INSERT INTO permissions (id, name, `desc`) VALUES (105, 'user_get', '查看用户和用户列表');

-- group permissions 组权限
INSERT INTO permissions (id, name, `desc`) VALUES (201, 'group_post', '添加用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (202, 'group_delete', '删除用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (203, 'group_put', '更新用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (204, 'group_patch', '修改用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (205, 'group_get', '查看用户组和用户组列表');

-- role permissions 角色权限
INSERT INTO permissions (id, name, `desc`) VALUES (301, 'role_post', '添加角色');
INSERT INTO permissions (id, name, `desc`) VALUES (302, 'role_delete', '删除角色');
INSERT INTO permissions (id, name, `desc`) VALUES (303, 'role_put', '更新角色');
INSERT INTO permissions (id, name, `desc`) VALUES (304, 'role_patch', '修改角色');
INSERT INTO permissions (id, name, `desc`) VALUES (305, 'role_get', '查看角色和角色列表');
