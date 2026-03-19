# 目标
为指定的类生成 JUnit 4 单元测试代码，保证分支覆盖率 ≥ 80%，并输出可直接复制到 `src/test/java` 运行的完整测试类。

# 背景
## 背景1：不同类型的类及其测试特点

### Service/Strategy 类的特点
Service/Strategy 类是业务服务类，通常用于处理业务逻辑。这些类的特点包括：
1. 通常包含一个或多个 public 方法
2. 通常依赖 Spring Bean 组件（如 Mapper、Converter 等）
3. 依赖注入方式可能是字段注入（使用 @Autowired 或 @Mock）或构造函数注入
4. **可能需要模拟用户登录信息**
5. **测试时需要 mock 依赖的 Spring Bean 组件**

### Service/Strategy 继承父类的测试特点
当 Service/Strategy 类继承自父类（如 BaseEnquiryInformationSaveStrategy）时，需要注意：
1. 父类中定义的依赖字段需要通过 `getSuperclass().getDeclaredField()` 来获取
2. 子类中定义的依赖字段需要通过 `getDeclaredField()` 来获取
3. 在 setUp() 方法中注入依赖时，需要分别处理子类和父类的字段

## 背景2：测试类和测试方法命名要求
1. 测试类命名：被测试类名 + Test，例如：`PaymentInformationServiceStrategyImpl` 对应的测试类名为 `PaymentInformationServiceStrategyImplTest`
2. 包名：与被测类相同
3. 方法名：`test_{被测方法名}_{场景描述}`，例如：`test_checkData_normalCase`
4. 使用 AssertJ 断言（推荐），对于历史测试代码可以使用 JUnit Assert
5. 对于静态方法，使用 `@DisplayName` 描述测试场景
```

# 要求

## Service/Strategy 类的测试要求
1. 对 Service/Strategy 类的 public 方法进行单元测试
2. 依赖的 Spring Bean 组件（如 Mapper、Converter 等）需要进行 mock
3. 如果使用字段注入，需要在 `setUp()` 中通过反射注入 mock 对象
4. 如果使用构造函数注入，需要在 `setUp()` 中通过构造函数注入 mock 对象
5. 每个测试都需要模拟用户登录（除非测试场景明确不需要）
6. 不能 mock 项目的工具类，例如：MyStringUtil、MyJsonUtil、MyListUtil、MyDateUtil、MyCollectionUtil
7. 不能 mock 任何静态方法（除了用户登录模拟）
8. 使用 `@DisplayName` 梳理测试场景的中文描述
9. 保持测试代码简洁、可读性强，符合团队编码规范

## Service/Strategy 继承父类的测试要求
1. 如果 Service/Strategy 类继承自父类，需要分别处理子类和父类的依赖注入
2. 子类字段注入使用：`deathClaimEnquiryServiceStrategy.getClass().getDeclaredField("fieldName")`
3. 父类字段注入使用：`deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("fieldName")`

# 示例代码

## Service/Strategy 类的示例代码（不继承父类）

```java
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.dao.entity.PaymentInformation;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.dao.mapper.PaymentInformationMapper;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.pojo.dto.AgreementInformationDTO;
import com.ocft.iic.uaw.server.modules.transaction.core.agreementinformation.service.converter.AgreementInformationConverter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.verify;

/**
 * PaymentInformationServiceStrategyImpl 单元测试
 * 测试 saveDetailInformation 方法是否正确调用 converter 和 mapper
 *
 * @author EX-XUEBO158
 */
@RunWith(MockitoJUnitRunner.class)
public class PaymentInformationServiceStrategyImplTest {

    @Mock
    private PaymentInformationMapper paymentInfoMapper;

    @Mock
    private AgreementInformationConverter agreementInformationConvertor;

    @Captor
    private ArgumentCaptor<PaymentInformation> paymentInfoCaptor;

    private PaymentInformationServiceStrategyImpl paymentInformationServiceStrategy;

    @Before
    public void setUp() {
        // 初始化服务实例
        paymentInformationServiceStrategy = new PaymentInformationServiceStrategyImpl();
        
        // 注入 mock 的依赖
        try {
            java.lang.reflect.Field field = paymentInformationServiceStrategy.getClass().getDeclaredField("paymentInfoMapper");
            field.setAccessible(true);
            field.set(paymentInformationServiceStrategy, paymentInfoMapper);
            
            field = paymentInformationServiceStrategy.getClass().getDeclaredField("agreementInformationConvertor");
            field.setAccessible(true);
            field.set(paymentInformationServiceStrategy, agreementInformationConvertor);
        } catch (Exception e) {
            throw new RuntimeException("Failed to inject mocks: " + e.getMessage(), e);
        }
    }

    /**
     * 测试 saveDetailInformation 方法 - 成功场景
     * 验证 converter 被调用且 mapper 接收到正确的 PaymentInformation 对象
     */
    @Test
    public void testSaveDetailInformation_Success() {
        // 准备测试数据
        AgreementInformationDTO dto = new AgreementInformationDTO();
        dto.setBrand("BrandA");
        dto.setAdditionalInfo("Additional Info");

        String transactionId = "TXN123456";

        // 创建模拟的 PaymentInformation 对象
        PaymentInformation mockPaymentInfo = new PaymentInformation();
        mockPaymentInfo.setBrand("BrandA");
        mockPaymentInfo.setAdditionalInfo("Additional Info");
        mockPaymentInfo.setTransactionId(transactionId);

        // 模拟 converter 返回 PaymentInformation 对象
        doReturn(mockPaymentInfo).when(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 模拟 mapper 行为
        doNothing().when(paymentInfoMapper).insertPaymentInformation(any(PaymentInformation.class));

        // 执行测试
        paymentInformationServiceStrategy.saveDetailInformation(dto, transactionId);

        // 验证 mapper 被调用
        verify(paymentInfoMapper).insertPaymentInformation(paymentInfoCaptor.capture());

        // 验证捕获的 PaymentInformation 对象
        PaymentInformation capturedPaymentInfo = paymentInfoCaptor.getValue();
        assertNotNull(capturedPaymentInfo);
        assertEquals("BrandA", capturedPaymentInfo.getBrand());
        assertEquals("Additional Info", capturedPaymentInfo.getAdditionalInfo());
        assertEquals(transactionId, capturedPaymentInfo.getTransactionId());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 converter 被调用
     */
    @Test
    public void testSaveDetailInformation_ConverterCalled() {
        // 准备测试数据
        AgreementInformationDTO dto = new AgreementInformationDTO();
        dto.setBrand("BrandB");
        dto.setAdditionalInfo("Test Info");

        String transactionId = "TXN789012";

        // 创建模拟的 PaymentInformation 对象
        PaymentInformation mockPaymentInfo = new PaymentInformation();
        mockPaymentInfo.setBrand("BrandB");
        mockPaymentInfo.setAdditionalInfo("Test Info");
        mockPaymentInfo.setTransactionId(transactionId);

        // 模拟 converter 返回 PaymentInformation 对象
        doReturn(mockPaymentInfo).when(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 模拟 mapper 行为
        doNothing().when(paymentInfoMapper).insertPaymentInformation(any(PaymentInformation.class));

        // 执行测试
        paymentInformationServiceStrategy.saveDetailInformation(dto, transactionId);

        // 验证 converter 被调用
        verify(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 验证 mapper 被调用
        verify(paymentInfoMapper).insertPaymentInformation(paymentInfoCaptor.capture());

        // 验证捕获的 PaymentInformation 对象
        PaymentInformation capturedPaymentInfo = paymentInfoCaptor.getValue();
        assertNotNull(capturedPaymentInfo);
        assertEquals("BrandB", capturedPaymentInfo.getBrand());
        assertEquals("Test Info", capturedPaymentInfo.getAdditionalInfo());
        assertEquals(transactionId, capturedPaymentInfo.getTransactionId());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 transactionId 正确传递
     */
    @Test
    public void testSaveDetailInformation_TransactionIdPassed() {
        // 准备测试数据
        AgreementInformationDTO dto = new AgreementInformationDTO();
        dto.setBrand("BrandC");

        String transactionId = "TXN-CUSTOM-001";

        // 创建模拟的 PaymentInformation 对象
        PaymentInformation mockPaymentInfo = new PaymentInformation();
        mockPaymentInfo.setBrand("BrandC");
        mockPaymentInfo.setTransactionId(transactionId);

        // 模拟 converter 返回 PaymentInformation 对象
        doReturn(mockPaymentInfo).when(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 模拟 mapper 行为
        doNothing().when(paymentInfoMapper).insertPaymentInformation(any(PaymentInformation.class));

        // 执行测试
        paymentInformationServiceStrategy.saveDetailInformation(dto, transactionId);

        // 验证 converter 被调用（transactionId 作为参数传递）
        verify(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 验证 mapper 被调用
        verify(paymentInfoMapper).insertPaymentInformation(paymentInfoCaptor.capture());

        // 验证捕获的 PaymentInformation 对象的 transactionId
        PaymentInformation capturedPaymentInfo = paymentInfoCaptor.getValue();
        assertNotNull(capturedPaymentInfo);
        assertEquals("BrandC", capturedPaymentInfo.getBrand());
        assertEquals(transactionId, capturedPaymentInfo.getTransactionId());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 brand 字段正确传递
     */
    @Test
    public void testSaveDetailInformation_BrandFieldPassed() {
        // 准备测试数据
        AgreementInformationDTO dto = new AgreementInformationDTO();
        dto.setBrand("BrandD");

        String transactionId = "TXN-BRAND-001";

        // 创建模拟的 PaymentInformation 对象
        PaymentInformation mockPaymentInfo = new PaymentInformation();
        mockPaymentInfo.setBrand("BrandD");

        // 模拟 converter 返回 PaymentInformation 对象
        doReturn(mockPaymentInfo).when(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 模拟 mapper 行为
        doNothing().when(paymentInfoMapper).insertPaymentInformation(any(PaymentInformation.class));

        // 执行测试
        paymentInformationServiceStrategy.saveDetailInformation(dto, transactionId);

        // 验证 converter 被调用（brand 作为 dto 参数传递）
        verify(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 验证 mapper 被调用
        verify(paymentInfoMapper).insertPaymentInformation(paymentInfoCaptor.capture());

        // 验证捕获的 PaymentInformation 对象的 brand
        PaymentInformation capturedPaymentInfo = paymentInfoCaptor.getValue();
        assertNotNull(capturedPaymentInfo);
        assertEquals("BrandD", capturedPaymentInfo.getBrand());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 additionalInfo 字段正确传递
     */
    @Test
    public void testSaveDetailInformation_AdditionalInfoFieldPassed() {
        // 准备测试数据
        AgreementInformationDTO dto = new AgreementInformationDTO();
        dto.setBrand("BrandE");
        dto.setAdditionalInfo("Custom Additional Info");

        String transactionId = "TXN-INFO-001";

        // 创建模拟的 PaymentInformation 对象
        PaymentInformation mockPaymentInfo = new PaymentInformation();
        mockPaymentInfo.setBrand("BrandE");
        mockPaymentInfo.setAdditionalInfo("Custom Additional Info");

        // 模拟 converter 返回 PaymentInformation 对象
        doReturn(mockPaymentInfo).when(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 模拟 mapper 行为
        doNothing().when(paymentInfoMapper).insertPaymentInformation(any(PaymentInformation.class));

        // 执行测试
        paymentInformationServiceStrategy.saveDetailInformation(dto, transactionId);

        // 验证 converter 被调用
        verify(agreementInformationConvertor).convertToTransactionPaymentInfo(dto, transactionId);

        // 验证 mapper 被调用
        verify(paymentInfoMapper).insertPaymentInformation(paymentInfoCaptor.capture());

        // 验证捕获的 PaymentInformation 对象的 additionalInfo
        PaymentInformation capturedPaymentInfo = paymentInfoCaptor.getValue();
        assertNotNull(capturedPaymentInfo);
        assertEquals("BrandE", capturedPaymentInfo.getBrand());
        assertEquals("Custom Additional Info", capturedPaymentInfo.getAdditionalInfo());
    }
}

## Service/Strategy 继承父类的示例代码（继承 BaseEnquiryInformationSaveStrategy）

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.mapper.TransactionMapper;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.dao.mapper.AgreementCheckedMapper;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.entity.Transaction;
import com.ocft.iic.uaw.server.modules.transaction.common.transaction.service.ReferenceNumberProvider;
import com.ocft.iic.uaw.server.modules.transaction.core.generalinformation.dao.mapper.DeathClaimEnquiryMapper;
import com.ocft.iic.uaw.server.modules.transaction.core.generalinformation.dao.entity.DeathClaimEnquiry;
import com.ocft.iic.uaw.server.modules.transaction.core.generalinformation.service.converter.DeathClaimEnquiryConverter;
import com.ocft.iic.uaw.server.modules.transaction.core.generalinformation.service.strategy.DeathClaimEnquiryServiceStrategyImpl;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.times;

/**
 * DeathClaimEnquiryServiceStrategyImpl 单元测试
 * 测试 saveDetailInformation 方法是否正确调用 converter 和 mapper
 * 该类继承自 BaseEnquiryInformationSaveStrategy，需要分别处理子类和父类的字段注入
 *
 * @author EX-XUEBO158
 */
@RunWith(MockitoJUnitRunner.class)
public class DeathClaimEnquiryServiceStrategyImplTest {

    @Mock
    private TransactionMapper transactionMapper;

    @Mock
    private AgreementCheckedMapper agreementCheckedMapper;

    @Mock
    private ReferenceNumberProvider referenceNumberProvider;

    @Mock
    private DeathClaimEnquiryMapper deathClaimEnquiryMapper;

    @Mock
    private DeathClaimEnquiryConverter deathClaimEnquiryConverter;

    @Captor
    private ArgumentCaptor<DeathClaimEnquiry> deathClaimEnquiryCaptor;

    private DeathClaimEnquiryServiceStrategyImpl deathClaimEnquiryServiceStrategy;

    @Before
    public void setUp() {
        // 初始化服务实例
        deathClaimEnquiryServiceStrategy = new DeathClaimEnquiryServiceStrategyImpl();
        
        // 注入 mock 的依赖
        // 注意：需要分别处理子类字段和父类字段
        try {
            // 子类字段注入
            Field field = deathClaimEnquiryServiceStrategy.getClass().getDeclaredField("deathClaimEnquiryMapper");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, deathClaimEnquiryMapper);
            
            field = deathClaimEnquiryServiceStrategy.getClass().getDeclaredField("deathClaimEnquiryConverter");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, deathClaimEnquiryConverter);
            
            // 父类字段注入（使用 getSuperclass().getDeclaredField()）
            field = deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("transactionMapper");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, transactionMapper);
            
            field = deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("agreementCheckedMapper");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, agreementCheckedMapper);
            
            field = deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("referenceNumberProvider");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, referenceNumberProvider);
            
            field = deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("enquiryInformationConverter");
            field.setAccessible(true);
            field.set(deathClaimEnquiryServiceStrategy, deathClaimEnquiryConverter);
            
            field = deathClaimEnquiryServiceStrategy.getClass().getSuperclass().getDeclaredField("transaction");
            field.setAccessible(true);
            Transaction mockTransaction = new Transaction();
            mockTransaction.setId("TXN-001");
            mockTransaction.setPolicyNumber("POL-001");
            mockTransaction.setClaimReportDate(new Date());
            field.set(deathClaimEnquiryServiceStrategy, mockTransaction);
        } catch (Exception e) {
            throw new RuntimeException("Failed to inject mocks: " + e.getMessage(), e);
        }
    }

    /**
     * 测试 saveDetailInformation 方法 - 成功场景
     * 验证 converter 被调用且 mapper 接收到正确的 DeathClaimEnquiry 对象
     */
    @Test
    public void testSaveDetailInformation_Success() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("张三");
        deathClaimEnquiry.setDeathDate(new Date());
        deathClaimEnquiry.setDeathPlace("北京");

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-001");
        mockTransaction.setPolicyNumber("POL-001");
        mockTransaction.setClaimReportDate(new Date());
        
        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals("张三", capturedDeathClaimEnquiry.getClaimantName());
        assertEquals("北京", capturedDeathClaimEnquiry.getDeathPlace());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 converter 被调用
     */
    @Test
    public void testSaveDetailInformation_ConverterCalled() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("李四");
        deathClaimEnquiry.setDeathDate(new Date());

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-002");
        mockTransaction.setPolicyNumber("POL-002");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 converter 被调用
        verify(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals("李四", capturedDeathClaimEnquiry.getClaimantName());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 claimantName 字段正确传递
     */
    @Test
    public void testSaveDetailInformation_ClaimantNameFieldPassed() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("王五");
        deathClaimEnquiry.setDeathDate(new Date());

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-003");
        mockTransaction.setPolicyNumber("POL-003");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 converter 被调用
        verify(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象的 claimantName
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals("王五", capturedDeathClaimEnquiry.getClaimantName());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 deathDate 字段正确传递
     */
    @Test
    public void testSaveDetailInformation_DeathDateFieldPassed() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("赵六");
        Date deathDate = new Date();
        deathClaimEnquiry.setDeathDate(deathDate);

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-004");
        mockTransaction.setPolicyNumber("POL-004");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 converter 被调用
        verify(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象的 deathDate
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals(deathDate, capturedDeathClaimEnquiry.getDeathDate());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 deathPlace 字段正确传递
     */
    @Test
    public void testSaveDetailInformation_DeathPlaceFieldPassed() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("孙七");
        deathClaimEnquiry.setDeathDate(new Date());
        deathClaimEnquiry.setDeathPlace("上海");

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-005");
        mockTransaction.setPolicyNumber("POL-005");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 converter 被调用
        verify(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象的 deathPlace
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals("上海", capturedDeathClaimEnquiry.getDeathPlace());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 transactionId 正确传递
     */
    @Test
    public void testSaveDetailInformation_TransactionIdPassed() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry = new DeathClaimEnquiry();
        deathClaimEnquiry.setClaimantName("周八");
        deathClaimEnquiry.setDeathDate(new Date());
        deathClaimEnquiry.setDeathPlace("广州");

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-006");
        mockTransaction.setPolicyNumber("POL-006");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry, mockTransaction);

        // 验证 converter 被调用
        verify(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用
        verify(deathClaimEnquiryMapper).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象
        DeathClaimEnquiry capturedDeathClaimEnquiry = deathClaimEnquiryCaptor.getValue();
        assertNotNull(capturedDeathClaimEnquiry);
        assertEquals("周八", capturedDeathClaimEnquiry.getClaimantName());
    }

    /**
     * 测试 saveDetailInformation 方法 - 验证 multiple deathClaimEnquiries 正确处理
     */
    @Test
    public void testSaveDetailInformation_MultipleDeathClaimEnquiries() {
        // 准备测试数据
        DeathClaimEnquiry deathClaimEnquiry1 = new DeathClaimEnquiry();
        deathClaimEnquiry1.setClaimantName("郑九");
        deathClaimEnquiry1.setDeathDate(new Date());

        DeathClaimEnquiry deathClaimEnquiry2 = new DeathClaimEnquiry();
        deathClaimEnquiry2.setClaimantName("王十");
        deathClaimEnquiry2.setDeathDate(new Date());

        Transaction mockTransaction = new Transaction();
        mockTransaction.setId("TXN-007");
        mockTransaction.setPolicyNumber("POL-007");

        // 模拟 converter 返回 DeathClaimEnquiry 对象
        doReturn(deathClaimEnquiry1).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());
        doReturn(deathClaimEnquiry2).when(deathClaimEnquiryConverter).convertToDeathClaimEnquiry(any(), any());

        // 模拟 mapper 行为
        doNothing().when(deathClaimEnquiryMapper).insertDeathClaimEnquiry(any(DeathClaimEnquiry.class));

        // 执行测试
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry1, mockTransaction);
        deathClaimEnquiryServiceStrategy.saveDetailInformation(deathClaimEnquiry2, mockTransaction);

        // 验证 converter 被调用两次
        verify(deathClaimEnquiryConverter, times(2)).convertToDeathClaimEnquiry(any(), any());

        // 验证 mapper 被调用两次
        verify(deathClaimEnquiryMapper, times(2)).insertDeathClaimEnquiry(deathClaimEnquiryCaptor.capture());

        // 验证捕获的 DeathClaimEnquiry 对象
        List<DeathClaimEnquiry> capturedDeathClaimEnquiries = deathClaimEnquiryCaptor.getAllValues();
        assertEquals(2, capturedDeathClaimEnquiries.size());
        assertEquals("郑九", capturedDeathClaimEnquiries.get(0).getClaimantName());
        assertEquals("王十", capturedDeathClaimEnquiries.get(1).getClaimantName());
    }
}
```