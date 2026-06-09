# 目标
你是一个资深java开发专家，根据背景和要求实现单元测试编写任务

# 背景

## 背景1：单元测试环境信息
* junit版本：junit4
* java版本：java8
* spring版本：springBoot2.6.6
* 使用MockMvc进行springmvc的单元测试开发

## 背景2：测试目的
1、验证Controller的行为，确保API契约正常
2、确保URL、HttpMethod、参数、返回值、异常处理按照预期工作

## 背景3：测试代码编写规范
* 测试方法命名规范：test_原方法名_场景描述，例如：test_getLabelStatus_superAdmin
* 使用Hamcrest进行断言验证
* 直接mock Controller依赖的command或者query,只需要验证一个成功返回的场景
* 遇到command方法返回Void，Mock写法参考：Mockito.doNothing().when(duplicateDefender).check(anyString());
* 确保MockMvcRequestBuilders生成的post路径需要根据Controller类上的@RequestMapping中的路径常量值拼接完整
* 采用MyJsonUtil.toJsonStr(form)来序列化入参作为MockMvcRequestBuilders的content
```
@Mock
private IvrMobileLocateResultQuery mockQuery;

@Test
void test_wrongApproach() {
// 直接mock query的execute方法
Mockito.when(mockQuery.execute(any())).thenReturn(expectedResult);
}
```
* 在`setUp()`方法中使用`ReflectionTestUtils.setField()`建立Controller与Command/Query之间的依赖关系

```
// 正确示例：mock底层依赖
@Mock
private IvrMobileLocateResultQuery query; // 注入真实的query对象

@BeforeEach
public void setUp() {
    MockitoAnnotations.openMocks(this);
    // 通过反射设置真实的依赖关系
    ReflectionTestUtils.setField(controller, "ivrMobileLocateResultQuery", query);
}
```
```
// 使用构造器+set方法来构造入参
SubWorkOrderReassignForm form = new SubWorkOrderReassignForm();
        form.setSubWorkOrderNo(123456L);
        form.setSupplierCode("SUPPLIER123");
        form.setSupplierName("新供应商名称");
        form.setContact("联系人");
        form.setAntiRepeatToken("token123");
        
 // 执行测试
mockMvc.perform(MockMvcRequestBuilders
                .post("/core/dispatch/reassignSubWorkOrderSupplier.do")
                .contentType(MediaType.APPLICATION_JSON_VALUE)
                // 使用MyJsonUtil.toJsonStr(form)来序列化入参
                .content(MyJsonUtil.toJsonStr(form))
        )
```

  
```controller调用query场景的单元测试示例
import com.paic.aoda.icss.gccib.is.sos.base.utils.extend.MyJsonUtil;
import com.paic.aoda.icss.gccib.is.sos.core.feedback.acp.application.model.form.GetAcpTelSurveyDetailListForm;
import com.paic.aoda.icss.gccib.is.sos.core.feedback.acp.application.model.vo.AcpTelSurveyDetailVO;
import com.paic.aoda.icss.gccib.is.sos.core.feedback.acp.application.query.GetAcpTelSurveyDetailListQuery;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import java.util.Collections;
import java.util.List;
import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;

/**
 * GetAcpTelSurveyDetailListController单元测试类
 *
 * @author AI Assistant
 * @since 2025-11-23
 */
@DisplayName("获取ACP电话回访问卷详情列表接口测试")
public class GetAcpTelSurveyDetailListControllerTest {

    private MockMvc mockMvc;

    @InjectMocks
    private GetAcpTelSurveyDetailListController controller;

    @Mock
    private GetAcpTelSurveyDetailListQuery query;

    @BeforeEach
    public void setUp() {
        // 严格按照规范顺序初始化测试环境
        MockitoAnnotations.openMocks(this);
        ReflectionTestUtils.setField(controller, "query", query);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @DisplayName("场景1_正常获取ACP电话回访问卷详情列表时，返回成功响应")
    @Test
    void test_getAcpTelSurveyDetailList_normalCase() throws Exception {
        // 准备期望的返回结果
        List<AcpTelSurveyDetailVO> expectedList = Collections.emptyList();

        // Mock query的execute方法
        Mockito.when(query.execute(any(GetAcpTelSurveyDetailListForm.class)))
                .thenReturn(expectedList);

        // 构造入参
        GetAcpTelSurveyDetailListForm form = new GetAcpTelSurveyDetailListForm();
        form.setSurveyId("SURVEY123456");
        form.setSurveyType("1");

        // 执行测试
        mockMvc.perform(MockMvcRequestBuilders
                         // 严格按照Controller类上的@RequestMapping路径常量实际值进行地址拼接
                        .post(CoreApiPath.FEEDBACK+"/getAcpTelSurveyDetailList.do")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(MyJsonUtil.toJsonStr(form))
                )
                .andExpect(MockMvcResultMatchers.status().is(HttpStatus.OK.value()))
                .andDo(print())
                .andExpect(MockMvcResultMatchers.jsonPath("$.code", Matchers.is("10000")))
                .andExpect(MockMvcResultMatchers.jsonPath("$.body", Matchers.hasSize(0)));

        // 验证query方法被调用一次
        Mockito.verify(query, Mockito.times(1)).execute(any(GetAcpTelSurveyDetailListForm.class));
    }
}
```

```controller调用command的场景单元测试示例
import com.paic.aoda.icss.gccib.is.sos.base.utils.extend.MyJsonUtil;
import com.paic.aoda.icss.gccib.is.sos.core.feedback.acp.application.command.AcpTelSurveyCommand;
import com.paic.aoda.icss.gccib.is.sos.core.feedback.acp.application.model.form.AcpTelSurveyForm;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;

/**
 * AcpTelSurveyController单元测试类
 *
 * @author AI Assistant
 * @since 2025-11-23
 */
@DisplayName("电话回访接口测试")
public class AcpTelSurveyControllerTest {

    private MockMvc mockMvc;

    @InjectMocks
    private AcpTelSurveyController controller;

    @Mock
    private AcpTelSurveyCommand command;

    @BeforeEach
    public void setUp() {
        // 严格按照规范顺序初始化测试环境
        MockitoAnnotations.openMocks(this);
        ReflectionTestUtils.setField(controller, "command", command);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @DisplayName("场景1_正常执行电话回访时，返回成功响应")
    @Test
    void test_acpTelSurvey_normalCase() throws Exception {
        // 准备期望的返回结果
        String expectedResult = "success";

        // Mock command的execute方法
        Mockito.when(command.execute(any(AcpTelSurveyForm.class)))
                .thenReturn(expectedResult);

        // 构造入参
        AcpTelSurveyForm form = new AcpTelSurveyForm();
        form.setCaseNo(123456789L);
        form.setHandlingLevel("JUNIOR");
        form.setTelNo("13800138000");
        form.setUserTsr("1234");
        form.setUserId("AGENT001");
        form.setUserUm("UM001");
        form.setConnId("CALL123456");
        form.setRecordNo("RECORD123456");


        // 执行测试
        mockMvc.perform(MockMvcRequestBuilders
                        // 严格按照Controller类上的@RequestMapping路径常量实际值进行地址拼接
                        .post(CoreApiPath.FEEDBACK+"/acpTelSurvey.do")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(MyJsonUtil.toJsonStr(form))
                )
                .andExpect(MockMvcResultMatchers.status().is(HttpStatus.OK.value()))
                .andDo(print())
                .andExpect(MockMvcResultMatchers.jsonPath("$.code", Matchers.is("10000")))
                .andExpect(MockMvcResultMatchers.jsonPath("$.body", Matchers.is("success")));

        // 验证command方法被调用一次
        Mockito.verify(command, Mockito.times(1)).execute(any(AcpTelSurveyForm.class));
    }
}
```
* 分页查询的入参组装使用form.setPage(1); form.setPageSize(10);
```controller分页查询单元测试示例
import com.paic.aoda.base.dto.PageVO;
import com.paic.aoda.icss.gccib.is.sos.base.constants.contextpath.CoreApiPath;
import com.paic.aoda.icss.gccib.is.sos.core.workorder.registration.application.model.form.PageHistoryWorkOrderForm;
import com.paic.aoda.icss.gccib.is.sos.core.workorder.registration.application.model.form.PageWorkOrderListForm;
import com.paic.aoda.icss.gccib.is.sos.core.workorder.registration.application.model.vo.PageWorkOrderListVO;
import com.paic.aoda.icss.gccib.is.sos.core.workorder.registration.application.query.PageHistoryWorkOrderQuery;
import com.paic.aoda.icss.gccib.is.sos.core.workorder.registration.application.query.PageWorkOrderQuery;
import com.paic.aoda.icss.gccib.is.sos.base.utils.extend.MyJsonUtil;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static org.mockito.ArgumentMatchers.any;

/**
 * PageWorkOrderListController单元测试类
 *
 * @author AI Assistant
 * @since 2025-11-24
 */
@DisplayName("分页查询工单信息接口测试")
public class PageWorkOrderListControllerTest {

    private MockMvc mockMvc;

    @InjectMocks
    private PageWorkOrderListController controller;

    @Mock
    private PageWorkOrderQuery pageWorkOrderQuery;

    @Mock
    private PageHistoryWorkOrderQuery pageHistoryWorkOrderQuery;

    @BeforeEach
    public void setUp() {
        // 严格按照规范顺序初始化测试环境
        MockitoAnnotations.openMocks(this);
        ReflectionTestUtils.setField(controller, "pageWorkOrderQuery", pageWorkOrderQuery);
        ReflectionTestUtils.setField(controller, "pageHistoryWorkOrderQuery", pageHistoryWorkOrderQuery);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @DisplayName("场景1_正常分页查询工单信息时，返回成功响应")
    @Test
    void test_pageWorkOrderList_normalCase() throws Exception {
        // 准备期望的返回结果
        PageVO<PageWorkOrderListVO> expectedPage = new PageVO<>();

        // Mock query的execute方法
        Mockito.when(pageWorkOrderQuery.execute(any(PageWorkOrderListForm.class)))
                .thenReturn(expectedPage);

        // 构造入参
        PageWorkOrderListForm form = new PageWorkOrderListForm();
        form.setPage(1);
        form.setPageSize(10);

        // 执行测试
        mockMvc.perform(MockMvcRequestBuilders
                        // 严格按照Controller类上的@RequestMapping路径常量实际值进行地址拼接
                        .post(CoreApiPath.WORK_ORDER + "/pageWorkOrder.do")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(MyJsonUtil.toJsonStr(form))
                )
                .andExpect(MockMvcResultMatchers.status().is(HttpStatus.OK.value()))
                .andExpect(MockMvcResultMatchers.jsonPath("$.code", Matchers.is("10000")))
                .andExpect(MockMvcResultMatchers.jsonPath("$.body", Matchers.notNullValue()));

        // 验证query方法被调用一次
        Mockito.verify(pageWorkOrderQuery, Mockito.times(1)).execute(any(PageWorkOrderListForm.class));
    }

    @DisplayName("场景2_正常分页查询历史父工单时，返回成功响应")
    @Test
    void test_pageHistoryWorkOrder_normalCase() throws Exception {
        // 准备期望的返回结果
        PageVO<PageWorkOrderListVO> expectedPage = new PageVO<>();

        // Mock query的execute方法
        Mockito.when(pageHistoryWorkOrderQuery.execute(any(PageHistoryWorkOrderForm.class)))
                .thenReturn(expectedPage);

        // 构造入参
        PageHistoryWorkOrderForm form = new PageHistoryWorkOrderForm();
        form.setPage(1);
        form.setPageSize(10);

        // 执行测试
        mockMvc.perform(MockMvcRequestBuilders
                        // 严格按照Controller类上的@RequestMapping路径常量实际值进行地址拼接
                        .post(CoreApiPath.WORK_ORDER + "/pageHistoryWorkOrder.do")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(MyJsonUtil.toJsonStr(form))
                )
                .andExpect(MockMvcResultMatchers.status().is(HttpStatus.OK.value()))
                .andExpect(MockMvcResultMatchers.jsonPath("$.code", Matchers.is("10000")))
                .andExpect(MockMvcResultMatchers.jsonPath("$.body", Matchers.notNullValue()));

        // 验证query方法被调用一次
        Mockito.verify(pageHistoryWorkOrderQuery, Mockito.times(1)).execute(any(PageHistoryWorkOrderForm.class));
    }
}
```

# 背景4：非REST接口单元测试特殊说明

对于非REST接口（如文件下载、文件上传、WebSocket等），需要特殊处理：

### 文件下载接口测试规范
1. 由于这类接口通常不返回JSON响应，而是直接操作HttpServletResponse写入数据，因此不能使用MockMvc进行测试
2. 应该使用传统的Mockito方式，mock HttpServletRequest和HttpServletResponse对象
3. 需要模拟HttpServletResponse的各种方法返回值，如getWriter()、getOutputStream()等
4. 测试时应验证核心业务逻辑是否正确执行，如Command的execute方法是否被调用

### 示例代码
```java
// 测试文件下载接口
@Test
@SneakyThrows
void downloadTemplateTest() {
    // 准备测试数据
    DownloadTemplateForm form = DownloadTemplateForm.builder()
            .templateCode("TEST_TEMPLATE")
            .build();
    
    // 创建模拟的HttpServletRequest和HttpServletResponse
    HttpServletRequest request = mock(HttpServletRequest.class);
    HttpServletResponse response = mock(HttpServletResponse.class);
    
    // 模拟response.getWriter()返回值
    PrintWriter writer = mock(PrintWriter.class);
    when(response.getWriter()).thenReturn(writer);
    
    // 模拟response.getOutputStream()返回值
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    when(response.getOutputStream()).thenReturn(new ServletOutputStream() {
        @Override
        public boolean isReady() {
            return true;
        }
        
        @Override
        public void setWriteListener(WriteListener writeListener) {
            // 不需要实现
        }
        
        @Override
        public void write(int b) throws IOException {
            outputStream.write(b);
        }
    });
    
    // 调用被测试方法
    controller.downloadTemplate(request, response, form);
    
    // 验证downloadTemplateCommand的execute方法被调用
    Mockito.verify(downloadTemplateCommand, Mockito.times(1)).execute(any());
}
```

## 要求
1、先搜索目标Controller是否已经单元测试，如果已经存在单元测试类，则不需要生成单元测试
2、按照背景生成准确Controller单元测试代码
3、根据Controller类上的@RequestMapping注解的路径常量值反思检查生成的单元测试代码中MockMvcRequestBuilders生成的接口路径地址是否正确
4、根据Controller入参的Form的构造，反思生成单元测试代码中的，form参数准备的set字段设置是否有遗漏，字段类型是否正确，测试值参考form对象的@Schema示例
5、反思生成的单元测试代码中的import依赖包，判断是否有没有使用的无用import需要删除，比如：import com.paic.aoda.base.dto.Response;