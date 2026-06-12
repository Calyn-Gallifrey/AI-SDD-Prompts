# 目标
本规则用于根据背景和要求生成 transaction 模块的 BO 模型对象。

## 示例边界

本文件中的代码片段、类名、字段名、注解值、示例值和业务名仅用于说明 BO 模型结构和写法，不是当前任务的默认业务内容。生成 BO 时，必须基于当前 Brief Design、当前代码和已确认接口契约替换所有示例业务信息。

# 背景
## 背景1：API接口设计文档
+ 用户输入：{包路径}
+ 用户输入：{类型(BO)}
+ 用户输入：{字段或业务描述}

## 背景2：BO对象生成规范
* 根据用户输入生成BO（Business Object）模型对象
* **BO类**：可继承BO基类（如BaseTransactionBO、BaseChangeCusInfoBO等），类名必须以`BO`为后缀
* 生成的对象放在对应位置，包路径为：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.bo`
* **BO基类说明**：BO基类提供公共属性，子类继承基类可复用这些属性。基类中的属性必须使用protected修饰符，以便子类访问

## 属性修饰符与toString规范
* **BO基类属性必须使用protected修饰符**：所有BO基类（如BaseTransactionBO、BaseChangeCusInfoBO等）中的属性应使用protected修饰符，以便子类继承访问
* **BO子类属性默认使用private修饰符**：BO子类的自有属性应使用private修饰符
* **子类toString方法需包含父类属性**：当子类重写toString方法时，必须显式包含父类的所有属性，确保日志输出的完整性

### 示例：BO基类属性修饰符为protected
```java
package com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.io.Serializable;

/**
 * 基础交易请求数据传输对象
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "基础交易请求数据传输对象")
public class BaseTransactionBO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "前端防重提交 token", required = true)
    protected String requestToken;

    @ApiModelProperty(value = "联系人ID", required = true)
    protected String contactId;

    @ApiModelProperty(value = "客户ID", required = true)
    protected String customerId;

    @ApiModelProperty(value = "交易类型", required = true)
    protected String transactionType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("requestToken", requestToken)
                .add("contactId", contactId)
                .add("customerId", customerId)
                .add("transactionType", transactionType)
                .toString();
    }
}
```

### 示例：BO子类属性修饰符为private
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseTransactionBO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.util.List;

/**
 * 联系信息变更入参BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "联系信息变更入参BO")
public class ChangeContactInfoBO extends BaseTransactionBO {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "最初的地址信息")
    private List<ChangeAddressDetailBO> originalAddressList;

    @ApiModelProperty(value = "修改后的地址信息")
    private List<ChangeAddressDetailBO> modifiedAddressList;

    @ApiModelProperty(value = "最初的邮箱信息")
    private List<ChangeEmailsDetailBO> originalEmailsList;

    @ApiModelProperty(value = "修改后的邮箱信息")
    private List<ChangeEmailsDetailBO> modifiedEmailsList;

    @ApiModelProperty(value = "最初的电话信息")
    private List<ChangePhonesDetailBO> originalPhoneList;

    @ApiModelProperty(value = "修改后的电话信息")
    private List<ChangePhonesDetailBO> modifiedPhoneList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "操作类型", example = "submit")
    private String operateFlag;

    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue")
    private String cancelReason;

    @ApiModelProperty(value = "取消备注", example = "取消备注示例")
    private String cancelObservations;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("requestToken", requestToken)
                .add("contactId", contactId)
                .add("customerId", customerId)
                .add("transactionType", transactionType)
                .add("originalAddressList", originalAddressList)
                .add("modifiedAddressList", modifiedAddressList)
                .add("originalEmailsList", originalEmailsList)
                .add("modifiedEmailsList", modifiedEmailsList)
                .add("originalPhoneList", originalPhoneList)
                .add("modifiedPhoneList", modifiedPhoneList)
                .add("transactionId", transactionId)
                .add("operateFlag", operateFlag)
                .add("cancelReason", cancelReason)
                .add("cancelObservations", cancelObservations)
                .toString();
    }
}
```

### 示例：子类toString方法包含父类属性
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseChangeCusInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 联系信息变更-电话详情BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "联系信息变更-电话详情BO")
public class ChangePhonesDetailBO extends BaseChangeCusInfoBO {

    @ApiModelProperty(value = "电话类型", example = "MOBILE")
    private String phoneType;

    @ApiModelProperty(value = "国家", example = "CN")
    private String country;

    @ApiModelProperty(value = "国际区号", example = "+86")
    private String diallingCode;

    @ApiModelProperty(value = "电话号码", example = "13800138000")
    private String number;

    @ApiModelProperty(value = "是否为默认电话", example = "Y/N")
    private String preferred;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("dealType", dealType)
                .add("changeId", changeId)
                .add("preferred", preferred)
                .add("phoneType", phoneType)
                .add("country", country)
                .add("diallingCode", diallingCode)
                .add("number", number)
                .toString();
    }
}
```

### 示例：子类toString方法包含父类属性
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.common.transaction.annotions.NeedParseCol;
import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseChangeCusInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;


/**
 * 联系信息变更-电话详情BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-电话详情BO")
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class ChangePhonesDetailBO extends BaseChangeCusInfoBO {

    @ApiModelProperty(value = "电话类型", example = "MOBILE")
    @NeedParseCol
    private String phoneType;

    @ApiModelProperty(value = "国家", example = "CN")
    @NeedParseCol
    private String country;

    @ApiModelProperty(value = "国际区号", example = "+86")
    @NeedParseCol
    private String diallingCode;

    @ApiModelProperty(value = "电话号码", example = "13800138000")
    @NeedParseCol
    private String number;

    @ApiModelProperty(value = "是否为默认电话", example = "Y/N")
    @NeedParseCol
    private String preferred;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("dealType", dealType)
                .add("changeId", changeId)
                .add("preferred", preferred)
                .add("phoneType", phoneType)
                .add("country", country)
                .add("diallingCode", diallingCode)
                .add("number", number)
                .toString();
    }
}
```

## 包路径规范
* BO类：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.bo`，类名必须以`BO`为后缀

### 示例1:BO类（继承BaseTransactionBO）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseTransactionBO;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import java.util.List;

/**
 * 联系信息变更入参BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "联系信息变更入参BO")
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeContactInfoBO extends BaseTransactionBO {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "最初的地址信息")
    private List<ChangeAddressDetailBO> originalAddressList;

    @ApiModelProperty(value = "修改后的地址信息")
    private List<ChangeAddressDetailBO> modifiedAddressList;

    @ApiModelProperty(value = "最初的邮箱信息")
    private List<ChangeEmailsDetailBO> originalEmailsList;

    @ApiModelProperty(value = "修改后的邮箱信息")
    private List<ChangeEmailsDetailBO> modifiedEmailsList;

    @ApiModelProperty(value = "最初的电话信息")
    private List<ChangePhonesDetailBO> originalPhoneList;

    @ApiModelProperty(value = "修改后的电话信息")
    private List<ChangePhonesDetailBO> modifiedPhoneList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "操作类型", example = "submit")
    private String operateFlag;

    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue")
    private String cancelReason;

    @ApiModelProperty(value = "取消备注", example = "取消备注示例")
    private String cancelObservations;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("transactionId", transactionId)
                .add("operateFlag", operateFlag)
                .add("cancelReason", cancelReason)
                .add("cancelObservations", cancelObservations)
                .toString();
    }
}
```

### 示例2:BO类（继承BaseChangeCusInfoBO）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.common.transaction.annotions.NeedParseCol;
import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseChangeCusInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;


/**
 * 联系信息变更-电话详情BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-电话详情BO")
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class ChangePhonesDetailBO extends BaseChangeCusInfoBO {

    @ApiModelProperty(value = "电话类型", example = "MOBILE")
    @NeedParseCol
    private String phoneType;

    @ApiModelProperty(value = "国家", example = "CN")
    @NeedParseCol
    private String country;

    @ApiModelProperty(value = "国际区号", example = "+86")
    @NeedParseCol
    private String diallingCode;

    @ApiModelProperty(value = "电话号码", example = "13800138000")
    @NeedParseCol
    private String number;

    @ApiModelProperty(value = "是否为默认电话", example = "Y/N")
    @NeedParseCol
    private String preferred;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("dealType", dealType)
                .add("changeId", changeId)
                .add("preferred", preferred)
                .add("phoneType", phoneType)
                .add("country", country)
                .add("diallingCode", diallingCode)
                .add("number", number)
                .toString();
    }
}
```

### 示例3:BO类（不继承基类）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;

/**
 * 查询联系信息BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "查询联系信息BO")
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContactInfoQueryAllBO {

    @ApiModelProperty(value = "客户ID", example = "customer_123456", required = true)
    @NotBlank(message = "CUSTOMER ID NOT NULL")
    private String customerId;

    @ApiModelProperty(value = "电话ID", example = "phone_123456")
    private String contactId;

}
```

### 示例4:BO类（带toString方法）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseTransactionBO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import java.util.List;

/**
 * 一般信息请求参数BO
 * BO类名必须以`BO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "一般信息请求参数BO")
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class GeneralInformationBO extends BaseTransactionBO {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "协议列表")
    private List<AgreementBO> agreements;

    @ApiModelProperty(value = "品牌", example = "Greenlight")
    private String brand;

    @ApiModelProperty(value = "附加信息", example = "this is additional info")
    private String additionalInfo;

    @ApiModelProperty(value = "操作标志：submit（提交）或 cancel（取消）", required = true, example = "submit")
    @NotBlank(message = "operateFlag is empty")
    private String operateFlag;

    @ApiModelProperty(value = "服务结果", example = "completed")
    private String serviceResult;

    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue with transaction")
    private String cancelReason;

    @ApiModelProperty(value = "取消备注", example = "this is cancel observations")
    private String cancelObservations;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("agreements", agreements)
                .add("brand", brand)
                .add("additionalInfo", additionalInfo)
                .add("operateFlag", operateFlag)
                .add("serviceResult", serviceResult)
                .add("cancelReason", cancelReason)
                .add("cancelObservations", cancelObservations)
                .toString();
    }
}
```


# 重要约束

## 类属性类型约束

**BO类的属性类型约束**：
- 如果属性不是Java基础类型（String、int、long、boolean、double、float等），则必须使用对应的BO类型
- **禁止**在BO类中使用Entity类型、VO类型、DTO类型或其他非相关POJO类型
- **禁止**在BO类中使用内部类

### 正确示例

```java
// 正确：BO类中使用其他BO类型
@Data
@ApiModel(description = "联系信息变更提交结果BO")
public class ParentBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情列表")  // 非基本类型属性需有 value 说明，不需example 示例值
    private List<ChildDetailBO> childList;  // 使用BO类型

   @ApiModelProperty(value = "电话ID", example = "phone_123456")  // 基本类型属性需有 value 说明 和 example 示例值
   private String contactId;
}
```

### 错误示例

```java
// 错误：BO类中使用Entity类型
@Data
public class WrongBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情")
    private ChildDetailEntity childDetail;  // 禁止使用Entity类型
}

// 错误：BO类中混用VO类型
@Data
public class WrongBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情")
    private ChildDetailVO childDetail;  // 禁止混用不同类型
}

// 错误：BO类中集合属性使用Entity类型
@Data
public class WrongBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情列表")
    private List<ChildDetailEntity> childList;  // 禁止在集合中使用Entity类型
}

// 错误：BO属性字段使用DTO类型
@Data
public class WrongBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情")
    private ChildDetailDto childDetail;  // 禁止在BO中使用DTO类型
}

// 错误：BO类中使用内部类
@Data
public class WrongBO extends BaseTransactionBO {
    @ApiModelProperty(value = "子详情")
    private ChildDetail childDetail;  // 禁止使用内部类，应独立为ChildDetailBO
    // 内部类示例（错误做法）
    public static class ChildDetail {
        private String field;
    }
}
```

## BO类注解约束

**BO类及属性定义必须添加 `@ApiModel` 和 `@ApiModelProperty` 注解**

### 注解使用要求

1. **@ApiModel 注解**：
   - 必须添加在类级别
   - 通过 `description` 属性描述类的用途

2. **@ApiModelProperty 注解**：
   - 必须添加在每个属性上
   - **value 属性**：必须说明属性的含义（必填）
   - **example 属性**：必须提供属性值的示例（必填）

### 正确示例

```java
/**
 * 一般信息请求参数BO
 * @author EX-XUEBO158
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "一般信息请求参数BO")
public class EnquiryInformationBO extends BaseTransactionBO implements Serializable {
    
    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "协议列表")  // 非基本类型属性需有 value 说明，不需example 示例值
    private List<AgreementBO> agreements;
    
    @ApiModelProperty(value = "品牌", example = "Greenlight") // 基本类型属性需有 value 说明 和 example 示例值
    private String brand;

    @ApiModelProperty(value = "附加信息", example = "this is additional info")
    private String additionalInfo;

    @ApiModelProperty(value = "操作标志：submit（提交）或 cancel（取消）", required = true, example = "submit")
    @NotBlank(message = "operateFlag is empty") 
    private String operateFlag;

    @ApiModelProperty(value = "服务结果", example = "completed")
    private String serviceResult;

    @ApiModelProperty(value = "取消原因", example = "Customer decided not to continue with transaction")
    private String cancelReason;

    @ApiModelProperty(value = "取消备注", example = "this is cancel observations")
    private String cancelObservations;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("agreements", agreements)
                .add("brand", brand)
                .add("additionalInfo", additionalInfo)
                .add("operateFlag", operateFlag)
                .add("serviceResult", serviceResult)
                .add("cancelReason", cancelReason)
                .add("cancelObservations", cancelObservations)
                .toString();
    }
}
```

### 错误示例（不符合约束）

```java
// 错误：缺少 @ApiModel 注解
@Data
public class WrongBO extends BaseTransactionBO {
    
    // 错误：缺少 @ApiModelProperty 注解
    private String brand;
    
    // 错误：缺少 example 属性
    @ApiModelProperty(value = "操作标志")
    private String operateFlag;
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

## BO基类说明

### BO基类属性修饰符规范
- **BO基类属性必须使用protected修饰符**：所有BO基类（如BaseTransactionBO、BaseChangeCusInfoBO等）中的属性应使用protected修饰符，以便子类继承访问
- **BO子类属性默认使用private修饰符**：BO子类的自有属性应使用private修饰符

### BaseTransactionBO（BO基类示例）
BO类默认继承此类，提供基础的事务对象功能，包含以下公共属性（均为protected修饰符）：
- `requestToken`：前端防重提交token
- `contactId`：联系人ID
- `referenceNumber`：参考编号
- `interactionId`：互动ID
- `agentId`：坐席ID
- `customerId`：客户ID
- `transactionType`：交易类型
- `parentTransactionId`：父交易ID
- `groupId`：工单分组ID
- `transactionId`：交易ID

### BaseChangeCusInfoBO（BO基类示例）
当BO类需要变更客户信息时的公共属性时，继承此类，提供以下公共字段（均为protected修饰符）：
- `uniqueKey`：唯一键
- `dealType`：处理类型（ADD、MODIFY、DELETE、NONE）
- `changeId`：变更ID
- `preferred`：是否为默认值

# 要求
1. 根据背景1获取用户输入的信息路径、对象类型、字段描述
2. 根据背景2和示例创建BO对象
3. 放到对应位置，如果没有则新建（windows系统）
4. **重要**：类名必须以`BO`为后缀
5. **重要**：BO类优先继承 `BaseTransactionBO`，当需要变更客户信息时继承 `BaseChangeCusInfoBO`
6. **重要**：使用 `@ApiModel` 和 `@ApiModelProperty` 注解描述类和属性
7. **重要**：非基本类型属性必须使用对应的BO类型
8. **重要**：禁止在BO类中使用Entity类型、VO类型、DTO类型或内部类
9. **重要**：BO基类（例如：BaseTransactionBO、BaseChangeCusInfoBO）的属性必须使用protected修饰符；BO子类的自有属性默认使用private修饰符；子类重写toString方法时，必须显式包含父类的所有属性
10. **重要**：新建或修改BO类后，需检查代码，确保满足上述属性修饰符与toString规范
