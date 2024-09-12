export enum errorEnum {
    SUCCESS = 0,                // 成功
    FAILED = 1,                 // 失败
    TOKEN_EMPTY = 310,          // token参数为空
    TOKEN_VALID = 311,          // token参数无效
    PARAMS_TYPE_ERROR = 320,    // 参数类型错误
    PARAMS_VALID_ERROR = 321,   // 参数校验错误
    PARAMS_ASSERT_ERROR = 322,  // 断言参数错误
    PERMISSIONS_ERROR = 403,    // 无相关的权限
    REQUEST_404_ERROR = 404,    // 请求接口丢失
    REQUEST_405_ERROR = 405,    // 请求方法错误
    SYSTEM_UNKNOWN_ERROR = 500, // 系统未知错误
    SYSTEM_TIMEOUT_ERROR = 504, // 网络请求超时
    DB_CONNECT_ERROR = 600,     // 数据库连接异常
    DB_EMPTY_DATA_ERROR = 601   // 查询数据不存在
}
