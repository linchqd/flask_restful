-- user permissions 用户权限
INSERT INTO permissions (id, name, `desc`) VALUES (101, 'user_add', '添加用户');
INSERT INTO permissions (id, name, `desc`) VALUES (102, 'user_delete', '删除用户');
INSERT INTO permissions (id, name, `desc`) VALUES (103, 'user_update_owner', '更新个人信息');
INSERT INTO permissions (id, name, `desc`) VALUES (104, 'user_update_all', '更新用户信息');
INSERT INTO permissions (id, name, `desc`) VALUES (105, 'user_modify', '修改用户');
INSERT INTO permissions (id, name, `desc`) VALUES (106, 'user_get_owner', '查看个人信息');
INSERT INTO permissions (id, name, `desc`) VALUES (107, 'user_get_list', '查看所有用户信息和列表');

-- group permissions 组权限
INSERT INTO permissions (id, name, `desc`) VALUES (201, 'group_add', '添加用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (202, 'group_delete', '删除用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (203, 'group_update', '更新用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (204, 'group_modify', '修改用户组');
INSERT INTO permissions (id, name, `desc`) VALUES (205, 'group_get_list', '查看用户组和用户组列表');

-- role permissions 角色权限
INSERT INTO permissions (id, name, `desc`) VALUES (301, 'role_add', '添加角色');
INSERT INTO permissions (id, name, `desc`) VALUES (302, 'role_delete', '删除角色');
INSERT INTO permissions (id, name, `desc`) VALUES (303, 'role_update', '更新角色');
INSERT INTO permissions (id, name, `desc`) VALUES (304, 'role_modify', '修改角色');
INSERT INTO permissions (id, name, `desc`) VALUES (305, 'role_get_list', '查看角色和角色列表');

-- permission
INSERT INTO permissions (id, name, `desc`) VALUES (401, 'permission_get_list', '查看权限和权限列表');
