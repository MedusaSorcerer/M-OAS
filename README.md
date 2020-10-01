![MedusaSorcerer的博客](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/05a55861c9064f50895842981b1f0db2~tplv-k3u1fbpfcp-zoom-1.image)
---

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> 前言

这是我的 <span style="color: red">第100篇</span> 博文,
选择了我自己撰写并设计的一款 OA 平台 - **M&OAS**,
项目会持续迭代更新,
也感各位大神们支持。

* <a href="https://juejin.im/post/6878485351153795080" style="text-decoration:none">juejin.im <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1a70bd3f4b0b43a799c2b7c242da9e01~tplv-k3u1fbpfcp-zoom-1.image"></a>
* <a href="https://moasdocs.github.io" style="text-decoration:none">Document <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1a70bd3f4b0b43a799c2b7c242da9e01~tplv-k3u1fbpfcp-zoom-1.image"></a>

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> UI 预览

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d49b76a5532f417a98edba8bf163941f~tplv-k3u1fbpfcp-zoom-1.image)

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> 简介

第一次设计产品,
来源也是想尝试着拓展自己的产品设计思维,
当然,
不可否认的是产品设计的样式,
可能是千篇一律,
只是在功能上得到启发和创新,
以及更好的用户体验。

项目 **M&OAS**(M & Office Automation Service) 致力开发出完善的自动化办公服务,
推崇更方便快捷的办公环境,
目前(2020-10-01)为 `version 1.0.1` 版。

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> 功能罗列

目前版本中包含了以下版本：
* Dashboard：数据可视化
* 流程处理：流程提交和审批
* 考勤处理：考勤查询以及考勤异常填补、假期申请
* 工作报告：工作日报填报, 内容项目组可见
* 用户配置：用户管理界面, 包含用户、项目组的查询和修改 *(推荐使用对接 AD 域)*
* 知识库：*待开发*
* 系统设置：个人信息设置、个人安全信息设置以及管理员可见的系统数据配置

目前由于时间问题,
知识库板块处于待开发阶段,
后期将补充完善。

项目前端采用 `Layui` 作为基础框架,
并采用了 `OKadmin2.0` 作为二次框架开发,
得以实现整个前端项目。

项目后端采用 `Django` 作为基础框架,
并使用 `django-restframework` 作为嵌套框架开发,
得以实现整个后端项目。

项目采用前后端分离式,
并使用了 `MySQL` 数据库作为 ORM(Object Relational Mapping),

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> 依赖安装
#### 后端项目
部署后端项目时你可能需要 Python3.8+ 版本,
使用 Python 安装相关依赖库：
```shell
python3 -m pip install -r requirements.txt
```
安装 MySQL 并创建数据库,
将 `databaseName` 替换成你需要自定义的数据库名称：
```sql
CREATE DATABASE databaseName DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
将相关数据配置写入配置文件：
```shell
vi ./conf/conf.py
```
生成数据表：
```shell
python3 maigration.py
```
配置邮件提醒相关配置,
或启动后使用管理员账户登录平台界面修改：
```shell
vi ./conf/conf.json
```

### <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1893e46d114b998122077202c5b611~tplv-k3u1fbpfcp-zoom-1.image"> 启动

尝试启动：
```shell
python3 manage.py runserver 0.0.0.0:8000
```
uWSGI 启动：
```shell
uwsgi --ini uwsgi.ini
```
uWSGI 停止：
```shell
uwsgi --stop uwsgi.pid
pkill -9 uwsgi
```

注意前端代码,
优先将其打包后再发布,
并可以使用 Nginx 服务器进行代理。

更多部署问题请 [点击这里](https://juejin.im/post/6850418118938853389)。

<br><br>

> 内容未详细标注,
想查阅更加详细的文档信息,
请跳转到文档界面。