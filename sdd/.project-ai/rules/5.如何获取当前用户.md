# 目标
你是一个资深java开发专家，根据背景和要求实现获取当前用户ID的任务

# 背景
## 背景1：获取当前用户ID

### 场景1：MapStruct Converter 场景

**前提条件**：转换器需继承 `BaseTransactionConverter` 接口

在 MapStruct 转换器中，通过调用 `currentUser()` 方法获取用户ID：

```java
package com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.service.converter;

import com.ocft.iic.uaw.server.modules.transaction.base.converter.BaseTransactionConverter;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.dao.entity.PaymentInformation;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.pojo.bo.AgreementInformationBO;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.pojo.dto.AgreementInformationDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

/**
 * @author EX-XUEBO158
 */
@Mapper(componentModel = "spring")
public interface AgreementInformationConverter extends BaseTransactionConverter {

    /**
     * 将 agreementInformationDTO 对象转换为TransactionPaymentInfo对象
     *
     * @param agreementInformationDTO 源对象
     * @param transactionId           transactionId
     * @return 转换后的TransactionPaymentInfo对象
     */
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    @Mapping(target = "transactionId", source = "transactionId")
    PaymentInformation convertToTransactionPaymentInfo(AgreementInformationDTO agreementInformationDTO, String transactionId);

    /**
     * 将BO转为DTO
     *
     * @param agreementInformationBO 支付工单bo
     * @return 支付工单DTO
     */
    AgreementInformationDTO convertBoToDto(AgreementInformationBO agreementInformationBO);

}
```

**说明**：该方法定义在 `BaseTransactionConverter` 接口中：

```java
package com.ocft.iic.uaw.server.modules.transaction.base.converter;

import com.ocft.uaw.comm.api.context.UserContext;

import java.time.LocalDateTime;

/**
 * mapstruct公共映射方法
 *
 * @author ZHOUMINGWEI328
 */
public interface BaseTransactionConverter {

    /**
     * 返回当前登录用户的um,默认为system
     *
     * @return um
     */
    default String currentUser() {
        return UserContext.getUserId();
    }

    /**
     * 返回当前时间
     *
     * @return 当前时间
     */
    default LocalDateTime nowTime() {
        return LocalDateTime.now();
    }
}
```

### 场景2：Service 层场景

在 Service 实现类中，直接使用 `UserContext.getUserId()`：

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.impl;

import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo.ChangeContactInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.dto.ChangeContactInfoDTO;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.ChangeContactInfoService;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.converter.ChangeContactInfoConverter;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.MyStringUtil;
import com.ocft.uaw.comm.api.context.UserContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * @author EX-LUOBING002
 */
@Service
public class ChangeContactInfoServiceImpl implements ChangeContactInfoService {

    @Autowired
    private ChangeContactInfoConverter changeContactInfoConverter;

    @Override
    public void submitOrCancel(ChangeContactInfoBO changeContactInfoBO) {
        // 获取当前用户ID
        String userId = UserContext.getUserId();
        
        // 转换BO为DTO
        ChangeContactInfoDTO changeContactInfoDTO = changeContactInfoConverter.convertBoToDto(changeContactInfoBO);
        
        // 设置创建人和更新人
        changeContactInfoDTO.setCreatedBy(userId);
        changeContactInfoDTO.setUpdatedBy(userId);
        
        // 业务逻辑处理
        // ...
    }
}
```

### 场景3：Helper 类场景

在 Helper 工具类中，通过 `UserContext.getCurrentUser()` 获取 `LoginUserDTO` 对象后调用 `getUserId()`：

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.helper;

import com.ocft.iic.uaw.server.modules.transaction.base.constants.BaseConstants;
import com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo.BaseChangeCusInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.BaseChangeCusEntity;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.helper.CusEntityChangeHelper;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.bo.ChangeContactInfoBO;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.dto.BuildChangeDetailDto;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.MyStringUtil;
import com.ocft.uaw.comm.api.context.UserContext;

import java.util.List;
import java.util.stream.Collectors;

/**
 * @author EX-LUOBING002
 * @description
 * @date 2026-02-11
 */
public class ChangeContactInfoHelper {

    /**
     * 通用方法：根据BuildChangeDetailDto构建变更明细列表
     *
     * @param dto         变更详情DTO
     * @param entityClass 实体类Class对象
     * @param <T>         BO类型，需继承 BaseChangeCusInfoBO
     * @param <R>         实体类型，需继承 BaseChangeCusEntity
     * @return 填充后的变更明细列表
     */
    public static <T extends BaseChangeCusInfoBO, R extends BaseChangeCusEntity> List<R> buildChangeDetailList(
            BuildChangeDetailDto<T> dto,
            Class<R> entityClass) {

        // 1. 构建变更列表（含新增、删除、修改、未变更）
        List<R> changeList = CusEntityChangeHelper.buildChangeList(
                dto.getOldList(), dto.getNewList(), entityClass);

        // 2. 使用通用填充方法批量设置字段（避免多次 map）
        return changeList.stream()
                .map(entity -> setChangeIdAndTransactionId(entity, dto.getChangeId(), dto.getTransactionId()))
                .collect(Collectors.toList());
    }

    /**
     * 通用方法：设置变更 ID 与事务 ID
     *
     * @param entity        目标实体
     * @param changeId      变更 ID
     * @param transactionId 事务 ID
     * @param <T>           实体类型，需继承 BaseChangeCusEntity
     * @return 设置后的实体
     */
    public static <T extends BaseChangeCusEntity> T setChangeIdAndTransactionId(T entity, String changeId, String transactionId) {
        entity.setChangeId(changeId);
        entity.setTransactionId(transactionId);
        String userId = UserContext.getCurrentUser().getUserId();
        entity.setCreatedBy(userId);
        entity.setUpdatedBy(userId);
        return entity;
    }

    /**
     * 判断是否需要记录主表
     */
    public static boolean isRecordTransaction(ChangeContactInfoBO bo) {
        return MyStringUtil.isBlank(bo.getTransactionId())
                || BaseConstants.CANCEL_STR.equals(bo.getOperateFlag());
    }
}
```

## 背景2：关键类说明

| 类名 | 包路径 | 说明 |
|------|--------|------|
| `UserContext` | `com.ocft.uaw.comm.api.context.UserContext` | 提供 `getUserId()` 和 `getCurrentUser()` 方法获取用户信息 |
| `LoginUserDTO` | `com.ocft.uaw.comm.api.DTO.LoginUserDTO` | 包含用户信息的DTO，`getUserId()` 方法返回用户ID |
| `BaseTransactionConverter` | `com.ocft.iic.uaw.server.modules.transaction.base.converter.BaseTransactionConverter` | MapStruct 转换器基类接口，提供 `currentUser()` 方法 |

# 要求
1. 根据代码所在场景（Converter、Service、Helper），选择对应的方式获取当前用户ID
2. 在 MapStruct Converter 中，需继承 `BaseTransactionConverter` 接口，使用 `currentUser()` 方法
3. 在 Service 层中，直接使用 `UserContext.getUserId()` 获取用户ID
4. 在 Helper 工具类中，使用 `UserContext.getCurrentUser().getUserId()` 获取用户ID
 