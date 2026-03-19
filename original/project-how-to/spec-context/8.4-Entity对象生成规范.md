# 目标
你是一个资深java开发专家，根据背景和要求生成transaction模块的Entity模型对象

# 背景
## 背景1：API接口设计文档
+ 用户输入：{包路径}
+ 用户输入：{类型(Entity)}
+ 用户输入：{字段或业务描述}

## 背景2：Entity对象生成规范
* 根据用户输入生成Entity（实体类）模型对象
* **Entity类**：继承 `BaseTransactionEntity`，类名必须以`Entity`为后缀（或根据表名命名）
* 生成的对象放在对应位置，包路径为：`com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity`

## 包路径规范
* Entity类：`com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity`，类名必须以`Entity`为后缀

### 示例1:BaseTransactionEntity类（继承BaseEntity）
```
package com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.ocft.iic.ecommon.api.entity.BaseEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;

/**
 * 交易实体基类
 * 所有 transaction 相关实体类继承此类
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@EqualsAndHashCode(callSuper = false)
@Data
@ApiModel(description = "交易实体基类")
public class BaseTransactionEntity extends BaseEntity implements Serializable {
    private static final long serialVersionUID = 1L;

    /**
     * 主键ID（自增）
     */
    @TableId(value = "id", type = IdType.AUTO)
    @ApiModelProperty(value = "主键ID", example = "1")
    private Long id;

    /**
     * 交易编号（唯一）
     */
    @TableField("transaction_id")
    @ApiModelProperty(value = "交易编号（唯一）", example = "transaction_123456")
    private String transactionId;

}
```

### 示例2:BaseChangeCusEntity类（继承BaseTransactionEntity）
```
package com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

/**
 * 客户基础信息变更公共实体
 * 继承 BaseTransactionEntity，提供变更相关的公共字段
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "客户基础信息变更公共实体")
public class BaseChangeCusEntity extends BaseTransactionEntity {

    @TableField("deal_type")
    @ApiModelProperty(value = "处理类型", example = "ADD/MODIFY/DELETE/NONE")
    protected String dealType;

    @TableField("change_id")
    @ApiModelProperty(value = "变更ID", example = "change_123456")
    protected String changeId;

    @TableField("unique_key")
    @ApiModelProperty(value = "唯一键", example = "unique_key_123")
    protected String uniqueKey;

    @TableField("preferred")
    @ApiModelProperty(value = "是否为默认", example = "Y/N")
    protected String preferred;

}
```

### 示例3:Entity类（继承BaseTransactionEntity）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.BaseTransactionEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 联系信息变更记录表
 * 对应表: iic_crm_transaction_change_contact_info
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("iic_crm_transaction_change_contact_info")
@ApiModel(description = "联系信息变更记录表")
public class ChangeContactInfo extends BaseTransactionEntity {

    @TableField("change_id")
    @ApiModelProperty(value = "变更ID", example = "change_123456")
    protected String changeId;

    @TableField("is_final")
    @ApiModelProperty(value = "是否为最终版本", example = "Y/N")
    private String isFinal;

    @TableField("operate_flag")
    @ApiModelProperty(value = "操作标志", example = "submit")
    private String operateFlag;

    @TableField("cancel_reason")
    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue")
    private String cancelReason;

    @TableField("cancel_observations")
    @ApiModelProperty(value = "取消备注", example = "取消备注示例")
    private String cancelObservations;

}
```

### 示例4:Entity类（继承BaseChangeCusEntity）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.BaseChangeCusEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 联系信息变更-地址信息明细表
 * 对应表: iic_crm_transaction_change_address_detail
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("iic_crm_transaction_change_address_detail")
@ApiModel(description = "联系信息变更-地址信息明细表")
public class ChangeAddressDetail extends BaseChangeCusEntity {

    @TableField("address_type")
    @ApiModelProperty(value = "地址类型", example = "HOME")
    private String addressType;

    @TableField("line_1")
    @ApiModelProperty(value = "地址行1", example = "123 Main Street")
    private String line1;

    @TableField("line_2")
    @ApiModelProperty(value = "地址行2", example = "Apt 4B")
    private String line2;

    @TableField("line_3")
    @ApiModelProperty(value = "地址行3", example = "Building A")
    private String line3;

    @TableField("line_4")
    @ApiModelProperty(value = "地址行4", example = "District 5")
    private String line4;

    @TableField("country")
    @ApiModelProperty(value = "国家", example = "CN")
    private String country;

    @TableField("postal_code")
    @ApiModelProperty(value = "邮政编码", example = "100000")
    private String postalCode;

}
```

### 示例5:Entity类（继承BaseTransactionEntity，自定义字段）
```
package com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.BaseTransactionEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 支付信息实体类
 * 对应表: iic_crm_transaction_payment_info
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@EqualsAndHashCode(callSuper = false)
@Data
@TableName("iic_crm_transaction_payment_info")
@ApiModel(description = "支付信息实体类")
public class PaymentInformation extends BaseTransactionEntity {

    @TableField("brand")
    @ApiModelProperty(value = "品牌", example = "Greenlight")
    private String brand;

    @TableField("additional_info")
    @ApiModelProperty(value = "附加信息", example = "this is additional info")
    private String additionalInfo;

}
```

### 示例6:Entity类（完整交易记录）
```
package com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;

/**
 * 交易记录实体类
 * 对应表: iic_crm_transaction
 * Entity类名必须以`Entity`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@EqualsAndHashCode(callSuper = true)
@Data
@TableName("iic_crm_transaction")
@ApiModel(description = "transaction主表实体")
public class Transaction extends BaseTransactionEntity implements Serializable {
    private static final long serialVersionUID = 1L;

    /**
     * 联系人ID
     */
    @TableField("contact_id")
    @ApiModelProperty(value = "联系人ID", example = "contact_123456")
    private String contactId;

    /**
     * 参考编号
     */
    @TableField("reference_number")
    @ApiModelProperty(value = "参考编号", example = "REF123456")
    private String referenceNumber;

    /**
     * 交互ID
     */
    @TableField("interaction_id")
    @ApiModelProperty(value = "交互ID", example = "interaction_123456")
    private String interactionId;

    /**
     * 员工ID（坐席）
     */
    @TableField("agent_id")
    @ApiModelProperty(value = "员工ID（坐席）", example = "agent_123456")
    private String agentId;

    /**
     * 客户ID
     */
    @TableField("customer_id")
    @ApiModelProperty(value = "客户ID", example = "customer_123456")
    private String customerId;

    /**
     * 交易类型
     */
    @TableField("transaction_type")
    @ApiModelProperty(value = "交易类型", example = "POLICY_ISSUE")
    private String transactionType;

    /**
     * 父级交易ID
     */
    @TableField("parent_transaction_id")
    @ApiModelProperty(value = "父级交易ID", example = "parent_transaction_123456")
    private String parentTransactionId;

    /**
     * 操作标志
     */
    @TableField("operate_flag")
    @ApiModelProperty(value = "操作标志", example = "submit")
    private String operateFlag;

    /**
     * 服务结果
     */
    @TableField("service_result")
    @ApiModelProperty(value = "服务结果", example = "completed")
    private String serviceResult;

    /**
     * 取消原因
     */
    @TableField("cancel_reason")
    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue")
    private String cancelReason;

    /**
     * 取消备注
     */
    @TableField("cancel_observations")
    @ApiModelProperty(value = "取消备注", example = "取消备注示例")
    private String cancelObservations;

}
```

# 重要约束

## 类属性类型约束

**Entity类的属性类型约束**：
- Entity类可以使用Java基础类型和String类型
- Entity类可以使用对应的BO/VO/DTO类型（当需要映射关联对象时）
- **必须**使用 `@TableName` 注解指定数据库表名
- **必须**使用 `@TableField` 注解指定字段映射

### 正确示例

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("iic_crm_transaction_change_contact_info")
@ApiModel(description = "联系信息变更记录表")
public class ChangeContactInfo extends BaseTransactionEntity {

    @TableField("change_id")
    @ApiModelProperty(value = "变更ID", example = "change_123456")
    protected String changeId;

    @TableField("is_final")
    @ApiModelProperty(value = "是否为最终版本", example = "Y/N")
    private String isFinal;

    @TableField("operate_flag")
    @ApiModelProperty(value = "操作标志", example = "submit")
    private String operateFlag;
}
```

## Entity类注解约束

**Entity类及属性定义建议添加 `@ApiModel` 和 `@ApiModelProperty` 注解**

### 注解使用要求

1. **@ApiModel 注解**：
   - 建议添加在类级别
   - 通过 `description` 属性描述类的用途

2. **@ApiModelProperty 注解**：
   - 建议添加在每个属性上
   - **value 属性**：建议说明属性的含义
   - **example 属性**：建议提供属性值的示例

### 正确示例

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("iic_crm_transaction_change_contact_info")
@ApiModel(description = "联系信息变更记录表")
public class ChangeContactInfo extends BaseTransactionEntity {

    @TableField("change_id")
    @ApiModelProperty(value = "变更ID", example = "change_123456")
    protected String changeId;

    @TableField("is_final")
    @ApiModelProperty(value = "是否为最终版本", example = "Y/N")
    private String isFinal;
}
```

## @ApiModelProperty注解说明
**@ApiModelProperty**注解用于描述模型对象字段的用途和示例值，通常用于Swagger API文档生成。
### 常用属性
- **value**：字段的描述信息，必填项
- **example**：字段的示例值，用于API文档展示
- **required**：字段是否必填，默认为false
- **allowableValues**：字段的允许值范围（已废弃，推荐使用枚举）
- **access**：指定字段的访问权限（如"hidden"隐藏字段）

### 使用示例
```
@ApiModelProperty(value = "客户ID", example = "CUST123456", required = true)
private String customerId;

@ApiModelProperty(value = "交易类型", example = "POLICY_ISSUE")
private String transactionType;

@ApiModelProperty(value = "唯一key", example = "unique_key_123")
private String uniqueKey;
```

## Entity公共字段说明

当Entity类需要记录变更信息时，可继承 `BaseChangeCusEntity`，该基类提供以下公共字段：
- `dealType`：处理类型（ADD、MODIFY、DELETE、NONE）
- `changeId`：变更ID
- `uniqueKey`：唯一键
- `preferred`：是否为默认值

## MyBatis-Plus注解说明

### @TableName
用于指定数据库表名。
```java
@TableName("iic_crm_transaction_change_contact_info")
```

### @TableField
用于指定字段映射。
```java
@TableField("change_id")
private String changeId;
```

### @TableId
用于指定主键字段。
```java
@TableId(value = "id", type = IdType.AUTO)
private Long id;
```

# 要求
1. 根据背景1获取用户输入的信息路径、对象类型、字段描述
2. 根据背景2和示例创建Entity对象
3. 放到对应位置，如果没有则新建（windows系统）
4. **重要**：类名必须以`Entity`为后缀
5. **重要**：Entity类继承 `BaseTransactionEntity`，如需变更公共字段可继承 `BaseChangeCusEntity`
6. **重要**：使用 `@TableName` 注解指定数据库表名，使用 `@TableField` 注解指定字段映射
7. **重要**：使用 `@ApiModel` 和 `@ApiModelProperty` 注解描述类和属性（建议）