# Transaction业务功能包结构开发规范
 
## 目标
本规范定义了Transaction业务功能包的标准结构，确保代码组织清晰、职责分明，便于维护和扩展。
 
## 包结构概览
 
Transaction业务功能包采用分层架构设计，主要包含以下四个核心子包：
 
```
transaction/
├── base/              # 基础层：定义基础常量、接口和抽象类
├── common/            # 公共层：提供跨业务模块的通用功能；
├── core/              # 核心层：实现具体的业务功能模块
└── support/           # 支撑层：提供工具类、缓存、校验等支撑能力
```
 
## 详细包结构说明
 
### 1. base/ - 基础层
 
基础层定义Transaction模块的基础常量、基础模型和基础服务接口。
 
```
base/
├── constants/         # 常量定义
│   ├── ContextPath.java          # 上下文路径常量
│   └── ModuleTags.java           # 模块标签常量
├── controller/        # 基础控制器
│   
├── pojo/              # 基础数据对象
│   ├── bo/            # 业务对象
│   │   └── BaseTransactionBO.java
│   ├── dto/           # 数据传输对象
│   │   └── BaseTransactionDTO.java
│   └── vo/            # 视图对象
│       └── BaseTransactionVO.java
└── service/           # 基础服务接口
    ├── imp/           # 服务实现
    │   └── package-info.java
    └── package-info.java
```
 
**职责说明：**
- `constants/`: 存放Transaction模块的全局常量，如API路径、模块标识等
- `controller/`: 存放基础控制器类或抽象控制器
- `pojo/`: 存放基础数据模型，包括BO（业务对象）、DTO（数据传输对象）、VO（视图对象）
- `service/`: 存放基础服务接口和抽象实现
 
### 2. common/ - 公共层
 
公共层提供跨业务模块共享的通用功能，如协议查询、父交易ID处理、通用交易处理等。
 
```
common/
├── agreement/         # 协议相关公共功能
│   ├── controller/    # 协议查询控制器
│   │   └── QueryAgreementInformationController.java
│   ├── dao/           # 数据访问层
│   │   ├── entity/    # 实体类（预留）
│   │   └── mapper/    # MyBatis Mapper接口（预留）
│   ├── helper/        # 辅助类
│   │   ├── AgreementParser.java
│   │   └── QueryAgreementHelper.java
│   ├── pojo/          # 数据对象
│   │   ├── bo/        # 业务对象
│   │   │   └── QueryAgreementBO.java
│   │   ├── dto/       # 数据传输对象（预留）
│   │   └── vo/        # 视图对象
│   │       ├── AgreementVO.java
│   │       ├── CoverageVO.java
│   │       ├── LifeVO.java
│   │       └── PolicyVO.java
│   ├── service/       # 服务层
│   │   ├── impl/      # 服务实现
│   │   │   └── QueryAgreementServiceImpl.java
│   │   └── QueryAgreementService.java
│   └── package-info.java
├── parenttransactionid/  # 生成parentTransactionId
│   ├── controller/
│   ├── pojo/
│   ├── service/
│   └── package-info.java
└── transaction/       # 通用交易处理
    ├── dao/
    │   ├── entity/
    │   └── mapper/
    ├── pojo/
    │   ├── bo/
    │   ├── dto/
    │   └── vo/
    └── service/
        └── package-info.java
```
 
**职责说明：**
- `agreement/`: 提供协议信息查询的公共功能，供各业务模块复用
- `parenttransactionid/`: 提供parentTransactionId生成相关的逻辑
- `transaction/`: 提供通用的交易处理功能
 
### 3. core/ - 核心层
 
核心层实现具体的业务功能模块，每个子模块代表一个独立的业务领域。
 
```
core/
├── agreementinformation/  # 工单类型：协议信息
│   ├── controller/        # 控制器层
│   │   └── SubmitAgreementInformationController.java
│   ├── dao/               # 数据访问层
│   │   ├── entity/        # 实体类
│   │   │   ├── PaymentInformation.java
│   │   │   ├── PolicyInformation.java
│   │   │   ├── PolicyValue.java
│   │   │   └── PremiumInformation.java
│   │   └── mapper/        # MyBatis Mapper接口
│   │       ├── PaymentInformationMapper.java
│   │       ├── PolicyInformationMapper.java
│   │       ├── PolicyValueMapper.java
│   │       └── PremiumInformationMapper.java
│   ├── enums/             # 枚举定义
│   │   └── package-info.java
│   ├── pojo/              # 数据对象
│   │   ├── bo/            # 业务对象
│   │   │   └── AgreementInformationBO.java
│   │   ├── dto/           # 数据传输对象
│   │   │   └── AgreementInformationDTOBaseEnquiryInformationDTO.java
│   │   ├── vo/            # 视图对象
│   │   │   └── package-info.java
│   │   └── package-info.java
│   └── service/           # 服务层
│       ├── converter/     # 对象转换器（MapStruct）
│       │   └── AgreementInformationConverter.java
│       ├── helper/        # 辅助类
│       │   └── AgreementInformationHelper.java
│       ├── impl/          # 服务实现
│       │   └── AgreementInformationServiceImpl.java
│       ├── strategy/      # 策略模式实现
│       │   ├── CancelAgreementServiceStrategyImpl.java
│       │   ├── PaymentInformationServiceStrategyImpl.java
│       │   ├── PolicyInformationServiceStrategyImpl.java
│       │   ├── PolicyValueServiceStrategyImpl.java
│       │   └── PremiumInformationServiceStrategyImpl.java
│       └── AgreementInformationService.java
└── generalinformation/   # 工单类型：通用信息
    ├── controller/
    ├── dao/
    │   ├── entity/
    │   └── mapper/
    ├── enums/
    ├── pojo/
    │   ├── bo/
    │   ├── dto/
    │   └── vo/
    └── service/
        ├── converter/
        ├── helper/
        ├── impl/
        ├── strategy/
        └── package-info.java
```
 
**职责说明：**
- `agreementinformation/`: 处理工单类型：【协议信息】相关的业务逻辑
- `generalinformation/`: 处理工单类型：【通用信息】相关的业务逻辑
- 每种工单类型独立一个目录
- 每个核心业务模块都包含完整的MVC分层结构
 
### 4. support/ - 支撑层
 
支撑层提供工具类、缓存、校验等支撑能力，不包含具体业务逻辑。
 
```
support/
├── remotecache/       # 远程缓存
│   ├── redis/         # Redis实现
│   │   └── RemoteCacheRedis.java
│   ├── RemoteCache.java           # 缓存接口
│   └── RemoteCacheKeys.java       # 缓存Key定义
├── repeatsubmitchecker/  # 重复提交校验
│   └── RepeatSubmitChecker.java
└── utils/             # 工具类
    ├── LogUtil.java
    ├── MyCollectionUtil.java
    ├── MyObjectUtil.java
    ├── MyStringUtil.java
    ├── RemoteResultUtil.java
    └── ToStringUtil.java
```
 
**职责说明：**
- `remotecache/`: 提供远程缓存功能，支持Redis等实现
- `repeatsubmitchecker/`: 提供重复提交校验功能
- `utils/`: 存放通用的工具类
 
## 包创建规范
 
### 1. package-info.java 文件规范
 
每个包目录下都必须创建 `package-info.java` 文件，用于标识包的归属。
 
**示例：**
```java
package com.ocft.iic.uaw.server.modules.transaction.base.controller;
```
 
**注意事项：**
- 文件内容仅包含包声明语句
- 包名必须与目录结构完全对应
- 使用项目的标准包前缀：`com.ocft.iic.uaw.server.modules.transaction`
 
### 2. Windows目录创建命令
 
在Windows环境下创建目录结构时，使用 `md` 或 `mkdir` 命令：
 
```cmd
md base\controller
md base\pojo\bo
md base\pojo\dto
md base\pojo\vo
md base\service\imp
```
 
## 命名规范
 
### 1. 包命名
 
- 全部小写字母
- 使用点号分隔
- 体现包的职责和层次
- 示例：`com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation`
 
### 2. 类命名
 
- **Controller**: 以 `Controller` 结尾，如 `SubmitAgreementInformationController`
- **Service**: 接口以 `Service` 结尾，实现类以 `ServiceImpl` 结尾
- **Mapper**: 以 `Mapper` 结尾，如 `PolicyInformationMapper`
- **Entity**: 使用业务名词，如 `PaymentInformation`
- **BO**: 以 `BO` 结尾，如 `AgreementInformationBO`
- **DTO**: 以 `DTO` 结尾，如 `BaseTransactionDTO`
- **VO**: 以 `VO` 结尾，如 `AgreementVO`
- **Helper**: 以 `Helper` 结尾，如 `QueryAgreementHelper`
- **Converter**: 以 `Converter` 结尾，如 `AgreementInformationConverter`
- **Strategy**: 以 `Strategy` 或 `StrategyImpl` 结尾
- **Util**: 以 `Util` 结尾，如 `LogUtil`
- **Constants**: 以 `Constants` 结尾，如 `ModuleTags`
 
## 分层职责
 
### Controller层
- 接收HTTP请求
- 参数校验
- 调用Service层处理业务
- 返回响应结果
 
### Service层
- 实现业务逻辑
- 事务控制
- 调用DAO层访问数据
- 使用Helper处理复杂逻辑
- 使用Converter进行对象转换
- 使用Strategy实现策略模式
 
### DAO层
- 数据库访问
- Entity与数据库表映射
- Mapper接口定义SQL操作
 
### Helper层
- 封装复杂业务逻辑
- 提供可复用的业务方法
 
### Converter层
- 使用MapStruct进行对象转换
- BO/DTO/VO/Entity之间的转换
 
### Strategy层
- 实现策略模式
- 处理不同场景的业务逻辑差异
 
## 依赖原则
 
1. **上层依赖下层**：Controller → Service → DAO
2. **横向依赖**：Core层可以依赖Common层和Support层
3. **禁止反向依赖**：下层不能依赖上层
4. **避免循环依赖**：包之间不能形成循环依赖
 
## 新增业务模块步骤
 
当需要新增一个业务模块时，按照以下步骤操作：
 
1. 在 `core/` 下创建新的业务模块目录
2. 按照标准结构创建子包：`controller/`, `dao/`, `enums/`, `pojo/`, `service/`
3. 在每个子包下创建 `package-info.java` 文件
4. 根据需要创建 `service/converter/`, `service/helper/`, `service/strategy/` 等子包
5. 按照命名规范创建相应的类文件
 
## 示例：新增一个业务模块
 
假设需要新增 `paymentinformation` 模块：
 
```cmd
md core\paymentinformation\controller
md core\paymentinformation\dao\entity
md core\paymentinformation\dao\mapper
md core\paymentinformation\enums
md core\paymentinformation\pojo\bo
md core\paymentinformation\pojo\dto
md core\paymentinformation\pojo\vo
md core\paymentinformation\service\converter
md core\paymentinformation\service\helper
md core\paymentinformation\service\impl
md core\paymentinformation\service\strategy
```
 
然后创建相应的 `package-info.java` 文件和业务类文件。
 
## 注意事项
 
1. **保持一致性**：所有模块都应遵循相同的包结构规范
2. **职责单一**：每个包和类都应有明确的单一职责
3. **避免过度设计**：根据实际需求创建包，不要为了结构而结构
4. **及时更新**：当包结构发生变化时，及时更新相关文档
5. **代码审查**：新增包结构时，应进行代码审查确保符合规范  