# 目标
本规则用于根据背景内容和参考示例创建单元测试类，并放到指定位置。

## 示例边界

本文件中的代码片段、类名、包名、字段名、测试方法名和业务数据仅用于说明 Service 单元测试结构和写法，不是当前任务的默认测试目标。生成测试时，必须基于当前 Brief Design、当前代码和已确认测试目标替换所有示例业务信息。

# 背景

## 背景1  单测框架
1、根据用户输入的类 或者 选中的代码，生成单元测试
2、单元测试框架使用junit 4和 Mockito框架
3、用单元测试对原代码进行单元测试覆盖
4、对于service类的公共方法进行单元测试
5、设计覆盖较全的场景案例，及对应的输入数据和返回值，以及对边界值的考虑等各种场景的测试案例
6、 使用断言,校验预期行为,预期返回值等
7、 只针对目标类本身进行测试，不对引用类生成单元测试
8、 import 时不得使用 import * 的方式导入引用文件
9、 不用创建model实体类对象，引用已有的实体类对象

## 背景2 Service类Mock规则
对于Service类的单元测试，使用@Autowired注解注入依赖，在单元测试中使用@InjectMocks和@Mock注解，参考如下示例：
```Service类Mock示例
@RunWith(MockitoJUnitRunner.class)
public class GeneralInformationServiceImplTest {

    @Mock
    private RepeatSubmitChecker repeatSubmitChecker;

    @Mock
    private com.ocft.iic.uaw.server.modules.transaction.common.transaction.service.BaseEnquiryInformationSaveStrategy<GeneralInformationDTO> saveStrategy;

    @InjectMocks
    private GeneralInformationServiceImpl generalInformationService;

    private GeneralInformationBO generalInformationBO;

    /**
     * 初始化测试数据和策略Map
     */
    @Before
    public void setUp() {
        // 初始化测试数据
        generalInformationBO = new GeneralInformationBO();
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setContactId("CONTACT_001");
        generalInformationBO.setReferenceNumber("REF_001");
        generalInformationBO.setInteractionId("INTERACTION_001");
        generalInformationBO.setAgentId("AGENT_001");
        generalInformationBO.setCustomerId("CUSTOMER_001");
        generalInformationBO.setTransactionType("deathClaimEnquiry");
        generalInformationBO.setParentTransactionId("PARENT_TXN_001");
        generalInformationBO.setOperateFlag("submit");
        generalInformationBO.setBrand("Greenlight");
        generalInformationBO.setUrl("https://www.oldmutual.co.za/about");

        AgreementBO agreement = new AgreementBO();
        agreement.setBrand("Greenlight");
        agreement.setPolicyNumber("POLICY_001");
        agreement.setProductCode("PRODUCT_001");
        agreement.setAgreementName("Agreement Name");
        agreement.setCoverAmount("100000");
        agreement.setStatus("active");

        List<AgreementBO> agreements = new ArrayList<>();
        agreements.add(agreement);
        generalInformationBO.setAgreements(agreements);

        // 使用反射为 generalInformationConverter 设值
        try {
            java.lang.reflect.Field field = generalInformationService.getClass().getDeclaredField("generalInformationConverter");
            field.setAccessible(true);
            field.set(generalInformationService, MyDocumentConverter.INSTANCE);
        } catch (Exception e) {
            fail("Failed to inject generalInformationConverter: " + e.getMessage());
        }

        // 初始化策略Map
        try {
            java.lang.reflect.Field field = generalInformationService.getClass().getDeclaredField("strategyMap");
            field.setAccessible(true);
            Map<String, com.ocft.iic.uaw.server.modules.transaction.common.transaction.service.BaseEnquiryInformationSaveStrategy<GeneralInformationDTO>> strategyMap = new HashMap<>();
            strategyMap.put("deathClaimEnquiry", saveStrategy);
            strategyMap.put("errorsAndIssues", saveStrategy);
            strategyMap.put("omEnquiry", saveStrategy);
            strategyMap.put("overpaymentRecoveryMissedPremiums", saveStrategy);
            strategyMap.put("cancelGeneral", saveStrategy);
            field.set(generalInformationService, strategyMap);
        } catch (Exception e) {
            fail("Failed to inject strategyMap: " + e.getMessage());
        }
    }

}

    /**
     * 测试 submitOrCancel 方法 - 成功场景（提交）
     */
    @Test
    public void testSubmitOrCancel_Success_Submit() {
        // 准备测试数据
        String requestToken = "REQUEST_TOKEN_001";
        generalInformationBO.setRequestToken(requestToken);

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setContactId("CONTACT_001");
        dto.setReferenceNumber("REF_001");
        dto.setInteractionId("INTERACTION_001");
        dto.setAgentId("AGENT_001");
        dto.setCustomerId("CUSTOMER_001");
        dto.setTransactionType("deathClaimEnquiry");
        dto.setParentTransactionId("PARENT_TXN_001");
        dto.setOperateFlag("submit");
        dto.setBrand("Greenlight");
        dto.setUrl("https://www.oldmutual.co.za/about");

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - 成功场景（取消）
     */
    @Test
    public void testSubmitOrCancel_Success_Cancel() {
        // 准备测试数据 - 取消场景
        generalInformationBO.setRequestToken("REQUEST_TOKEN_002");
        generalInformationBO.setOperateFlag("cancel");
        generalInformationBO.setCancelReason("Customer decided not to continue");
        generalInformationBO.setCancelObservations("Observations for cancellation");

        String requestToken = "REQUEST_TOKEN_002";

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setOperateFlag("cancel");
        dto.setCancelReason("Customer decided not to continue");
        dto.setCancelObservations("Observations for cancellation");

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - 重复提交异常
     */
    @Test(expected = IICRuntimeException.class)
    public void testSubmitOrCancel_DuplicateSubmit() {
        // 准备测试数据
        String requestToken = "REQUEST_TOKEN_001";
        generalInformationBO.setRequestToken(requestToken);

        // 模拟重复提交检查抛出异常
        doThrow(new com.ocft.uaw.comm.api.exception.IICRuntimeException("请勿重复提交，请稍后再试"))
                .when(repeatSubmitChecker).check(requestToken);

        // 执行测试
        generalInformationService.submitOrCancel(generalInformationBO);
        fail("Expected IICRuntimeException to be thrown");
    }

    /**
     * 测试 submitOrCancel 方法 - 策略执行失败
     */
    @Test(expected = IICRuntimeException.class)
    public void testSubmitOrCancel_StrategyExecutionFailed() {
        // 准备测试数据
        String requestToken = "REQUEST_TOKEN_001";
        generalInformationBO.setRequestToken(requestToken);

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行失败
        when(saveStrategy.execute(anyList())).thenReturn(false);

        // 执行测试
        generalInformationService.submitOrCancel(generalInformationBO);
        fail("Expected com.ocft.uaw.comm.api.exception.IICRuntimeException to be thrown");
    }

    /**
     * 测试 submitOrCancel 方法 - 不支持的交易类型
     */
    @Test(expected = IICRuntimeException.class)
    public void testSubmitOrCancel_UnsupportedTransactionType() {
        // 准备测试数据 - 不支持的交易类型
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setTransactionType("UNSUPPORTED_TYPE");

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setTransactionType("UNSUPPORTED_TYPE");

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check("REQUEST_TOKEN_001");

        // 执行测试
        generalInformationService.submitOrCancel(generalInformationBO);
        fail("Expected IICRuntimeException to be thrown");
    }

    /**
     * 测试 submitOrCancel 方法 - 空协议列表
     */
    @Test
    public void testSubmitOrCancel_EmptyAgreements() {
        // 准备测试数据 - 空协议列表
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setAgreements(new ArrayList<>());

        String requestToken = "REQUEST_TOKEN_001";

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setAgreements(new ArrayList<>());

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - null 协议列表
     */
    @Test
    public void testSubmitOrCancel_NullAgreements() {
        // 准备测试数据 - null 协议列表
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setAgreements(null);

        String requestToken = "REQUEST_TOKEN_001";

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setAgreements(null);

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - 多个协议
     */
    @Test
    public void testSubmitOrCancel_MultipleAgreements() {
        // 准备测试数据 - 多个协议
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");

        AgreementBO agreement1 = new AgreementBO();
        agreement1.setBrand("Greenlight");
        agreement1.setPolicyNumber("POLICY_001");

        AgreementBO agreement2 = new AgreementBO();
        agreement2.setBrand("Brand2");
        agreement2.setPolicyNumber("POLICY_002");

        List<AgreementBO> agreements = new ArrayList<>();
        agreements.add(agreement1);
        agreements.add(agreement2);
        generalInformationBO.setAgreements(agreements);

        String requestToken = "REQUEST_TOKEN_001";

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - null operateFlag
     */
    @Test
    public void testSubmitOrCancel_NullOperateFlag() {
        // 准备测试数据 - null operateFlag
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setOperateFlag(null);

        String requestToken = "REQUEST_TOKEN_001";

        // 构建DTO对象
        GeneralInformationDTO dto = new GeneralInformationDTO();
        dto.setOperateFlag(null);

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - deathClaimEnquiry 类型
     */
    @Test
    public void testSubmitOrCancel_DeathClaimEnquiry() {
        // 准备测试数据 - deathClaimEnquiry 类型
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setTransactionType("deathClaimEnquiry");

        String requestToken = "REQUEST_TOKEN_001";

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - errorsAndIssues 类型
     */
    @Test
    public void testSubmitOrCancel_ErrorsAndIssues() {
        // 准备测试数据 - errorsAndIssues 类型
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setTransactionType("errorsAndIssues");

        String requestToken = "REQUEST_TOKEN_001";

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - omEnquiry 类型
     */
    @Test
    public void testSubmitOrCancel_OmEnquiry() {
        // 准备测试数据 - omEnquiry 类型
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setTransactionType("omEnquiry");

        String requestToken = "REQUEST_TOKEN_001";

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }

    /**
     * 测试 submitOrCancel 方法 - overpaymentRecoveryMissedPremiums 类型
     */
    @Test
    public void testSubmitOrCancel_OverpaymentRecoveryMissedPremiums() {
        // 准备测试数据 - overpaymentRecoveryMissedPremiums 类型
        generalInformationBO.setRequestToken("REQUEST_TOKEN_001");
        generalInformationBO.setTransactionType("overpaymentRecoveryMissedPremiums");

        String requestToken = "REQUEST_TOKEN_001";

        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = generalInformationService.submitOrCancel(generalInformationBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }
}
```

## 背景3：特殊Mock处理
1、对于 converter 类型的字段，不得使用 mock，需要使用真实的实现类
2、对于strategyMap等复杂字段，可以使用反射注入
3、参考如下示例
```特殊Mock处理示例
// 使用反射为 generalInformationConverter 设值
try {
    java.lang.reflect.Field field = generalInformationService.getClass().getDeclaredField("generalInformationConverter");
    field.setAccessible(true);
    field.set(generalInformationService, new GeneralInformationConverterImpl());
} catch (Exception e) {
    fail("Failed to inject generalInformationConverter: " + e.getMessage());
}

// 初始化策略Map
try {
    java.lang.reflect.Field field = generalInformationService.getClass().getDeclaredField("strategyMap");
    field.setAccessible(true);
    Map<String, com.ocft.iic.uaw.server.modules.transaction.common.transaction.service.BaseEnquiryInformationSaveStrategy<GeneralInformationDTO>> strategyMap = new HashMap<>();
    strategyMap.put("deathClaimEnquiry", saveStrategy);
    strategyMap.put("errorsAndIssues", saveStrategy);
    strategyMap.put("omEnquiry", saveStrategy);
    strategyMap.put("overpaymentRecoveryMissedPremiums", saveStrategy);
    strategyMap.put("cancelGeneral", saveStrategy);
    field.set(generalInformationService, strategyMap);
} catch (Exception e) {
    fail("Failed to inject strategyMap: " + e.getMessage());
}
```

## 背景4：Converter为单例模式的处理
当converter字段使用 `@Autowired` 注解注入，且其实现类为单例模式（如 `Mappers.getMapper(Converter.class)`）时，在单元测试中：
1. **converter 无需 mock**
2. 使用反射注入 converter 的 `INSTANCE` 单例
3. converter 方法无需 mock

**参考示例：**
```java
@RunWith(MockitoJUnitRunner.class)
public class MyDocumentServiceImplTest {

    @Mock
    private RepeatSubmitChecker repeatSubmitChecker;

    @Mock
    private BaseEnquiryInformationSaveStrategy<MyDocumentInformationDTO> saveStrategy;

    @InjectMocks
    private MyDocumentServiceImpl myDocumentService;

    @Before
    public void setUp() {
        // 使用反射为 myDocumentConverter 设值（单例模式）
        try {
            java.lang.reflect.Field field = myDocumentService.getClass().getDeclaredField("myDocumentConverter");
            field.setAccessible(true);
            field.set(myDocumentService, MyDocumentConverter.INSTANCE);
        } catch (Exception e) {
            fail("Failed to inject myDocumentConverter: " + e.getMessage());
        }

        // 初始化策略Map
        try {
            java.lang.reflect.Field field = myDocumentService.getClass().getDeclaredField("strategyMap");
            field.setAccessible(true);
            Map<String, BaseEnquiryInformationSaveStrategy<MyDocumentInformationDTO>> strategyMap = new HashMap<>();
            strategyMap.put("myDocument", saveStrategy);
            strategyMap.put("cancelDocument", saveStrategy);
            field.set(myDocumentService, strategyMap);
        } catch (Exception e) {
            fail("Failed to inject strategyMap: " + e.getMessage());
        }
    }

    @Test
    public void testSubmitOrCancel_Success_Submit() {
        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = myDocumentService.submitOrCancel(myDocumentBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }
}
```

## 背景5：静态方法的处理
对于静态方法（如 MyDocumentHelper.buildDocumentInformationDTO()），**不得使用 Mockito 进行 mock**。需要直接调用真实方法或重构代码为实例方法。

**错误示例（不适用写法）：**
```java
// 这是错误的！静态方法无法被 mock
Mockito.mockStatic(MyDocumentHelper.class);
when(MyDocumentHelper.buildDocumentInformationDTO(any())).thenReturn(dto);
```

**正确做法：**
```java
// 直接调用静态方法
MyDocumentInformationDTO dto = MyDocumentHelper.buildDocumentInformationDTO(myDocumentBO);
```

**完整示例：**
```java
@RunWith(MockitoJUnitRunner.class)
public class MyDocumentServiceImplTest {

    @Mock
    private RepeatSubmitChecker repeatSubmitChecker;

    @Mock
    private BaseEnquiryInformationSaveStrategy<MyDocumentInformationDTO> saveStrategy;

    @InjectMocks
    private MyDocumentServiceImpl myDocumentService;

    @Before
    public void setUp() {
        // 使用反射为 myDocumentConverter 设值（单例模式）
        try {
            java.lang.reflect.Field field = myDocumentService.getClass().getDeclaredField("myDocumentConverter");
            field.setAccessible(true);
            field.set(myDocumentService, MyDocumentConverter.INSTANCE);
        } catch (Exception e) {
            fail("Failed to inject myDocumentConverter: " + e.getMessage());
        }

        // 初始化策略Map
        try {
            java.lang.reflect.Field field = myDocumentService.getClass().getDeclaredField("strategyMap");
            field.setAccessible(true);
            Map<String, BaseEnquiryInformationSaveStrategy<MyDocumentInformationDTO>> strategyMap = new HashMap<>();
            strategyMap.put("myDocument", saveStrategy);
            strategyMap.put("cancelDocument", saveStrategy);
            field.set(myDocumentService, strategyMap);
        } catch (Exception e) {
            fail("Failed to inject strategyMap: " + e.getMessage());
        }
    }

    @Test
    public void testSubmitOrCancel_Success_Submit() {
        // 模拟重复提交检查通过
        doNothing().when(repeatSubmitChecker).check(requestToken);

        // 模拟策略执行成功
        when(saveStrategy.execute(anyList())).thenReturn(true);

        // 执行测试
        InformationResVO result = myDocumentService.submitOrCancel(myDocumentBO);

        // 验证结果
        assertNotNull(result);
        assertEquals(IICResEnum.SUCCESS.getMsg(), result.getResult());

        // 验证方法调用
        verify(repeatSubmitChecker, times(1)).check(requestToken);
    }
}
```

# 要求
1、根据用户输入的类 或者 选中的代码，生成单元测试
2、用单元测试对原代码进行单元测试覆盖
3、对于service类的公共方法进行单元测试
4、import 时不得使用 import * 的方式导入引用文件
5、converter 无需 mock，例如：private final MeetingContactInfoConverter converter = Mappers.getMapper(MeetingContactInfoConverter.class);
6、service功能代码变更频繁，单元测试代码需要Mockito.verify断言，验证方法调用次数
7、不得 mock 项目的工具类，例如：MyStringUtil、MyJsonUtil、MyListUtil、MyDateUtil、MyCollectionUtil
8、对于strategyMap等复杂字段，可以使用反射注入
9、对于静态方法（如 MyDocumentHelper.buildDocumentInformationDTO()），不得使用 Mockito 进行 mock
10、当使用 INSTANCE 单例模式的 converter 时，无需 mock，但需要 import 对应的类
11、如果出现 "UnnecessaryStubbingException" 错误，检查是否对无需 mock 的对象进行了 mock，或是否正确使用了反射注入
12、import 语句需要完整，包括所有使用的类和静态方法（如 when、doNothing、doThrow、verify、times、anyList 等）
```
