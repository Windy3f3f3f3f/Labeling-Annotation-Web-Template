# 易扩展的标注网页模板

一个前后端分离的标注网页模板，后端使用 Flask（Python）进行数据管理与 API 提供，前端使用 Vue 3（结合 Element-Plus）实现可视化界面和交互逻辑。

[English Document](./README.md)

![Home Page](./assets/home.png)

## 功能概览

### 1. 后端 (Flask + SQLite)
- 提供 RESTful API 接口，如获取下一条未标注数据、提交标注结果、获取标注进度等
- 内置打分标注逻辑：BaseAnnotation 基类，可以自定义打分逻辑
- 支持数据导入 (load_data.py) 与导出 (export_data.py) 到 JSON 文件
- 默认使用 SQLite 数据库进行数据持久化

### 2. 前端 (Vue 3 + Element-Plus)
- 使用 Vue CLI 初始化，内置路由、状态管理示例
- 集成 Element-Plus [https://element-plus.org/zh-CN/] 组件库，提供丰富的 UI 组件（表单、按钮、弹窗、进度条等）
- 提供典型的文本对比 + 打分标注界面 AnnotationView.vue，可在此基础上二次开发多种标注方式

### 3. 可扩展性

#### 后端：
- 在 annotation_types 文件夹下新增自定义逻辑类，继承 BaseAnnotation
- 修改或新增数据库表结构，以满足不同类型标注（多选标注、命名实体识别等）

#### 前端：
- 修改 views/AnnotationView.vue 或自建组件，扩展文本展示方式、按钮布局或打分维度
- 通过 Vuex 做全局状态管理（如用户信息、权限等），通过 Vue Router 增加新页面或功能模块

## 项目结构

```
.
├── .gitignore
├── RAEDME.md                        # 本文件
├── backend/
│   ├── app.py                       # Flask 入口，注册路由、启动服务
│   ├── config.py                    # 后端配置（数据库、服务器端口、CORS 等）
│   ├── load_data.py                 # 导入 JSON 数据到数据库
│   ├── export_data.py               # 导出数据库中标注结果为 JSON
│   ├── annotation_types/            # 存放标注逻辑类
│   │   ├── base.py                  # 标注逻辑基类
│   │   └── scoring.py               # 示例打分标注逻辑
│   ├── database/                    # 数据库相关工具
│   │   └── db_utils.py              # 数据库初始化、连接、建表
│   └── requirements.txt             # Python 依赖
├── frontend/
│   ├── package.json                 # 前端依赖
│   ├── public/
│   │   └── index.html               # 前端入口文件
│   ├── src/
│   │   ├── api/                     # axios 封装及后端交互
│   │   ├── constants/               # 全局配置
│   │   ├── layouts/                 # 布局组件
│   │   ├── views/                   # 视图组件
│   │   │   ├── AnnotationView.vue   # 标注界面示例（双文本打分）
│   │   │   └── HomeView.vue         # 示例首页
│   │   ├── store/                   # Vuex 状态管理
│   │   ├── router/                  # Vue Router 路由配置
│   │   └── main.ts                  # Vue 应用入口
│   └── vue.config.js                # 前端服务配置
└── ...
```

## 快速开始

### 0. 配置端口、ip等

- 修改 backend/config.py 中的 CORS.ORIGINS your_ip:port
- 修改 frontend/src/constants/config.ts 中的 API.BASE_URL your_ip:port

### 1. 启动后端 (Flask)

#### 安装依赖

```bash
cd backend
# 建议使用虚拟环境(venv/conda)隔离环境
conda create -n flask python=3.9
conda activate flask
pip install -r requirements.txt
```

#### 导入数据（第一次启动时需执行，后续启动时跳过）

```bash
python load_data.py --file data_to_load.json
```

将读取 JSON 内容并写入 annotation_data 数据表。可在 load_data.py 中根据字段需要自行扩展。

#### 启动后端服务

```bash
python app.py
```

成功后可访问 http://127.0.0.1:5000。该地址提供了类似 /api/annotation/next、/api/annotation/submit 等路由用于标注操作。

#### 导出标注结果（可选）

```bash
python export_data.py --output results.json
```

若不指定 --output，会自动生成带时间戳的文件名。

### 3. 启动前端 (Vue 3)

#### 安装依赖

```bash
cd ../frontend
npm install
```

#### 启动前端服务

```bash
npm run serve
```

默认会在 http://your_ip:8080 启动开发服务器（可在 vue.config.js 中更改端口）。

#### 访问标注页面
打开浏览器访问 http://your_ip:8080，即可看到示例标注界面。前端会调用后端提供的 API 来获取/提交标注数据。

## 如何自定义标注系统

### 1. 自定义标注逻辑
要实现新的标注类型(如多选标注、序列标注等),需要修改以下文件:

1. **backend/annotation_types/** 目录
   - 新建标注类型文件(如 multiple_choice.py)
   - 继承 base.py 中的 BaseAnnotation 类
   - 实现必要的方法(get_next_data, submit_annotation, get_progress)

2. **backend/database/db_utils.py**
   - 在 init_db() 函数中添加新的数据表定义
   - 根据新标注类型设计合适的表结构

3. **backend/app.py**
   - 导入新的标注类
   - 添加对应的 API 路由
   - 实现路由处理逻辑

### 2. 自定义前端界面
要实现新的标注界面,需要修改以下文件:

1. **frontend/src/views/**
   - 新建或修改视图组件(如 MultipleChoiceView.vue)
   - 实现标注界面的模板和交互逻辑

2. **frontend/src/router/routes.ts**
   - 添加新视图的路由配置
   - 设置路由参数和元信息

3. **frontend/src/api/annotation.ts**
   - 添加与新标注类型对应的 API 调用函数
   - 定义请求和响应的数据类型

4. **frontend/src/store/** (可选)
   - 如需要全局状态管理,添加新的 store 模块
   - 实现状态管理相关逻辑
   
### 3. 扩展数据导入导出
如果新的标注类型需要特殊的数据格式:

1. **backend/load_data.py**
   - 修改数据导入逻辑
   - 添加数据格式验证

2. **backend/export_data.py**
   - 修改数据导出逻辑
   - 调整导出文件格式


## 实际部署
由于是简单标注，应该不需要实际部署。

如果需要实际部署的话，要通过Nginx部署前端的静态文件，通过Gunicorn启动后端服务。

## 目前没支持的
- 用户登录等权限管理
- 标注结果可视化
