```
**任务**
你是一名资深的开发专家，请针对[用户选中代码]按照以下步骤生成单元测试用例。

**步骤**
1. 分析代码结构：
  - 如果选中的是单个方法，分析{{选中函数}}的输入参数、返回值和业务逻辑
  - 如果选中的是多个方法，遍历代码中的所有public方法，分析每个方法的参数、返回值和业务逻辑

2. 构造测试数据：
  - 根据方法的入参出参，结合[类定义]信息，构造不同场景的测试数据
  - 特别关注边界条件和异常情况的测试数据构造

3. 分析方法特性：
  - 分析方法的分支条件
  - 分析方法的边界条件
  - 分析可能的异常情况

4. 生成测试用例：
  - 按照[测试场景]，严格仿照[示例]格式生成可执行的单元测试用例，尤其注意注释内容要全面
  - 使用指定的[mock框架]和[单测框架]进行生成，严禁混用同类框架
  - 生成单元测试用例时务必严格遵守[基本要求]与[团队自定义要求](如果有)

**测试场景**
1. 分支逻辑测试：为每个分支逻辑生成独立的测试用例
2. 边界条件测试：为每种边界情况生成独立的测试用例
3. 异常处理测试：为每种异常情况生成独立的测试用例

**指定框架**
1. mock框架：Mockito
2. 单测框架：JUnit

**基本要求**
1. 测试方法命名规则：test_被测试函数名称_用例场景_expect_预期结果
2. 模拟规则：仅对存在@Autowired注解的成员变量进行mock
3. 单一场景测试：每个测试方法只测试一种情况
4. 注释：添加详细的注释，为生成的类、方法及方法内每一行代码生成中文注释说明，注释需避免过于宽泛的描述
5. 包导入：确保不要导入不存在的包
6. 断言：每个测试方法必须有明确的assert代码和相关注释说明
7. 覆盖率要求：单元测试100%行覆盖率，100%分支覆盖、100%逻辑覆盖
8. 聚焦结果：无需贴出分析步骤，只返回生成的单测用例，以markdown格式展示

**团队自定义要求**
- 无

**示例**
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.when;

/**
 * 针对OmCustomerContactInformationServiceImpl类的单元测试集
 * 测试客户联系信息查询功能，包括成功场景和空值场景
 * @author EX-YUANLEI246
 */
@RunWith(MockitoJUnitRunner.class)
public class OmCustomerContactInformationServiceImplTest {

    @Mock
    private OMCustomerServiceImpl omCustomerService;

    @InjectMocks
    private OmCustomerContactInformationServiceImpl informationService;

    /**
     * 测试 queryOmCustomerContactInformation 方法 - 成功场景
     * 构建完整的客户信息Mock数据，验证方法在正常情况下的处理逻辑
     */
    @Test
    public void testQueryOmCustomerContactInformation_Success() {
        // 构建完整的Portfolio响应数据，用于模拟成功获取客户信息的场景
        OmCustomer customerDetail = buildMockOmCustomer();
        String customerId = "CUSTOMER001";
        // 模拟调用OM客户详情服务，返回构建的Mock数据
        when(omCustomerService.getCustomerDetail(customerId)).thenReturn(customerDetail);
        // 执行测试，调用查询客户联系信息方法
        ChangeContactInfoVO changeContactInfoVO = informationService.queryOmCustomerContactInformation(customerId);
        // 验证返回结果非空，确保方法正常返回联系信息VO对象
        assertNotNull(changeContactInfoVO);
    }

    /**
     * 测试 queryOmCustomerContactInformation 方法 - 空值场景
     * 构建部分字段为空的客户信息Mock数据，验证方法在空值情况下的处理逻辑
     */
    @Test
    public void testQueryOmCustomerContactInformation_Null() {
        // 构建部分字段为空的Portfolio响应数据，用于模拟客户信息不完整的情况
        OmCustomer customerDetail = buildMockOmCustomer_Null();
        String customerId = "CUSTOMER001";
        // 模拟调用OM客户详情服务，返回构建的空值Mock数据
        when(omCustomerService.getCustomerDetail(customerId)).thenReturn(customerDetail);
        // 执行测试，调用查询客户联系信息方法
        ChangeContactInfoVO changeContactInfoVO = informationService.queryOmCustomerContactInformation(customerId);
        // 验证返回结果非空，确保方法在空值情况下仍能正常返回VO对象
        assertNotNull(changeContactInfoVO);
    }

    /**
     * 构建 Mock 的 Portfolio 对象 - 完整数据
     * 使用JSON字符串构建包含电话、邮箱和地址的完整客户信息Mock数据
     */
    private OmCustomer buildMockOmCustomer() {
        String jsonStr = "{\n" +
                "\t" + ""customerNumber": "K1LLXSIUEG2HM",\n" +
                "\t" + "phoneNumbers": [\n" +
                "\t\t{\n" +
                "\t\t\t"phoneType": "Home Cellular Number",\n" +
                "\t\t\t"country": "South Africa",\n" +
                "\t\t\t"number": "+27 0814987280",\n" +
                "\t\t\t"isPramary": "1"\n" +
                "\t\t}"\n" +
                "\t]\n" +
                "\t" + "emailAddresses": [\n" +
                "\t\t{\n" +
                "\t\t\t"emailType": "Home Email Address",\n" +
                "\t\t\t"email": "PJOUBERT2@VODAMAIL.CO.ZA",\n" +
                "\t\t\t"isPramary": "1"\n" +
                "\t\t}"\n" +
                "\t]\n" +
                "\t" + "addresses": [\n" +
                "\t\t{\n" +
                "\t\t\t"type": "Home Residential Address",\n" +
                "\t\t\t"line1": "HIGHLANDS ALEJA ALAPIASTRAAT 9,LYTTELTON",\n" +
                "\t\t\t"line2": "",\n" +
                "\t\t\t"line3": "",\n" +
                "\t\t\t"line4": "",\n" +
                "\t\t\t"country": "South Africa",\n" +
                "\t\t\t"postalCode": "0157",\n" +
                "\t\t\t"isPramary": "1"\n" +
                "\t\t}"\n" +
                "\t]\n" +
                "}";
        return JSON.parseObject(jsonStr, OmCustomer.class);
    }

    /**
     * 构建 Mock 的 Portfolio 对象 - 空值数据
     * 使用JSON字符串构建部分字段为空的客户信息Mock数据
     */
    private OmCustomer buildMockOmCustomer_Null() {
        String jsonStr = "{\n" +
                "\t" + ""customerNumber": "K1LLXSIUEG2HM",\n" +
                "\t" + "phoneNumbers": [\n" +
                "\t\t{\n" +
                "\t\t\t"phoneType": "Home Cellular Number",\n" +
                "\t\t\t"country": "South Africa",\n" +
                "\t\t\t"number": "+27 0814987280",\n" +
                "\t\t\t"isPramary": "1"\n" +
                "\t\t}"\n" +
                "\t]\n" +
                "\t" + "emailAddresses": [\n" +
                "\t\t{\n" +
                "\t\t\t"emailType": "Home Email Address",\n" +
                "\t\t\t"email": "PJOUBERT2@VODAMAIL.CO.ZA",\n" +
                "\t\t\t"isPramary": "1"\n" +
                "\t\t}"\n" +
                "\t]\n" +
                "}";
        return JSON.parseObject(jsonStr, OmCustomer.class);
    }
}

**类定义**
1.方法入参出参类定义
```java
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
 * @author EX-LUOBING002
 * @description
 * @date 2026-02-10
 */
@Data
@ApiModel(description = "本次联系信息变更详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeContactInfoVO implements Serializable {

    @ApiModelProperty(value = "电话信息列表")
    private List<ChangePhonesDetailVO> phoneList;

    @ApiModelProperty(value = "邮箱信息列表")
    private List<ChangeEmailsDetailVO> emailList;

    @ApiModelProperty(value = "地址信息列表")
    private List<ChangeAddressDetailVO> addressList;

    @ApiModelProperty(value = "工单id")
    private String transactionId;

    @ApiModelProperty(value = "操作标志：submit（提交）或 cancel（取消）", required = true)
    private String operateFlag;
}
```

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.iaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @description
 * @author EX-LUOBING002
 * @date 2026-02-10
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

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.iaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @description
 * @author EX-LUOBING002
 * @date 2026-02-10
 */
@Data
@ApiModel(description = "联系信息变更-电话详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangePhonesDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key")
    private String uniqueKey;

    @ApiModelProperty(value = "电话类型")
    private BaseCustomerColInfoVO phoneType;

    @ApiModelProperty(value = "国家")
    private BaseCustomerColInfoVO country;

    @ApiModelProperty(value = "国际区号")
    private BaseCustomerColInfoVO diallingCode;

    @ApiModelProperty(value = "电话号码")
    private BaseCustomerColInfoVO number;

    @ApiModelProperty(value = "是否为默认电话")
    private BaseCustomerColInfoVO preferred;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("phoneType", phoneType)
                .add("country", country)
                .add("diallingCode", diallingCode)
                .add("number", number)
                .add("preferred", preferred)
                .toString();
    }
}
```

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.iaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @description
 * @author EX-LUOBING002
 * @date 2026-02-10
 */
@Data
@ApiModel(description = "联系信息变更-邮箱详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeEmailsDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key")
    private String uniqueKey;

    @ApiModelProperty(value = "邮箱类型")
    private BaseCustomerColInfoVO emailType;

    @ApiModelProperty(value = "邮箱地址")
    private BaseCustomerColInfoVO email;

    @ApiModelProperty(value = "是否为默认邮箱")
    private BaseCustomerColInfoVO preferred;

    @Override
    public String toString() {
        return ToStringUtil.toStringHelper(this)
                .add("uniqueKey", uniqueKey)
                .add("emailType", emailType)
                .add("email", email)
                .add("preferred", preferred)
                .toString();
    }
}
```

```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo;

import com.ocft.iic.iaw.server.modules.transaction.support.utils.ToStringUtil;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @description
 * @author EX-LUOBING002
 * @date 2026-02-10
 */
@Data
@ApiModel(description = "联系信息变更-地址详情VO")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChangeAddressDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "唯一key")
    private String uniqueKey;

    @ApiModelProperty(value = "地址类型")
    private BaseCustomerColInfoVO addressType;

    @ApiModelProperty(value = "地址行1")
    private BaseCustomerColInfoVO line1;

    @ApiModelProperty(value = "地址行2")
    private BaseCustomerColInfoVO line2;

    @ApiModelProperty(value = "地址行3")
    private BaseCustomerColInfoVO line3;

    @ApiModelProperty(value = "地址行4")
    private BaseCustomerColInfoVO line4;

    @ApiModelProperty(value = "国家")
    private BaseCustomerColInfoVO country;

    @ApiModelProperty(value = "邮政编码")
    private BaseCustomerColInfoVO postalCode;

    @ApiModelProperty(value = "是否为默认")
    private BaseCustomerColInfoVO preferred;

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

2.方法所在简化文件内容
```java
package com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.impl;

import com.ocft.iic.third.api.dto.rsp.OmCustomer;
import com.ocft.iic.uaw.server.modules.customer.service.impl.OMCustomerServiceImpl;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.OmCustomerContactInformationService;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.service.helper.OmCustomerContactInformationHelper;
import com.ocft.iic.uaw.server.modules.transaction.core.changecontactinfo.pojo.vo.ChangeContactInfoVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * @author EX-YUANLEI246
 */
@Service
public class OmCustomerContactInformationServiceImpl implements OmCustomerContactInformationService {

    @Autowired
    private OMCustomerServiceImpl omCustomerService;

    @Override
    public ChangeContactInfoVO queryOmCustomerContactInformation(String customerId) {
        //调用本地转接服务，获取客户信息
        OmCustomer customerDetail = omCustomerService.getCustomerDetail(customerId);
        // 解析结果转换成业务VO对象
        return OmCustomerContactInformationHelper.convertToChangeContactInfoVO(customerDetail);
    }
}
```

**用户选中代码**
{{选中文件内容}}
```
 