# 目标
本规则用于根据背景和要求生成 transaction 模块的 DTO 模型对象。

# 背景
## 背景1：API接口设计文档
+ 用户输入：{包路径}
+ 用户输入：{类型(DTO)}
+ 用户输入：{字段或业务描述}

## 背景2：DTO对象生成规范
* 根据用户输入生成DTO（Data Transfer Object）模型对象
* **DTO类**：不强制继承基类，根据实际需求决定，类名必须以`DTO`为后缀
* 生成的对象放在对应位置，包路径为：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.dto`

## 包路径规范
* DTO类：`com.ocft.iic.uaw.server.modules.transaction.core.{模块名}.pojo.dto`，类名必须以`DTO`为后缀

### 示例1:DTO类
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.dto;

import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseChangeCusInfoBO;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 构建变更详情DTO
 * DTO类名必须以`DTO`为后缀
 * @author {当前用户账号}
 * @date {生成当天日期}
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@ApiModel(description = "构建变更详情DTO")
public class BuildChangeDetailDto<T extends BaseChangeCusInfoBO> {

    @ApiModelProperty(value = "旧列表")
    private List<T> oldList;

    @ApiModelProperty(value = "新列表")
    private List<T> newList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "变更ID", example = "change_123456")
    private String changeId;
}
```

# 重要约束

## 类属性类型约束

**DTO类的属性类型约束**：
- 如果属性不是Java基础类型（String、int、long、boolean、double、float等），则必须使用对应的DTO类型
- **禁止**在DTO类中使用Entity类型、BO类型、VO类型或其他非相关POJO类型
- **禁止**在DTO类中使用内部类

### 正确示例

```java
// 正确：DTO类中使用其他DTO类型
@Data
public class BuildChangeDetailDto<T extends BaseChangeCusInfoDTO> {
    @ApiModelProperty(value = "旧列表")
    private List<T> oldList;
}
```

### 错误示例

```java
// 错误：DTO类中使用Entity类型
@Data
public class WrongDto {
    @ApiModelProperty(value = "子详情")
    private ChildDetailEntity childDetail;  // 禁止使用Entity类型
}

// 错误：DTO类中混用BO类型
@Data
public class WrongDto {
    @ApiModelProperty(value = "子详情")
    private ChildDetailBO childDetail;  // 禁止混用不同类型
}

// 错误：DTO类中集合属性使用Entity类型
@Data
public class WrongDto {
    @ApiModelProperty(value = "子详情列表")
    private List<ChildDetailEntity> childList;  // 禁止在集合中使用Entity类型
}

// 错误：DTO属性字段使用VO类型
@Data
public class WrongDto {
    @ApiModelProperty(value = "子详情")
    private ChildDetailVO childDetail;  // 禁止在DTO中使用VO类型
}

// 错误：DTO类中使用内部类
@Data
public class WrongDto {
    @ApiModelProperty(value = "子详情")
    private ChildDetail childDetail;  // 禁止使用内部类，应独立为ChildDetailDto
    // 内部类示例（错误做法）
    public static class ChildDetail {
        private String field;
    }
}
```

## DTO类注解约束

**DTO类及属性定义建议添加 `@ApiModel` 和 `@ApiModelProperty` 注解**

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
@NoArgsConstructor
@AllArgsConstructor
@ApiModel(description = "构建变更详情DTO")
public class BuildChangeDetailDto<T extends BaseChangeCusInfoBO> {

    @ApiModelProperty(value = "旧列表")
    private List<T> oldList;

    @ApiModelProperty(value = "新列表")
    private List<T> newList;

    @ApiModelProperty(value = "工单id", example = "transaction_123456")
    private String transactionId;

    @ApiModelProperty(value = "变更ID", example = "change_123456")
    private String changeId;
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

# 要求
1. 根据背景1获取用户输入的信息路径、对象类型、字段描述
2. 根据背景2和示例创建DTO对象
3. 放到对应位置，如果没有则新建（windows系统）
4. **重要**：类名必须以`DTO`为后缀
5. **重要**：使用 `@ApiModel` 和 `@ApiModelProperty` 注解描述类和属性（建议）
6. **重要**：非基本类型属性必须使用对应的DTO类型
7. **重要**：禁止在DTO类中使用Entity类型、BO类型、VO类型或内部类