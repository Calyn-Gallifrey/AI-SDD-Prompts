package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.handler.ApiExceptionHandler;
import com.example.uawsdddemo.model.dto.CreatePolicyInfoChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyInfoChangeWorkOrderResponse;
import com.example.uawsdddemo.model.enums.ChangeFieldType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;
import com.example.uawsdddemo.service.PolicyInfoChangeWorkOrderService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.time.Instant;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(MockitoJUnitRunner.class)
public class PolicyInfoChangeWorkOrderControllerTest {

    private final ObjectMapper objectMapper = new ObjectMapper();

    private MockMvc mockMvc;

    @Mock
    private PolicyInfoChangeWorkOrderService service;

    @InjectMocks
    private PolicyInfoChangeWorkOrderController controller;

    @Before
    public void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setControllerAdvice(new ApiExceptionHandler())
                .build();
    }

    @Test
    public void testCreate_success_expectCreatedResponse() throws Exception {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        Mockito.when(service.create(any(CreatePolicyInfoChangeWorkOrderRequest.class))).thenReturn(buildResponse(false));

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-info-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.workOrderId", Matchers.is("WO-10001")))
                .andExpect(jsonPath("$.policyNo", Matchers.is("P-10001")))
                .andExpect(jsonPath("$.status", Matchers.is("SUBMITTED")))
                .andExpect(jsonPath("$.changeSummary").doesNotExist());

        Mockito.verify(service, times(1)).create(any(CreatePolicyInfoChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreate_validationFailed_expectBadRequest() throws Exception {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        request.setPolicyNo("");

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-info-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0)).create(any(CreatePolicyInfoChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreate_businessValidationFailed_expectBadRequest() throws Exception {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        Mockito.when(service.create(any(CreatePolicyInfoChangeWorkOrderRequest.class)))
                .thenThrow(new BadRequestException("newValue must be different from oldValue"));

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-info-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("newValue must be different from oldValue")));

        Mockito.verify(service, times(1)).create(any(CreatePolicyInfoChangeWorkOrderRequest.class));
    }

    @Test
    public void testGet_success_expectOkResponse() throws Exception {
        Mockito.when(service.get("WO-10001")).thenReturn(buildResponse(true));

        mockMvc.perform(MockMvcRequestBuilders.get("/api/work-orders/policy-info-change/WO-10001"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.workOrderId", Matchers.is("WO-10001")))
                .andExpect(jsonPath("$.policyNo", Matchers.is("P-10001")))
                .andExpect(jsonPath("$.changeSummary", Matchers.is("HOLDER_PHONE: 13800000000 -> 13900000000")));

        Mockito.verify(service, times(1)).get("WO-10001");
    }

    private CreatePolicyInfoChangeWorkOrderRequest buildRequest() {
        CreatePolicyInfoChangeWorkOrderRequest request = new CreatePolicyInfoChangeWorkOrderRequest();
        request.setPolicyNo("P-10001");
        request.setChangeFieldType(ChangeFieldType.HOLDER_PHONE);
        request.setOldValue("13800000000");
        request.setNewValue("13900000000");
        request.setRequester("alice");
        return request;
    }

    private PolicyInfoChangeWorkOrderResponse buildResponse(boolean includeChangeSummary) {
        PolicyInfoChangeWorkOrderResponse response = new PolicyInfoChangeWorkOrderResponse();
        response.setWorkOrderId("WO-10001");
        response.setPolicyNo("P-10001");
        response.setChangeFieldType(ChangeFieldType.HOLDER_PHONE);
        response.setOldValue("13800000000");
        response.setNewValue("13900000000");
        response.setRequester("alice");
        response.setStatus(WorkOrderStatus.SUBMITTED);
        response.setCreatedAt(Instant.parse("2026-05-28T08:00:00Z"));
        if (includeChangeSummary) {
            response.setChangeSummary("HOLDER_PHONE: 13800000000 -> 13900000000");
        }
        return response;
    }
}
