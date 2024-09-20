****
<h1 align="center">WaitAdmin (Python) 通用管理系统</h1>

<p align="center">
<a href="https://www.tslang.cn/"><img src="https://img.shields.io/badge/TypeScript-3-294e80" alt="wa"></a>
<a href="#"><img src="https://img.shields.io/badge/Vue.js-3-4eb883" alt="wa"></a>
<a href="#"><img src="https://img.shields.io/badge/Element Plus-2-409eff" alt="wa"></a>
<a href="https://www.nuxtjs.cn/"><img src="https://img.shields.io/badge/Nuxt.js--18bc78" alt="wa"></a>
</p>

<p align="center">
<a href="https://mp.weixin.qq.com/"><img src="https://img.shields.io/badge/微信-公众号-05ce66" alt="wa"></a>
<a href="https://mp.weixin.qq.com/"><img src="https://img.shields.io/badge/微信-小程序-05ce66" alt="wa"></a>
<a href="https://pay.weixin.qq.com/"><img src="https://img.shields.io/badge/微信-支付API3-05ce66" alt="wa"></a>
<a href="https://open.weixin.qq.com/"><img src="https://img.shields.io/badge/微信-开放平台-05ce66" alt="wa"></a>

</p>
<p align="center">
<a href="https://cloud.tencent.com/"><img src="https://img.shields.io/badge/腾讯云-COS-00a3ff" alt="wa"></a>
<a href="https://www.qiniu.com/"><img src="https://img.shields.io/badge/七牛云-OSS-07beff" alt="wa"></a>
<a href="https://www.aliyun.com/"><img src="https://img.shields.io/badge/阿里云-OSS-ff6a00" alt="wa"></a>
</p>
<p align="center">
<a href="https://cloud.tencent.com/"><img src="https://img.shields.io/badge/腾讯云-短信-00a3ff" alt="wa"></a>
<a href="https://www.aliyun.com/"><img src="https://img.shields.io/badge/阿里云-短信-ff6a00" alt="wa"></a>
</p>

**项目概述** <br/>
WaitAdmin(Python)是一个采用现代技术栈构建的权限控制后台管理系统，旨在为企业提供高效、安全、易扩展的后台解决方案。
该项目由个人开发者独立开发，无法与企业级团队开发的项目在规模和资源上相提并论，是否合适需自行衡量。
系统前端采用Vue 3框架结合TypeScript，保证了界面的流畅性和代码的可维护性；
后端则选用FastAPI，以其高性能和易开发的特点，为系统提供了强大的后端支持。<br/>

PS: 业余Python开发者, 项目采用PHP常见的MVC结构, 如觉得不合适请止步。

**商用说明** <br/>
- MIT开源协议, 允许免费商用。

**在线体验**
- 官方网站：<a href="https://www.waitadmin.cn" target="_blank">https://www.waitadmin.cn</a>
- 前台演示：<a href="https://python-demo.waitadmin.cn" target="_blank">https://python-demo.waitadmin.cn</a>
- 后台演示：<a href="https://python-demo.waitadmin.cn/admin" target="_blank">https://python-demo.waitadmin.cn/admin</a>

**后台账号**
- 登录账号：test
- 登录密码：123456

**环境要求**

| 运行环境   | 要求版本     | 推荐版本     |
|:-------|:---------|:---------|
| Python | >=3.10.* | 3.10.*   |
| Mysql  | >=5.7    | 5.7      |
| Nginx  | 无限制      | 最新LTS版   |
| Node   | >=20.*   | v20.14.0 |


## 技术架构
- **后台端：** Vue3 + TypeScript + Pinia + Element Plus
- **前台端：** NuxtJs3 + TypeScript + Pinia + Element Plus
- **接口端：** FastAPI + Pydantic + Tortoise-orm
- **数据库：** MySQL>=5.7
- **缓存层：** Redis
- **服务部署：** Nginx

## 主要特性
- 路由自动根据目录自动注册
- 采用常见的MVC结构(上手更容易)
- 内置基于RBAC的权限管理的功能
- 开箱即用,内置常用的工具和组件

## 内置功能
- 用户管理：该功能主要完成系统用户配置。
- 部门管理：配置系统组织机构(公司、部门、小组)
- 岗位管理：配置系统用户所属担任职务。
- 菜单管理：配置系统菜单操作权限访问路径等。
- 角色管理：配置角色菜单权限分配
- 邮件配置：配置电子邮件发送功能
- 操作日志：系统操作日志记录和查询
- 定时任务：管理定时任务的(新增、修改、删除)
- 系统缓存：管理系统产生的缓存(可自行清理)
- 附件管理：管理用户上传的图片和视频
- 文章管理：管理文章的(新增、修改、删除)
- 文件存储：管理文件的存储(本地存储、阿里云OSS、腾讯云OSS、七牛云OSS)
- 操作日志 记录用户的登录、操作等日志信息，便于追踪和审计。
- 接口文档 FastAPI自动生成的Swagger UI接口文档，方便前后端开发人员对接。
- ....

## 🚀 快速开始

**(1) 克隆项目代码：**
```shell
git clone https://gitee.com/wafts/waitadmin-python.git
cd waitadmin-python
```

**(2) 创建虚拟环境 (可选)：**
```shell
# 以下为Linux下创建虚拟环境, 如果Windows激活有一点点不一样。
# 如果您不了解虚拟环境, 建议您百度了解一下, 这在项目中很常见。

wa# python3 -m venv venv

wa# source venv/bin/activate
```

**(3) 安装核心依赖 (必选)：**
- 如果安装很慢,或者失败情况,请切换到国内源,或使用魔法。
```shell
# 注意要进入到server目录
cd waitadmin-python/server

pip3 install -r requirements.txt
```

**(4) 导入数据结构：**
- 1、首先你先要创建一个数据库,字符集建议使用 `utf8mb4`, 如我创建的库是: `ts_wa`
- 2、数据结构文件在 `server/sql/install.sql`
- 3、使用`Navicat`之类的工具, 把`install.sql`导入到创建的`ts_wa`数据库里。

**(5) 修改配置文件：**
- 在`server`根目录下载的`.example.env`, 复制该示例创建最终生效的`.env`文件
```shell
  cp .example.env .env
```
然后在`.env`修改里面的配置信息, 修改Mysql连接配置项,Redis配置, 根据需要自己实际情况进行修改。
```
# .env文件的内容示例

APP_DEBUG=False              # 调试模式,生成环境建议关闭

SERVER_HOST=0.0.0.0          # 服务监听地址
SERVER_PORT=8200             # 服务监听端口
SERVER_RELOAD=True           # 服务监听重启
SERVER_WORKERS=4             # 服务的进程数

MYSQL_HOST=127.0.0.1         # Mysql地址
MYSQL_PORT=3306              # Mysql端口
MYSQL_USERNAME=root          # Mysql账号
MYSQL_PASSWORD=root          # Mysql密码
MYSQL_DATABASE=ts_wa         # Mysql数据库
MYSQL_PREFIX=wait_           # Mysql表前缀
MYSQL_MINSIZE=1              # 最少链接数
MYSQL_MAXSIZE=100            # 最大链接数
MYSQL_CHARSET=utf8mb4        # 字符编码
MYSQL_ECHO=False             # 打印SQL

REDIS_HOST=127.0.0.1         # Redis地址
REDIS_PORT=6379              # Redis端口
REDIS_USERNAME=''            # Redis账号
REDIS_PASSWORD=''            # Redis密码
```

**(6) 运行项目：**
```shell
python3 manager.py
```
```shell
# 看到以下信息则表示运行成功了
INFO:     Will watch for changes in these directories: ['/Applications/waitadmin-python/server']
INFO:     Uvicorn running on http://0.0.0.0:8100 (Press CTRL+C to quit)
INFO:     Started reloader process [4614] using StatReload
INFO:     Started server process [4617]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**(7) 完毕：**
```
1、以上就是服务端的启动方式 (server)。
2、后台(admin) 与 前台(nuxtjs), 请自行按照 vue 那一套流程进行启动。
    cd admin
    npm install
    npm run dev
```

## 演示图
<table>
    <tr>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_001.png" height="200" width="400" alt="wa"/></td>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_002.png" height="200" width="400" alt="wa"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_003.png" height="200" width="400" alt="wa"/></td>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_004.png" height="200" width="400" alt="wa"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_005.png" height="200" width="400" alt="wa"/></td>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_006.png" height="200" width="400" alt="wa"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_007.png" height="200" width="400" alt="wa"/></td>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_008.png" height="200" width="400" alt="wa"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_009.png" height="200" width="400" alt="wa"/></td>
        <td><img src="https://gitee.com/wafts/waitadmin-python/raw/develop/server/public/static/default/example/ys_010.png" height="200" width="400" alt="wa"/></td>
    </tr>
</table>

## 交流群
QQ群：
<a href="https://gitee.com/link?target=https://jq.qq.com/?_wv=1027&k=TRrklD6W">
    <img src="https://img.shields.io/badge/613667155-blue.svg" alt="加入QQ群">
</a>
