# 目标
你是一个资深java开发专家，根据背景和要求生成transaction模块的VO模型对象

# 背景
## 背景1：API接口设计文档
+ 用户输入：{包路径}
+ 用户输入：{类型(VO)}
+ 用户输入：{字段或业务描述}

## 背景2：VO对象生成规范
* 根据用户输入生成VO（View Object）模型对象
* **VO类**：实现 `Serializable` 接口，类名必须以`VO`为后缀
* **VO基类说明**：VO基类提供公共属性，子类继承基类可复用这些属性。基类中的属性必须使用protected修饰符，以便子类访问
* 生成的对象放在对应位置，包路径为：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.vo`

## 属性修饰符与toString规范
* **VO基类属性必须使用protected修饰符**：所有VO基类中的属性应使用protected修饰符，以便子类继承访问
* **VO子类属性默认使用private修饰符**：VO子类的自有属性应使用private修饰符
* **VO类需实现Serializable接口**：VO类必须实现 `Serializable` 接口，确保序列化兼容性
* **子类toString方法需包含父类属性**：当子类重写toString方法时，必须显式包含父类的所有属性，确保日志输出的完整性
* **VO类需重写toString方法**：当VO类包含复杂属性或需要日志输出时，应重写 `toString()` 方法，确保日志输出的完整性

### 示例：VO基类属性修饰符为protected
```java
package com.ocft.iic.uaw.server.modules.transaction.base.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.io.Serializable;

/**
 * 基础交易响应数据传输对象
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "基础交易响应数据传输对象")
public class BaseTransactionVO implements Serializable {

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

### 示例：VO子类属性修饰符为private
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.vo.BaseTransactionVO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.io.Serializable;
import java.util.List;

/**
 * 联系信息变更出参VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "联系信息变更出参VO")
public class ChangeContactInfoVO extends BaseTransactionVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "最初的地址信息")
    private List<ChangeAddressDetailVO> originalAddressList;

    @ApiModelProperty(value = "修改后的地址信息")
    private List<ChangeAddressDetailVO> modifiedAddressList;

    @ApiModelProperty(value = "最初的邮箱信息")
    private List<ChangeEmailsDetailVO> originalEmailsList;

    @ApiModelProperty(value = "修改后的邮箱信息")
    private List<ChangeEmailsDetailVO> modifiedEmailsList;

    @ApiModelProperty(value = "最初的电话信息")
    private List<ChangePhonesDetailVO> originalPhoneList;

    @ApiModelProperty(value = "修改后的电话信息")
    private List<ChangePhonesDetailVO> modifiedPhoneList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "操作类型", example = "submit")
    private String operateFlag;

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
                .toString();
    }
}
```

### 示例：VO子类toString方法包含父类属性
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.vo.BaseChangeCusInfoVO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.io.Serializable;

/**
 * 联系信息变更-电话详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@ApiModel(description = "联系信息变更-电话详情VO")
public class ChangePhonesDetailVO extends BaseChangeCusInfoVO implements Serializable {

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

### 示例：VO类属性修饰符为private（无继承）
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 联系信息变更-地址详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-地址详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeAddressDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key", example = "unique_key_123")
    private String uniqueKey;

    @ApiModelProperty(value = "地址类型", example = "HOME")
    private String addressType;

    @ApiModelProperty(value = "地址行1", example = "123 Main Street")
    private String line1;

    @ApiModelProperty(value = "地址行2", example = "Apt 4B")
    private String line2;

    @ApiModelProperty(value = "地址行3", example = "Building A")
    private String line3;

    @ApiModelProperty(value = "地址行4", example = "District 5")
    private String line4;

    @ApiModelProperty(value = "国家", example = "CN")
    private String country;

    @ApiModelProperty(value = "邮政编码", example = "100000")
    private String postalCode;

    @ApiModelProperty(value = "是否为默认", example = "Y/N")
    private String preferred;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("addressType", addressType)
                .add("line1", line1)
                .add("line2", line2)
                .add("line3", line3)
                .add("line4", line4)
                .add("country", country)
                .add("postalCode", postalCode)
                .add("preferred", preferred)
                .add("dealType", dealType)
                .toString();
    }
}
```

### 示例：VO类属性修饰符为private
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 联系信息变更-地址详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-地址详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeAddressDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key", example = "unique_key_123")
    private String uniqueKey;

    @ApiModelProperty(value = "地址类型", example = "HOME")
    private String addressType;

    @ApiModelProperty(value = "地址行1", example = "123 Main Street")
    private String line1;

    @ApiModelProperty(value = "地址行2", example = "Apt 4B")
    private String line2;

    @ApiModelProperty(value = "地址行3", example = "Building A")
    private String line3;

    @ApiModelProperty(value = "地址行4", example = "District 5")
    private String line4;

    @ApiModelProperty(value = "国家", example = "CN")
    private String country;

    @ApiModelProperty(value = "邮政编码", example = "100000")
    private String postalCode;

    @ApiModelProperty(value = "是否为默认", example = "Y/N")
    private String preferred;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("addressType", addressType)
                .add("line1", line1)
                .add("line2", line2)
                .add("line3", line3)
                .add("line4", line4)
                .add("country", country)
                .add("postalCode", postalCode)
                .add("preferred", preferred)
                .add("dealType", dealType)
                .toString();
    }
}
```

### 示例：VO类（包含BaseCustomerColInfoVO包装类型）
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 联系信息变更-地址详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-地址详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeAddressDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key", example = "unique_key_123")
    private String uniqueKey;

    @ApiModelProperty(value = "地址类型", example = "HOME")
    private BaseCustomerColInfoVO addressType;

    @ApiModelProperty(value = "地址行1", example = "123 Main Street")
    private BaseCustomerColInfoVO line1;

    @ApiModelProperty(value = "地址行2", example = "Apt 4B")
    private BaseCustomerColInfoVO line2;

    @ApiModelProperty(value = "地址行3", example = "Building A")
    private BaseCustomerColInfoVO line3;

    @ApiModelProperty(value = "地址行4", example = "District 5")
    private BaseCustomerColInfoVO line4;

    @ApiModelProperty(value = "国家", example = "CN")
    private BaseCustomerColInfoVO country;

    @ApiModelProperty(value = "邮政编码", example = "100000")
    private BaseCustomerColInfoVO postalCode;

    @ApiModelProperty(value = "是否为默认", example = "Y/N")
    private BaseCustomerColInfoVO preferred;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("addressType", addressType)
                .add("line1", line1)
                .add("line2", line2)
                .add("line3", line3)
                .add("line4", line4)
                .add("country", country)
                .add("postalCode", postalCode)
                .add("preferred", preferred)
                .add("dealType", dealType)
                .toString();
    }
}
```

### 示例：BaseCustomerColInfoVO类（VO包装类型）
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 客户列信息VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "客户列信息VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BaseCustomerColInfoVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "原始值", example = "old_value_123")
    private String oldValue;

    @ApiModelProperty(value = "新值", example = "new_value_456")
    private String newValue;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("oldValue", oldValue)
                .add("newValue", newValue)
                .add("dealType", dealType)
                .toString();
    }
}
```

## VO基类说明

### VO基类属性修饰符规范
- **VO基类属性必须使用protected修饰符**：所有VO基类（如BaseTransactionVO、BaseChangeCusInfoVO等）中的属性应使用protected修饰符，以便子类继承访问
- **VO子类属性默认使用private修饰符**：VO子类的自有属性应使用private修饰符

### BaseTransactionVO（VO基类示例）
VO类默认继承此类，提供基础的事务对象功能，包含以下公共属性（均为protected修饰符）：
- `requestToken`：前端防重提交token
- `contactId`：联系人ID
- `customerId`：客户ID
- `transactionType`：交易类型

### BaseChangeCusInfoVO（VO基类示例）
当VO类需要变更客户信息时的公共属性时，继承此类，提供以下公共字段（均为protected修饰符）：
- `uniqueKey`：唯一键
- `dealType`：处理类型（ADD、MODIFY、DELETE、NONE）
- `changeId`：变更ID
- `preferred`：是否为默认值

# 包路径规范
* VO类：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.vo`，类名必须以`VO`为后缀

### 示例1:VO类
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

/**
 * 本次联系信息变更详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "本次联系信息变更详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeContactInfoVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "电话信息列表")
    private List<ChangePhonesDetailVO> phoneList;

    @ApiModelProperty(value = "邮箱信息列表")
    private List<ChangeEmailsDetailVO> emailList;

    @ApiModelProperty(value = "地址信息列表")
    private List<ChangeAddressDetailVO> addressList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "操作标志：submit（提交）或 cancel（取消）", required = true, example = "submit")
    private String operateFlag;
}
```

### 示例2:VO类（包含BaseCustomerColInfoVO包装类型）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 联系信息变更-地址详情VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更-地址详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeAddressDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key", example = "unique_key_123")
    private String uniqueKey;

    @ApiModelProperty(value = "地址类型", example = "HOME")
    private BaseCustomerColInfoVO addressType;

    @ApiModelProperty(value = "地址行1", example = "123 Main Street")
    private BaseCustomerColInfoVO line1;

    @ApiModelProperty(value = "地址行2", example = "Apt 4B")
    private BaseCustomerColInfoVO line2;

    @ApiModelProperty(value = "地址行3", example = "Building A")
    private BaseCustomerColInfoVO line3;

    @ApiModelProperty(value = "地址行4", example = "District 5")
    private BaseCustomerColInfoVO line4;

    @ApiModelProperty(value = "国家", example = "CN")
    private BaseCustomerColInfoVO country;

    @ApiModelProperty(value = "邮政编码", example = "100000")
    private BaseCustomerColInfoVO postalCode;

    @ApiModelProperty(value = "是否为默认", example = "Y/N")
    private BaseCustomerColInfoVO preferred;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("addressType", addressType)
                .add("line1", line1)
                .add("line2", line2)
                .add("line3", line3)
                .add("line4", line4)
                .add("country", country)
                .add("postalCode", postalCode)
                .toString();
    }
}
```

### 示例3:BaseCustomerColInfoVO类（VO包装类型）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 客户列信息VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "客户列信息VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BaseCustomerColInfoVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "原始值", example = "old_value_123")
    private String oldValue;

    @ApiModelProperty(value = "新值", example = "new_value_456")
    private String newValue;

    @ApiModelProperty(value = "处理类型", example = "UPDATE")
    private String dealType;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("oldValue", oldValue)
                .add("newValue", newValue)
                .add("dealType", dealType)
                .toString();
    }
}
```

### 示例4:VO类（返回结果VO）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.uaw.server.modules.transaction.base.constants.BaseConstants;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 联系信息变更提交结果VO
 * VO类名必须以`VO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@ApiModel(description = "联系信息变更提交结果VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ContactInfoSubmitVO {

    @ApiModelProperty(value = "响应码，success表示成功", example = "success")
    private String code;

    @ApiModelProperty(value = "响应消息", example = "操作成功")
    private String msg;

    public static ContactInfoSubmitVO success() {
        return ContactInfoSubmitVO.builder()
                .code(BaseConstants.SUCCESS_STR)
                .build();
    }
}
```

# 重要约束

## 类属性类型约束

**VO类的属性类型约束**：
- 如果属性不是Java基础类型（String、int、long、boolean、double、float等），则必须使用对应的VO类型
- **禁止**在VO类中使用Entity类型、BO类型、DTO类型或其他非相关POJO类型
- **禁止**在VO类中使用内部类

### 正确示例

```java
// 正确：VO类中使用其他VO类型
@Data
public class ParentVO implements Serializable {
    @ApiModelProperty(value = "子详情列表") // 非基本类型属性需有 value 说明，不需example 示例值
    private List<ChildDetailVO> childList;  // 使用VO类型

   @ApiModelProperty(value = "电话ID", example = "phone_123456")  // 基本类型的属性，需有 value 说明 和 example 示例值
   private String contactId;
}
```

### 错误示例

```java
// 错误：VO类中使用Entity类型
@Data
public class WrongVO implements Serializable {
    @ApiModelProperty(value = "子详情")
    private ChildDetailEntity childDetail;  // 禁止使用Entity类型
}

// 错误：VO类中混用BO类型
@Data
public class WrongVO implements Serializable {
    @ApiModelProperty(value = "子详情")
    private ChildDetailBO childDetail;  // 禁止混用不同类型
}

// 错误：VO类中集合属性使用Entity类型
@Data
public class WrongVO implements Serializable {
    @ApiModelProperty(value = "子详情列表")
    private List<ChildDetailEntity> childList;  // 禁止在集合中使用Entity类型
}

// 错误：VO属性字段使用DTO类型
@Data
public class WrongVO implements Serializable {
    @ApiModelProperty(value = "子详情")
    private ChildDetailDto childDetail;  // 禁止在VO中使用DTO类型
}

// 错误：VO类中使用内部类
@Data
public class WrongVO implements Serializable {
    @ApiModelProperty(value = "子详情")
    private ChildDetail childDetail;  // 禁止使用内部类，应独立为ChildDetailVO
    // 内部类示例（错误做法）
    public static class ChildDetail {
        private String field;
    }
}
```

## VO类注解约束

**VO类及属性定义必须添加 `@ApiModel` 和 `@ApiModelProperty` 注解**

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
 * 一般信息请求参数VO
 * @author EX-XUEBO158
 */
@Data
@ApiModel(description = "一般信息请求参数VO")
public class EnquiryInformationVO implements Serializable {
    
    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "协议列表")  // 非基本类型属性需有 value 说明，不需example 示例值
    private List<AgreementVO> agreements;
    
    @ApiModelProperty(value = "品牌", example = "Greenlight") // 基本类型属性需有 value 说明 和 example 示例值
    private String brand;

    @ApiModelProperty(value = "附加信息", example = "this is additional info")
    private String additionalInfo;

    @ApiModelProperty(value = "操作标志：submit（提交）或 cancel（取消）", required = true, example = "submit")
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
public class WrongVO implements Serializable {
    
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

## VO包装类型说明
当需要展示字段变更前后的值时，使用 `BaseCustomerColInfoVO` 包装类型：
- `oldValue`：原始值
- `newValue`：新值
- `dealType`：处理类型（如：ADD、UPDATE、DELETE）

# 要求
1. 根据背景1获取用户输入的信息路径、对象类型、字段描述
2. 根据背景2和示例创建VO对象
3. 放到对应位置，如果没有则新建（windows系统）
4. **重要**：类名必须以`VO`为后缀
5. **重要**：VO类实现 `Serializable` 接口并重写 `toString()` 方法
6. **重要**：使用 `@ApiModel` 和 `@ApiModelProperty` 注解描述类和属性
7. **重要**：非基本类型属性必须使用对应的VO类型
8. **重要**：禁止在VO类中使用Entity类型、BO类型、DTO类型或内部类
9. **重要**：VO基类（例如：BaseTransactionVO、BaseChangeCusInfoVO）的属性必须使用protected修饰符；VO子类的自有属性默认使用private修饰符；子类重写toString方法时，必须显式包含父类的所有属性
10. **重要**：新建或修改VO类后，需检查代码，确保满足上述属性修饰符与toString规范
 