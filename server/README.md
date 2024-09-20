- ****
<h1 align="center">WaitAdmin (FastApi) 服务端</h1>

## 目录结构
```
├─📂 server
│  ├─📂 apps                 // 应用目录
│  │  ├─📂 admin             // 后台应用
│  │  │  ├─📂 routers        // 控制器
│  │  │  ├─📂 schemas        // 响应层
│  │  │  ├─📂 service        // 逻辑层
│  │  │  ├─📄 config.py      // 配置
│  │  │  ├─📄 interceptor.py // 拦截器
│  │  │  ├─📄 middleware.py  // 中间键
│  │  ├─📂 api               // 前台应用
│  │  │  ├─📂 routers        // 控制器
│  │  │  ├─📂 schemas        // 响应层
│  │  │  ├─📂 service        // 逻辑层
│  │  │  ├─📄 config.py      // 配置
│  │  │  ├─📄 interceptor.py // 拦截器
│  │  │  ├─📄 middleware.py  // 中间键
│  │  ├─...
│  │
│  ├─📂 common              // 公共目录
│  │  ├─📂 enums            // 枚举目录
│  │  ├─📂 models           // 模型目录
│  │  ├─📂 utils            // 工具目录
│  │  ├─...
│  │
│  ├─📂 kernels             // 核心逻辑
│  │  ├─📄 cache.py          
│  │  ├─📄 database.py         
│  │  ├─📄 events.py            
│  │  ├─...
│  │
│  ├─📂 plugins           // 插件目录
│  │  ├─📂 mail           // 邮件服务
│  │  ├─📂 msg            // 消息服务
│  │  ├─📂 sms            // 短信服务
│  │  ├─📂 storage        // 存储服务
│  │  ├─📂 wechat         // 微信服务
│  │  ├─...
│  │
│  ├─📂 public            // 公开目录
│  │  ├─📂 static         // 静态文件目录
│  │  ├─📂 storage        // 资源存储目录
│  │  ├─...
│  │
│  ├─📂 sql                // 安装SQL
│  │  ├─📄 install.sql  
│  │
│  ├─📄 .env               // 环境配置
│  ├─📄 .example.env       // 配置模板
│  ├─📄 .gitignore         // Git配置
│  ├─📄 config.py          // 全局配置
│  ├─📄 events.py          // 事件管理
│  ├─📄 exception.py       // 异常管理
│  ├─📄 hypertext.py       // Http管理
│  ├─📄 manager.py         // 启动的文件
│  ├─📄 middleware.py      // 全局中间件
│  ├─📄 README.md          // README
│  ├─📄 requirement.txt    // 依赖包
```

## 依赖说明
```
python-dotenv
    用于从.env文件中加载环境变量到os.environ
python-multipart
    处理HTTP请求中(multipart/form-data)

fastapi
    高性能Web框架,用于构建API
fastapi-cache2
    一个FastAPI的缓存扩展,用于缓存API响应以提高性能
pydantic-settings
    使用Pydantic模型来管理应用的设置
tortoise-orm
    一个基于Pydantic和asyncio的ORM (异步操作)

aiosmtplib
    SMTP协议的异步客户端,用于发送电子邮件
aiofiles
    提供异步文件操作接口,用于异步读写文件

asyncpg
    PostgreSQL数据库的异步客户端
aiomysql
    MySQL数据库的异步客户端
aioredis
    Redis数据库的异步客户端
redis
    Redis数据库的同步客户端

oss2
    阿里云OSS(对象存储服务)的Python SDK, 用于与阿里云OSS进行交互。
qiniu
    七牛云OSS(对象存储服务)的Python SDK, 用于与七牛云存储服务进行交互
cos-python-sdk-v5
    腾讯云COS(对象存储)的Python SDK, 用于与腾讯云COS进行交互

alibabacloud_dysmsapi20170525
    阿里云短信服务的Python SDK, 用于发送短信
tencentcloud-sdk-python
    腾讯云服务的Python SDK, 提供了与腾讯云各种服务交互的接口
    
simpel_captcha
    一个简单的图片验证码生成库
APScheduler
   一个Python库, 用于在应用程序中调度任务(定时任务)
python-weixin
    可能是用于与微信API交互的库, 不是官方库
wechatpayv3
    微信支付V3版本的Python SDK, 用于与微信支付API进行交互
python-alipay-sdk
    支付宝的Python SDK, 用于与支付宝API进行交互
```

## 交流群
QQ群：
<a href="https://gitee.com/link?target=https://jq.qq.com/?_wv=1027&k=TRrklD6W">
    <img src="https://img.shields.io/badge/613667155-blue.svg" alt="加入QQ群">
</a>
