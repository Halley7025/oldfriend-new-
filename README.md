**老友助手｜本地启动 README**

这是啊队队队小组完成的“老友助手”小程序项目，包含前端小程序（WeChat 小程序）、后端（Spring Boot）和数据库脚本。
---

## 环境要求
- Git、PowerShell（或终端）
- MySQL 8.x（必需）；Redis（可选，用于会话/缓存）
- JDK 17、Maven 3.8+（已含在 `start_backend.ps1` 自动调用）
- 微信开发者工具（用于打开 `minicode-1`）

## 快速开始（推荐）

### 步骤1：检查MySQL服务
首先确认MySQL服务正在运行：
```powershell
Get-Service -Name "MySQL*" -ErrorAction SilentlyContinue | Select-Object Name, Status
```
- 如果服务状态为 `Running`，继续下一步
- 如果服务未启动，请先启动MySQL服务

### 步骤2：初始化数据库
创建数据库并导入脚本（首次运行必须执行）：
```bash
mysql -u root -p
CREATE DATABASE elderly_assistant DEFAULT CHARSET utf8mb4;
USE elderly_assistant;
SOURCE database/init_database.sql;
SOURCE database/insert_test_data.sql;
```
**注意**：
- 记住你的MySQL密码，下一步配置后端时需要用到
- 可选数据：`database/fujian_hospitals.sql`、`database/quick_import_hospitals.sql` 可按需导入

### 步骤3：配置后端数据库连接
编辑 [java-backend/src/main/resources/application.yml](java-backend/src/main/resources/application.yml)：
```yaml
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/elderly_assistant?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    username: root           # 改为你的MySQL名
    password: YOUR_PASSWORD    # 改为你的MySQL密码
```
**其他可选配置**：
- Redis配置（可选）
- 百度语音API密钥（用于语音支付功能）
- 微信小程序配置（用于获取用户手机号）

### 步骤4：启动后端服务
方法一：
在文件夹根目录输入
```powershell

.\start_backend.ps1
# 如无法运行，用方法二
```
方法二：
```powershell
# 进入后端目录
cd java-backend

# 清理并打包（第一次或代码修改后执行）
mvn clean package -DskipTests

# 启动服务
java -jar target\assistant-backend-1.0.0.jar
```

**✅ 启动成功标志：**
```
  ____  _             _           _ 
 / ___|| |_ __ _ _ __| |_ ___  __| |
 \___ \| __/ _` | '__| __/ _ \/ _` |
  ___) | || (_| | |  | ||  __/ (_| |
 |____/ \__\__,_|_|   \__\___|\__,_|

老友助手后端服务启动成功！
访问 Swagger 文档: http://localhost:8080/doc.html
```

**注意**：保持终端窗口打开，服务会在后台持续运行

### 步骤5：获取本机IP地址
打开新的PowerShell终端，执行以下命令：
```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*WLAN*" -or $_.InterfaceAlias -like "*以太网*"} | Where-Object {$_.IPAddress -notlike "169.254.*"} | Select-Object IPAddress, InterfaceAlias
```
**结果示例**：
```
IPAddress       InterfaceAlias
---------       --------------
192.168.56.1    以太网
10.133.83.187   WLAN
```
- 如果使用WiFi连接，记下 **WLAN** 对应的IP地址
- 如果使用网线连接，记下 **以太网** 对应的IP地址

### 步骤6：配置前端API地址
编辑 [minicode-1/utils/config.js](minicode-1/utils/config.js)，将 `apiBaseUrl` 改为你的IP地址：
```javascript
const DEV_CONFIG = {
  // 将下面的IP改为步骤5中获取的WLAN地址
  apiBaseUrl: 'http://10.133.83.187:8082/api',  // 替换为你的实际IP
  timeout: 10000,
  useMock: false
};
```

### 步骤7：启动微信小程序
1. 打开**微信开发者工具**
2. 选择"导入项目"
3. 项目目录选择：`oldfriend\minicode-1`
4. 点击**编译**按钮

**真机调试**：
- 确保手机和电脑连接同一个WiFi网络（推荐使用手机热点）
- 在微信开发者工具中点击"预览"，用手机扫真机调试的码即可
- 如果手机无法访问，检查Windows防火墙是否放行8082端口

---

## 验证启动成功

✅ **后端验证**：
- 在浏览器访问：`http://localhost:8082/api`
- 应该看到Spring Boot的欢迎页面或404页面（说明服务已启动）

✅ **前端验证**：
- 在微信开发者工具的"控制台"中查看网络请求
- 如果看到请求成功返回数据，说明前后端连接正常

✅ **完整测试**：
- 在小程序中尝试使用生活缴费、打车等功能
- 查看后端终端是否有请求日志输出

## 如需测试联系物业功能
- 可在前端`minicode-1\pages\Emergency_safety`文件夹中
- 找到`Emergency_safety.js`文件
```javascript
Page({
    data: {
      fontSizes: {},
      currentLocation: '正在定位...',
      latitude: null,
      longitude: null,
      propertyPhone: '18350587025', // 物业联系电话（修改为自己的手机号即可）
      emergencyContacts: [] // 自定义紧急联系人
    }
```
## 常见问题速查

### 问题1：后端启动失败
**症状**：执行 `.\start_backend.ps1` 后报错

**解决方案**：
- **Maven未安装**：下载并安装 Maven 3.8+，配置环境变量
- **JDK版本不对**：确保安装JDK 17或以上版本
- **MySQL连接失败**：
  - 检查MySQL服务是否启动：`Get-Service -Name "MySQL*"`
  - 检查 `application.yml` 中的数据库密码是否正确
  - 确认数据库 `elderly_assistant` 已创建

### 问题2：前端无法连接后端
**症状**：小程序请求失败，控制台显示网络错误

**解决方案**：
- **检查后端是否启动**：浏览器访问 `http://localhost:8082/api`
- **IP地址配置错误**：
  - 重新执行步骤5获取IP地址
  - 更新 `minicode-1/utils/config.js` 中的 `apiBaseUrl`
- **防火墙阻止**：
  ```powershell
  # 允许8082端口入站
  New-NetFirewallRule -DisplayName "老友助手后端" -Direction Inbound -LocalPort 8082 -Protocol TCP -Action Allow
  ```
- **手机与电脑不在同一网络**：确保连接同一个WiFi

### 问题3：编译时间过长
**症状**：`mvn clean package` 执行很久

**解决方案**：
- 首次编译需要下载依赖，可能需要5-15分钟
- 配置Maven国内镜像加速（阿里云镜像）
- 后续启动会快很多（约10秒）

### 问题4：端口被占用
**症状**：提示 "Port 8082 is already in use"

**解决方案**：
```powershell
# 查找占用8082端口的进程
netstat -ano | findstr :8082

# 结束进程（替换<PID>为实际进程ID）
taskkill /F /PID <PID>
```
或修改 `application.yml` 中的 `server.port` 为其他端口（如8083），同时更新前端配置

### 问题5：数据库导入失败
**症状**：执行 `SOURCE` 命令时报错

**解决方案**：
- 使用绝对路径：
  ```sql
  SOURCE C:/Users/26367/Desktop/新建文件夹/database/init_database.sql;
  ```
- 确保SQL文件编码为UTF-8
- 检查MySQL版本是否为8.0+

---

## 停止服务

### 停止后端服务
- 在运行 `start_backend.ps1` 的终端窗口按 `Ctrl + C`
- 或关闭该终端窗口

### 停止MySQL服务（可选）
```powershell
Stop-Service -Name "MySQL*"
```

---

## 快速重启

如果环境已配置好，后续启动只需：
1. 确保MySQL服务运行
2. 执行 `.\start_backend.ps1`
3. 打开微信开发者工具，编译运行

## 目录速览
- `minicode-1/`：微信小程序前端。
- `java-backend/`：Spring Boot 后端代码与配置。
- `database/`：建表与示例数据脚本。
- `start_backend.ps1`：后端启动脚本（Windows / PowerShell）。
- `deploy_fix.ps1`：部署辅助脚本。
- `code/`、`minicode-1/` 等其他演示/测试代码。


##  质量保障 (Quality Assurance)

> **特别说明：** 简历中所提及的全流程测试管理体系、自动化测试框架、以及性能压测相关工作，由于原本在企业/团队内部私有仓库进行，为配合开源展示，近期已将相关的测试代码（API/UI自动化、JMeter脚本）、CI/CD 流水线配置脱敏并迁移至本项目 	ests 与 .github 目录下进行公开。我们采用 GitHub Actions 实现每次提交的自动化验证，大幅缩短回归测试周期。

