-- user permissions 用户权限
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (101, 'user_add', '添加用户', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (102, 'user_delete', '删除用户', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (103, 'user_update_owner', '更新个人信息', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (104, 'user_update_all', '更新用户信息', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (105, 'user_modify', '修改用户', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (106, 'user_get_owner', '查看个人信息', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (107, 'user_get_list', '查看所有用户信息和列表', '{}');

-- group permissions 组权限
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (201, 'group_add', '添加用户组', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (202, 'group_delete', '删除用户组', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (203, 'group_update', '更新用户组', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (204, 'group_modify', '修改用户组', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (205, 'group_get_list', '查看用户组和用户组列表', '{}');

-- role permissions 角色权限
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (301, 'role_add', '添加角色', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (302, 'role_delete', '删除角色', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (303, 'role_update', '更新角色', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (304, 'role_modify', '修改角色', '{}');
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (305, 'role_get_list', '查看角色和角色列表', '{}');

-- permission
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (401, 'permission_get_list', '查看权限和权限列表', '{}');

-- dashboard
INSERT INTO permissions (id, name, `desc`, `ctime`) VALUES (501, 'dashboard', '查看dashboard', '{}');

-- default superuser / role
INSERT INTO users (id, `name`, `cname`, `email`, `phone_number`, `pwd_hash`, `is_super`, `status`, `ctime`) values (1, 'admin', 'admin', 'admin@admin.com', '13888888888', 'pbkdf2:sha256:150000$ymlosmY7$184ddd6854ef11252a8a0f5b78511773548bb5e9ccf7460360d936d4b72e8bf1', True, True, '{}');
INSERT INTO roles (id, name, `desc`, `ctime`) VALUES (1, '账户管理员', '账户管理者,可以对用户/用户组进行增删改查操作', '{}');
INSERT INTO roles (id, name, `desc`, `ctime`) VALUES (2, '系统默认角色', '所有用户都应该拥有该角色', '{}');
INSERT INTO role_permission (`role_id`, `permission_id`) VALUES (1, 101), (1, 102), (1, 103), (1, 104), (1, 105), (1, 106), (1, 107), (1, 201), (1, 202), (1, 203), (1, 204), (1, 205),  (1, 305), (1, 501);
INSERT INTO role_permission (`role_id`, `permission_id`) VALUES (2, 103), (2, 106), (2, 501);
