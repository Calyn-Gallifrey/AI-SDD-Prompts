## 目标
为指定的静态 Java 工具类中的 **public static 方法** 生成 **JUnit 4 单元测试代码**，并输出可直接复制到 `src/test/java` 运行的完整测试类。

## 背景1 测试类和测试方法命名要求
1. 工具类只含 `public static` 方法，可独立测试。
2. 项目使用 JUnit 4。
3. 测试代码需符合团队规约：
    - 类名：`{被测类}Test`
    - 包名：与被测类相同（位于 `src/test/java` 对应包下）
    - 方法名：`test{被测方法名}_{场景}`
    - 使用 JUnit 4 断言 API（`org.junit.Assert`）
    - 使用 `@Test` 注解（来自 `org.junit.Test`）

## 背景2 参考示例（MyDocumentHelperTest）
```java
package com.ocft.iic.uaw.server.modules.transaction.core.mydocument.service.helper;

import com.ocft.iic.uaw.server.modules.transaction.core.mydocument.pojo.dto.MyDocumentDTO;
import com.ocft.iic.uaw.server.modules.transaction.core.mydocument.pojo.dto.MyDocumentInformationDTO;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.Assert.*;

/**
 * MyDocumentHelper 单元测试
 *
 * @author EX-SHANGHONG336
 */
public class MyDocumentHelperTest {

    /**
     * 测试 buildDocumentInformationDTO 方法 - 正常场景
     */
    @Test
    public void testBuildDocumentInformationDTO_Success() {
        // 准备测试数据
        MyDocumentInformationDTO dto = new MyDocumentInformationDTO();
        MyDocumentDTO document = new MyDocumentDTO();
        document.setDocumentSource("testSource");
        List<MyDocumentDTO> documents = new ArrayList<>();
        documents.add(document);
        dto.setDocuments(documents);

        // 执行测试
        List<MyDocumentInformationDTO> resultList = MyDocumentHelper.buildDocumentInformationDTO(dto);

        // 断言结果
        assertNotNull(resultList);
        assertEquals(1, resultList.size());
        assertNotNull(resultList.get(0));
        assertNotNull(resultList.get(0).getDocuments());
        assertEquals(1, resultList.get(0).getDocuments().size());
        assertEquals("testSource", resultList.get(0).getDocuments().get(0).getDocumentSource());
    }

    /**
     * 测试 buildDocumentInformationDTO 方法 - dto 为 null
     * 注意：根据实际代码逻辑，如果方法会将 null 添加到列表中，应断言 resultList.get(0) 为 null
     */
    @Test
    public void testBuildDocumentInformationDTO_NullDto() {
        // 执行测试
        List<MyDocumentInformationDTO> resultList = MyDocumentHelper.buildDocumentInformationDTO(null);

        // 断言结果
        assertNotNull(resultList);
        assertEquals(1, resultList.size());
        assertNull(resultList.get(0));
    }
}
```

## 背景3 依赖字段初始化的处理
某些工具类方法会依赖 DTO 中的字段（如 `uniqueBrands`、`needSplit` 等），在调用这些方法前需要先初始化相关字段。此时应：
1. 先调用相应的 getter 方法或工具类方法获取值
2. 通过 setter 方法手动设置字段值
3. 确保后续方法调用时不会出现空指针异常

**示例：**
```java
@Test
public void testGetSplitFlag_NeedSplit() {
    // 准备测试数据
    AgreementInformationDTO dto = new AgreementInformationDTO();
    // ... 设置 agreements 等字段 ...

    // 先设置依赖字段，避免 getSplitFlag 调用时出现空指针
    dto.setUniqueBrands(AgreementInformationHelper.getUniqueBrands(dto));

    // 执行测试
    Boolean needSplit = AgreementInformationHelper.getSplitFlag(dto);

    // 断言结果
    assertNotNull(needSplit);
    assertTrue(needSplit);
}
```

## 背景3-1 依赖字段初始化的链式调用处理
当工具类方法之间存在链式调用关系时，需要确保每个方法调用前都已初始化依赖字段。**特别注意：** `getSplitFlag` 方法内部会调用 `getUniqueBrands` 方法，因此在调用 `getSplitFlag` 前不需要预先设置 `uniqueBrands` 字段，但如果 `getUniqueBrands` 方法本身依赖 DTO 的字段（如 agreements、brand），则需要确保这些字段已正确设置。

**AgreementInformationHelper 链式调用示例：**
```java
// getSplitFlag 方法内部调用 getUniqueBrands 方法
public static Boolean getSplitFlag(AgreementInformationDTO agreementInformationDTO) {
    return agreementInformationDTO.getUniqueBrands().size() >= NEED_SPLIT_TRANSACTION_BRAND_TOTAL;
}

// getUniqueBrands 方法依赖 agreements 和 brand 字段
public static Set<String> getUniqueBrands(AgreementInformationDTO agreementInformationDTO) {
    Set<String> brandSet = new HashSet<>();
    if (MyCollectionUtil.isNotEmpty(agreementInformationDTO.getAgreements())) {
        agreementInformationDTO.getAgreements().forEach(agree -> {
            if (MyStringUtil.isNotBlank(agree.getBrand()) && MyStringUtil.isNotBlank(agree.getBrand().trim())) {
                brandSet.add(agree.getBrand().trim());
            }
        });
    }
    if (MyStringUtil.isNotBlank(agreementInformationDTO.getBrand()) && MyStringUtil.isNotBlank(agreementInformationDTO.getBrand().trim())) {
        brandSet.add(agreementInformationDTO.getBrand().trim());
    }
    return brandSet;
}

// 正确的测试方式：先设置 agreements 和 brand，再调用 getSplitFlag
@Test
public void testGetSplitFlag_NeedSplit() {
    // 准备测试数据
    AgreementInformationDTO dto = new AgreementInformationDTO();
    
    AgreementDTO agreement1 = new AgreementDTO();
    agreement1.setBrand("BrandA");
    
    AgreementDTO agreement2 = new AgreementDTO();
    agreement2.setBrand("BrandB");
    
    List<AgreementDTO> agreements = new ArrayList<>();
    agreements.add(agreement1);
    agreements.add(agreement2);
    dto.setAgreements(agreements);
    
    // 先设置唯一品牌集合，避免 getSplitFlag 调用时出现空指针
    dto.setUniqueBrands(AgreementInformationHelper.getUniqueBrands(dto));

    // 执行测试
    Boolean needSplit = AgreementInformationHelper.getSplitFlag(dto);

    // 断言结果
    assertNotNull(needSplit);
    assertTrue(needSplit);
}
```

## 背景4 集合初始化规范
为避免使用 Java 8 的 Collectors API（某些项目可能不支持），请使用以下方式初始化集合：
1. 使用 `new HashSet<>(Arrays.asList(...))` 替代 `java.util.stream.Collectors.toSet()`
2. 使用 `new ArrayList<>()` 替代 `Arrays.asList()` 直接作为字段值
3. 使用 `new HashSet<>()` 替代 `java.util.HashSet<>`

**示例：**
```java
// 正确的集合初始化方式
Set<String> brands = new HashSet<>(Arrays.asList("BrandA", "BrandB"));
List<AgreementDTO> agreements = new ArrayList<>();
agreements.add(agreement1);
```

## 要求
1. 必须使用 JUnit 4 注解（`@Test` 来自 `org.junit.Test`）
2. 断言使用 JUnit 4 的断言 API（如 `assertTrue`、`assertFalse`、`assertEquals`、`assertNotNull`、`assertNull`）
3. 每个测试方法应包含：准备测试数据、执行测试、断言结果三个步骤
4. 对于可能抛出异常的场景，应使用 try-catch 捕获并验证异常
5. 对于依赖 DTO 字段的工具类方法，需先初始化相关字段，确保测试正常运行
6. 集合初始化请使用标准方式（`new HashSet<>(Arrays.asList(...))`、`new ArrayList<>()`），避免使用 Java 8 的 Collectors API

## 背景6 空值处理注意事项
某些工具类方法在处理 null 参数时会将 null 添加到返回的列表中（如 `resultList.add(null)`），此时测试断言应为：
- `assertNotNull(resultList)` - 列表不为 null
- `assertEquals(1, resultList.size())` - 列表大小为 1
- `assertNull(resultList.get(0))` - 列表中的元素为 null

**示例：**
```java
@Test
public void testBuildDocumentInformationDTO_NullDto() {
    // 执行测试
    List<MyDocumentInformationDTO> resultList = MyDocumentHelper.buildDocumentInformationDTO(null);

    // 断言结果
    assertNotNull(resultList);
    assertEquals(1, resultList.size());
    assertNull(resultList.get(0));
}
```

## 背景7 异常处理注意事项
对于不支持 null 值的方法（如 stream 操作或访问 null 对象的字段），当参数为 null 时会抛出 NullPointerException，此时应使用 `@Test(expected = NullPointerException.class)` 注解进行测试，并在测试方法末尾调用 `fail()` 方法。

**示例：**
```java
@Test(expected = NullPointerException.class)
public void testGetUniqueBrands_NullDto() {
    // 执行测试
    AgreementInformationHelper.getUniqueBrands(null);
    fail("Expected NullPointerException to be thrown");
}
```

**注意：** 当使用 `@Test(expected = NullPointerException.class)` 注解时，如果方法确实抛出了指定异常，测试将通过；但如果方法没有抛出异常，测试将失败。因此需要在测试方法末尾调用 `fail()` 方法，确保在异常未被抛出时测试也能正确失败。