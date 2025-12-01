/**
 * 管理员列表类型
 */
interface AuthAdminListResponse {
    // ID
    id: number;
    // 所属角色
    role: string;
    // 所属部门
    dept: string;
    // 用户头像
    avatar: string;
    // 用户昵称
    nickname: string;
    // 登录账号
    username: string;
    // 联系电话
    mobile: string;
    // 电子邮箱
    email: string;
    // 是否禁用
    is_disable: boolean;
    // 最后登录IP
    last_login_ip: string;
    // 最后登录时间
    last_login_time: string;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 管理员自身类型
 */
interface AuthAdminOneselfResponse {
    // 用户
    user: {
        // ID
        id: number;
        // 角色ID
        role_id: number;
        // 部门ID
        dept_id: number;
        // 岗位ID
        post_id: number;
        // 用户头像
        avatar: string;
        // 用户昵称
        nickname: string;
        // 登录账号
        username: string;
        // 联系电话
        mobile: string;
        // 电子邮箱
        email: string;
        // 角色名称
        role: string;
        // 是否禁用: [0=否, 1=是]"
        is_disable: number;
    };
    // 权限
    perms: string[];
    // 菜单
    menus: AuthAdminMenuResponse[];
}

/**
 * 管理员菜单类型
 */
interface AuthAdminMenuResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 权限类型: [M,C,A]
    type: string;
    // 菜单名称
    name: string;
    // 菜单图标
    icon: string;
    // 权限标识
    perms: string;
    // 路由参数
    params: string;
    // 组件路径
    component: string;
    // 路由地址
    path: string;
    // 是否显示
    is_show: boolean;
    // 是否禁用
    is_disable: boolean;
    // 子菜单
    children: AuthAdminMenuResponse[];
}

/**
 * 管理员详情类型
 */
interface AuthAdminDetailResponse {
    // ID
    id: number;
    // 角色ID
    role_id: number;
    // 部门ID
    dept_id: number;
    // 岗位ID
    post_id: number;
    // 用户头像
    avatar: string;
    // 用户昵称
    nickname: string;
    // 登录账号
    username: string;
    // 联系电话
    mobile: string;
    // 电子邮箱
    email: string;
    // 角色名称
    role: string;
    // 是否禁用
    is_disable: boolean;
}
