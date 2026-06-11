# 目标
本规则用于根据数据库表结构创建符合项目规范要求的 MyBatis ORM 代码。

# 背景

## 背景1：获取用户输入的上下文信息
+ 用户输入：{ORM代码所在业务包package位置}
+ 用户输入：{ORM代码生成类型}
+ 用户输入：{表结构定义}
+ 用户输入：{业务场景描述}

## 背景2：新增表的标准ORM代码生成
* 如果{ORM代码生成类型}为**新增表的标准ORM代码生成**，则根据{表结构定义}新增创建该表的标准mybatis的CRUD的代码
* mybatis的mapper接口类根据表名命名XxxMapper.java，生成代码到 {ORM代码所在业务包package位置}/dao/mapper
* mybatis的mapper接口类需要加注解@Repository
* mybatis的mapper的xml根据表名命名XxxMapper.xml，生成代码到 {ORM代码所在业务包package位置}/dao/mapper
```
mybatis的mapper接口类 示例
package com.ocft.iic.uaw.server.modules.transaction.core.mydocument.dao.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.ocft.iic.uaw.server.modules.transaction.core.mydocument.dao.entity.MyDocument;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * My Document 工单 Mapper 接口
 * <p>提供文档信息的数据库操作方法</p>
 * @author EX-SHANGHONG336
 * @see MyDocument 文档实体
 * @see BaseMapper 基础 Mapper 接口
 * @since 1.0.0
 */
@Repository
public interface MyDocumentMapper extends BaseMapper<MyDocument> {

    /**
     * 批量插入文档明细信息
     * @param infoList 文档详细信息列表
     */
    void batchInsertDocumentInformation(List<MyDocument> infoList);
}
```
* Mapper接口类对应的XML文件示例：
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.ocft.iic.uaw.server.modules.transaction.core.mydocument.dao.mapper.MyDocumentMapper">

    <insert id="batchInsertDocumentInformation"
            parameterType="java.util.List">
        INSERT INTO iic_crm_transaction_my_document (
            transaction_id,
            document_id,
            name,
            description,
            data,
            source,
            line_of_business,
            content_type,
            create_date,
            agreement_number,
            client_number,
            document_type,
            effective_date,
            document_source,
            created_by,
            updated_by
        ) VALUES
        <foreach collection="list" item="item" separator=",">
            (
                #{item.transactionId},
                #{item.documentId},
                #{item.name},
                #{item.description},
                #{item.data},
                #{item.source},
                #{item.lineOfBusiness},
                #{item.contentType},
                #{item.createDate},
                #{item.agreementNumber},
                #{item.clientNumber},
                #{item.documentType},
                #{item.effectiveDate},
                #{item.documentSource},
                #{item.createdBy},
                #{item.updatedBy}
            )
        </foreach>
    </insert>
</mapper>
```
* 根据表结构创建Entity实体类根据表明命名XxxEntity.java,生成代码到 {ORM代码所在业务包package位置}/dao/entity
* Entity实体类中加上表字段的主键
```
Entity实体类代码示例：
package com.ocft.iic.uaw.server.modules.transaction.core.mydocument.dao.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.BaseTransactionEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * My Document 工单实体类
 * @author EX-SHANGHONG336
 * @see BaseTransactionEntity 基础交易实体
 * @since 1.0.0
 */
@EqualsAndHashCode(callSuper = false)
@Data
@TableName("iic_crm_transaction_my_document")
@ApiModel(description = "My Document 工单实体")
public class MyDocument extends BaseTransactionEntity {

    private static final long serialVersionUID = 1L;

    @TableField("document_id")
    @ApiModelProperty(value = "文档ID")
    private String documentId;

    @TableField("name")
    @ApiModelProperty(value = "文档名称")
    private String name;

    @TableField("description")
    @ApiModelProperty(value = "文档描述")
    private String description;

    @TableField("data")
    @ApiModelProperty(value = "文档数据")
    private String data;

    @TableField("source")
    @ApiModelProperty(value = "文档来源")
    private String source;

    @TableField("line_of_business")
    @ApiModelProperty(value = "业务线")
    private String lineOfBusiness;

    @TableField("content_type")
    @ApiModelProperty(value = "内容类型")
    private String contentType;

    @TableField("create_date")
    @ApiModelProperty(value = "创建日期")
    private String createDate;

    @TableField("agreement_number")
    @ApiModelProperty(value = "协议编号")
    private String agreementNumber;

    @TableField("client_number")
    @ApiModelProperty(value = "客户编号")
    private String clientNumber;

    @TableField("document_type")
    @ApiModelProperty(value = "文档类型")
    private String documentType;

    @TableField("effective_date")
    @ApiModelProperty(value = "生效日期")
    private String effectiveDate;

    @TableField("document_source")
    @ApiModelProperty(value = "文档来源类型（GENERATED/LIST）")
    private String documentSource;
}
```
* Entity实体类需要继承BaseTransactionEntity基类
* BaseTransactionEntity基类包含主键id（自增）和交易编号transactionId字段
* 使用@TableField注解映射数据库字段
* 使用@TableName注解指定数据库表名
* 使用@ApiModel和@ApiModelProperty注解添加API文档说明

## 背景3：存量表单场景ORM代码生成
* 如果{ORM代码生成类型}为**存量表单场景ORM代码生成**，则根据{表结构定义}和{业务场景描述}创建增量代码
* 在{ORM代码所在业务包package位置}/dao/mapper，寻找对应的Mapper接口类和xml文件进行修改
* 在{ORM代码所在业务包package位置}/dao/entity，寻找对应Entity实体类进行修改

## 背景4：存量表多表关联查询场景ORM代码生成
* 如果{ORM代码生成类型}为**存量表多表关联查询ORM代码生成**，则根据{表结构定义}和{业务场景描述}新增创建mapper接口类、xml文件、查询输入参数、结果集返回参数
* 在{ORM代码所在业务包package位置}/dao/mapper 新增创建mapper类和xml文件
* 在{ORM代码所在业务包package位置}/pojo/dto 创建业务场景的查询输入参数XxxInputDto和结果集返回参数XxxResultDto
```
查询输入参数示例：

package com.ocft.iic.uaw.server.modules.transaction.common.transaction.pojo.dto;

import lombok.Data;

import java.io.Serializable;

/**
 * @author EX-XUEBO158
 */
@Data
public class AgreementDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    private String brand;

    private String policyNumber;

    private String productCode;

    private String carrierAdminSystem;

    private String productSystemId;

    private String agreementName;

    private String coverAmount;

    private String status;
}
```

```
结果集返回参数示例：

package com.ocft.iic.uaw.server.modules.transaction.base.pojo.bo;

import com.ocft.iic.uaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import javax.validation.constraints.NotBlank;
import java.io.Serializable;

/**
 * @author EX-XUEBO158
 */
@ApiModel(description = "基础交易请求数据传输对象，用于接收前端提交的交易信息")
@Data
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class BaseTransactionBO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "前端防重提交 token，用于防止重复提交", required = true,example = "0E517EAAFA054092-4ecc86ad-8494-411f-b0c2-b1f314b5ae43")
    @NotBlank(message = "requestToken is empty")
    private String requestToken;

    @ApiModelProperty(value = "联系人ID，不能为空", required = true,example ="1dc05b65-a837-4e37-99b2-640473759e2d")
    @NotBlank(message = "contactId is empty")
    private String contactId;

    @ApiModelProperty(value = "参考编号，不能为空", required = true,example ="CST2602000012")
    @NotBlank(message = "referenceNumber is empty")
    private String referenceNumber;

    @ApiModelProperty(value = "互动ID，不能为空", required = true,example ="CST2602000012")
    @NotBlank(message = "interactionId is empty")
    private String interactionId;

    @ApiModelProperty(value = "坐席ID，不能为空", required = true,example ="BBDDA47BE1BF4C51")
    @NotBlank(message = "agentId is empty")
    private String agentId;

    @ApiModelProperty(value = "客户ID，不能为空", required = true,example ="K1LLXSIUEG2HM")
    @NotBlank(message = "customerId is empty")
    private String customerId;

    @ApiModelProperty(value = "交易类型，不能为空", required = true,example ="contactDetails")
    @NotBlank(message = "transactionType is empty")
    private String transactionType;

    @ApiModelProperty(value = "父交易ID，不能为空", required = true,example ="SIT2602000065")
    @NotBlank(message = "parentTransactionId is empty")
    private String parentTransactionId;
}
```

## 背景5：MapStruct转换器
* 在{ORM代码所在业务包package位置}/service/converter 创建业务场景的转换器XxxConverter.java
* 使用MapStruct进行实体转换
```
MapStruct转换器示例：

package com.ocft.iic.uaw.server.modules.transaction.common.transaction.service.converter;

import com.ocft.iic.uaw.server.modules.transaction.base.converter.BaseTransactionConverter;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.AgreementChecked;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.Transaction;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.pojo.dto.AgreementDTO;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.pojo.dto.EnquiryInformationDTO;
import org.mapstruct.Context;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.util.List;
import java.util.stream.Collectors;

/**
 * @author EX-XUEBO158
 */
@Mapper(componentModel = "spring")
public interface EnquiryInformationConverter extends BaseTransactionConverter {

    /**
     * 从工单数据对象 抽取 主表的entity 对象
     *
     * @param enquiryInformationDTO 一般工单表单数据
     * @param transactionId         id
     * @return entity
     */
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    @Mapping(target = "transactionId", source = "transactionId")
    Transaction convertToTransaction(EnquiryInformationDTO enquiryInformationDTO, String transactionId);

    /**
     * 将 AgreementDTO 转换为 AgreementChecked，设置 transactionId  createdBy updatedBy
     *
     * @param agreementDTO  选中的合同/协议
     * @param transactionId id
     * @return entity
     */
    @Mapping(target = "createdBy", expression = "java(currentUser())")
    @Mapping(target = "updatedBy", expression = "java(currentUser())")
    @Mapping(target = "transactionId", source = "transactionId")
    AgreementChecked convertToAgreementChecked(AgreementDTO agreementDTO, String transactionId);

    /**
     * 批量转换：将 List<agreementDTO> 转换为 List<AgreementChecked>
     *
     * @param agreementDTOList 选中的合同/协议
     * @param transactionId    id
     * @return entity
     */
    default List<AgreementChecked> convertToAgreementCheckedList(List<AgreementDTO> agreementDTOList, @Context String transactionId) {
        if (agreementDTOList == null) {
            return null;
        }
        return agreementDTOList.stream()
                .map(dto -> convertToAgreementChecked(dto, transactionId))
                .collect(Collectors.toList());
    }
}
```

## 背景6：MyBatis XML文件编写规范
* XML文件放在 {ORM代码所在业务包package位置}/src/main/resources/mapper/{模块路径} 目录下
* XML文件命名与Mapper接口类名保持一致（XxxMapper.xml）
* XML文件的namespace必须与Mapper接口类的全限定名一致
* 插入语句使用<foreach>标签实现批量插入
```XML
文件示例：

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.ocft.iic.uaw.server.modules.transaction.core.mydocument.dao.mapper.MyDocumentMapper">

    <insert id="batchInsertDocumentInformation"
            parameterType="java.util.List">
        INSERT INTO iic_crm_transaction_my_document (
            transaction_id,
            document_id,
            name,
            description,
            data,
            source,
            line_of_business,
            content_type,
            create_date,
            agreement_number,
            client_number,
            document_type,
            effective_date,
            document_source,
            created_by,
            updated_by
        ) VALUES
        <foreach collection="list" item="item" separator=",">
            (
                #{item.transactionId},
                #{item.documentId},
                #{item.name},
                #{item.description},
                #{item.data},
                #{item.source},
                #{item.lineOfBusiness},
                #{item.contentType},
                #{item.createDate},
                #{item.agreementNumber},
                #{item.clientNumber},
                #{item.documentType},
                #{item.effectiveDate},
                #{item.documentSource},
                #{item.createdBy},
                #{item.updatedBy}
            )
        </foreach>
    </insert>
</mapper>
```
* 查询语句使用<where>标签动态生成WHERE条件
```XML
<select id="queryTransactionByCondition" 
        parameterType="com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.dto.TransactionQueryDto"
        resultType="com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.entity.Transaction">
    SELECT 
        id,
        transaction_id,
        contact_id,
        reference_number,
        interaction_id,
        agent_id,
        customer_id,
        transaction_type,
        parent_transaction_id,
        operate_flag,
        service_result,
        cancel_reason,
        cancel_observations,
        created_by,
        updated_by,
        created_date,
        updated_date
    FROM iic_crm_transaction
    <where>
        <if test="customerId != null and customerId != ''">
            AND customer_id = #{customerId}
        </if>
        <if test="contactId != null and contactId != ''">
            AND contact_id = #{contactId}
        </if>
        <if test="transactionType != null and transactionType != ''">
            AND transaction_type = #{transactionType}
        </if>
        <if test="operateFlag != null and operateFlag != ''">
            AND operate_flag = #{operateFlag}
        </if>
    </where>
    ORDER BY created_date DESC
</select>
```

# 要求
1. 根据背景1明确获取我输入的信息
2. 明确区分{ORM代码生成类型}类型，选择相应的背景规范进行代码生成
3. 按照背景规范要求的代码生成位置准确生成，避免自由生成代码位置
4. 使用MyBatis-Plus作为ORM框架
5. Entity实体类需要继承BaseTransactionEntity基类
6. Mapper接口类需要继承BaseMapper<T>并添加@Repository注解
7. 使用Lombok注解简化代码（@Data, @EqualsAndHashCode, @TableName, @TableField）
8. 使用MapStruct进行实体转换，实现DTO/BO与Entity之间的转换
9. XML文件namespace必须与Mapper接口类的全限定名一致
10. XML文件放在src/main/resources/mapper/{模块路径}目录下
11. 使用<foreach>标签实现批量插入
12. 使用<where>标签动态生成WHERE条件