# 目标
本规则用于根据背景内容和参考示例生成对象转换代码，并放到指定位置。

## 示例边界

本文件中的代码片段、类名、包名、字段名和业务名仅用于说明 MapStruct 转换结构和写法，不是当前任务的默认业务内容。生成转换代码时，必须基于当前 Brief Design、当前代码和已确认对象模型替换所有示例业务信息。

# 背景
## 背景1
- 项目技术栈：Java 1.8、SpringBoot 2.7.18、MySQL
- 用户输入: {业务描述}
- 用户输入: {包路径}

## 背景2
  - 转换类接口: 创建业务对象转换类接口，继承BaseTransactionConverter
  - 使用类: 在Service层通过@Autowired注入使用
  - 一个转换对象生成一个转换类接口
  - 两个对象转换时，如果属性不同，可以使用 @Mapping(target = "xxx", source = "xxx") 建立映射关系
  - 目标值也可以使用表达式，@Mapping(target = "xxx", expression = "java(this.xxx())")
  - BaseTransactionConverter提供公共方法：
    - currentUser()：返回当前登录用户的um
    - nowTime()：返回当前时间LocalDateTime

# 示例
## 示例1 业务对象转换类接口
```
package {包路径}.assembler;

import com.ocft.iic.uaw.server.modules.transaction.base.converter.BaseTransactionConverter;
import {源对象包路径};
import {目标对象包路径};
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

/**
 * @author {当前登录域账号}
 * @description {业务描述}
 * @date {当前日期，格式：yyyy-MM-dd}
 */
@Mapper(componentModel = "spring")
public interface {业务名称}Converter extends BaseTransactionConverter {

    /**
     * 静态实例方式（非Spring管理）
     */
    {业务名称}Converter INSTANCE = Mappers.getMapper({业务名称}Converter.class);

    /**
     * {源对象} 转换为 {目标对象}
     *
     * @param {源对象} {源对象}
     * @param {其他参数} {其他参数}
     * @return {目标对象} {目标对象}
     * @author {当前登录域账号}
     * @date {当前日期，格式：yyyy-MM-dd}
     **/
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    {其他映射规则}
    {目标对象} {方法名}({源对象} {源对象}, {其他参数类型} {其他参数});
}
```

## 使用方式
在Service层可通过以下两种方式使用：

**方式1：Spring注入（推荐）**
```java
@Autowired
private {业务名称}Converter {业务名称}Converter;
```

**方式2：静态实例方式（非Spring管理）**
```java
{业务名称}Converter converter = {业务名称}Converter.INSTANCE;
```

## 示例2 联系信息变更对象转换（实际项目示例）
```
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.assembler;

import com.ocft.iic.uaw.server.modules.transaction.base.converter.BaseTransactionConverter;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.Transaction;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.dao.entity.ChangeContactInfo;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.dao.dto.ChangeContactInfoDto;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo.ChangeContactInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo.BaseCustomerColInfoVO;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo.ChangeContactInfoVO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.JsonUtil;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.MyStringUtil;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

/**
 * @author EX-LUOBING002
 * @description 联系信息变更对象转换器
 * @date 2026-02-11
 */
@Mapper(componentModel = "spring")
public interface ChangeContactInfoConverter extends BaseTransactionConverter {

    /**
     * 静态实例方式（非Spring管理）
     */
    ChangeContactInfoConverter INSTANCE = Mappers.getMapper(ChangeContactInfoConverter.class);

    /**
     * changeContactInfoBO 转换为 ChangeContactInfo
     *
     * @param changeContactInfoBO changeContactInfoBO
     * @param transactionId 交易ID
     * @param changeId 变更ID
     * @return ChangeContactInfo
     * @author EX-LUOBING002
     * @date 2026-02-11
     **/
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    @Mapping(target = "isFinal", constant = "Y")
    @Mapping(target = "transactionId", source = "transactionId")
    ChangeContactInfo toChangeContactInfo(ChangeContactInfoBO changeContactInfoBO, String transactionId, String changeId);

    /**
     * changeContactInfoBO 转换为 Transaction
     *
     * @param changeContactInfoBO changeContactInfoBO
     * @param transactionId 交易ID
     * @return Transaction
     * @author EX-LUOBING002
     * @date 2026-02-11
     **/
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    @Mapping(target = "transactionId", source = "transactionId")
    @Mapping(target = "transactionType", constant = "contactDetails")
    @Mapping(target = "serviceResult", constant = "in processing")
    Transaction toTransaction(ChangeContactInfoBO changeContactInfoBO, String transactionId);

    /**
     * changeContactInfo 转换为 ChangeContactInfoDto
     *
     * @param changeContactInfo changeContactInfo
     * @return ChangeContactInfoDto
     * @author EX-LUOBING002
     * @date 2026-02-12
     **/
    ChangeContactInfoDto toChangeContactInfoDto(ChangeContactInfo changeContactInfo);

    /**
     * contactInfoDtot 转换为 ChangeContactInfoVO
     *
     * @param contactInfoDtot contactInfoDtot
     * @return ChangeContactInfoVO
     * @author EX-LUOBING002
     * @date 2026-02-12
     **/
    ChangeContactInfoVO toChangeContactInfoVo(ChangeContactInfoDto contactInfoDtot);

    /**
     * value 转换为 BaseCustomerColInfoVO
     *
     * @param value value
     * @return BaseCustomerColInfoVO
     * @author EX-LUOBING002
     * @date 2026-02-12
     **/
    default BaseCustomerColInfoVO toBaseCustomerColInfoVO(String value) {
        if (MyStringUtil.isBlank(value)) {
            return null;
        }
        return JsonUtil.toBean(value, BaseCustomerColInfoVO.class);
    }
}
```

## 使用方式
在Service层可通过以下两种方式使用：

**方式1：Spring注入（推荐）**
```java
@Autowired
private ChangeContactInfoConverter changeContactInfoConverter;

// 调用转换方法
ChangeContactInfo changeContactInfo = changeContactInfoConverter.toChangeContactInfo(changeContactInfoBO, transactionId, changeId);
Transaction transaction = changeContactInfoConverter.toTransaction(changeContactInfoBO, transactionId);
```

**方式2：静态实例方式（非Spring管理）**
```java
ChangeContactInfoConverter converter = ChangeContactInfoConverter.INSTANCE;

// 调用转换方法
ChangeContactInfo changeContactInfo = converter.toChangeContactInfo(changeContactInfoBO, transactionId, changeId);
Transaction transaction = converter.toTransaction(changeContactInfoBO, transactionId);
```

# 要求
- 生成的文件放到对应目录，windows系统，没有则创建
- 转换类接口放到 {包路径}/service/assembler 目录下
- 文件命名规范：{业务名称}Converter.java
- 包路径规范：{包路径}.service.assembler
- 必须继承 BaseTransactionConverter 接口
- 使用 @Mapper(componentModel = "spring") 注解
- 方法命名规范：使用驼峰命名，格式为 {源对象}To{目标对象}
- 必须包含 INSTANCE 静态实例定义：{业务名称}Converter INSTANCE = Mappers.getMapper({业务名称}Converter.class);


