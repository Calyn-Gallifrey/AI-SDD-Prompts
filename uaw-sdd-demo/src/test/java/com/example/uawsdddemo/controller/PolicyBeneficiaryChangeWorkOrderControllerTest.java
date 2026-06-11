package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.handler.ApiExceptionHandler;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryEmailChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyBeneficiaryChangeWorkOrderResponse;
import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;
import com.example.uawsdddemo.service.PolicyBeneficiaryChangeWorkOrderService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.time.Instant;

import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(MockitoJUnitRunner.class)
public class PolicyBeneficiaryChangeWorkOrderControllerTest {

    private final ObjectMapper objectMapper = new ObjectMapper();

    private MockMvc mockMvc;

    @Mock
    private PolicyBeneficiaryChangeWorkOrderService service;

    @InjectMocks
    private PolicyBeneficiaryChangeWorkOrderController controller;

    @Before
    public void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setControllerAdvice(new ApiExceptionHandler())
                .build();
    }

    @Test
    public void testCreate_success_expectCreatedResponse() throws Exception {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        Mockito.when(service.create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class)))
                .thenReturn(buildResponse());

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.workOrderId", Matchers.is("WO-BEN-10001")))
                .andExpect(jsonPath("$.policyNo", Matchers.is("P-20001")))
                .andExpect(jsonPath("$.beneficiaryIdNoMasked", Matchers.is("****7890")))
                .andExpect(jsonPath("$.beneficiaryIdNo").doesNotExist())
                .andExpect(jsonPath("$.status", Matchers.is("SUBMITTED")));

        Mockito.verify(service, times(1)).create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreate_validationFailed_expectBadRequest() throws Exception {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        request.setBeneficiaryName("");

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0)).create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreate_invalidBenefitRatio_expectBadRequest() throws Exception {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        request.setBenefitRatio(101);

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0)).create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreate_businessValidationFailed_expectBadRequest() throws Exception {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        Mockito.when(service.create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class)))
                .thenThrow(new BadRequestException(
                        "submitted duplicate policy beneficiary change work order exists"));

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message",
                        Matchers.is("submitted duplicate policy beneficiary change work order exists")));

        Mockito.verify(service, times(1)).create(any(CreatePolicyBeneficiaryChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreateEmailChange_success_expectCreatedResponse() throws Exception {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        Mockito.when(service.createEmailChange(any(CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.class)))
                .thenReturn(buildEmailResponse());

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change/email")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.workOrderId", Matchers.is("WO-BEN-EMAIL-10001")))
                .andExpect(jsonPath("$.policyNo", Matchers.is("P-20001")))
                .andExpect(jsonPath("$.beneficiaryIdNoMasked", Matchers.is("****7890")))
                .andExpect(jsonPath("$.beneficiaryEmail", Matchers.is("bob@example.com")))
                .andExpect(jsonPath("$.beneficiaryIdNo").doesNotExist())
                .andExpect(jsonPath("$.status", Matchers.is("SUBMITTED")));

        Mockito.verify(service, times(1))
                .createEmailChange(any(CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.class));
    }

    @Test
    public void testCreateEmailChange_trimmedEmail_expectCreatedResponse() throws Exception {
        String requestBody = "{"
                + "\"policyNo\":\"P-20001\","
                + "\"beneficiaryName\":\"Bob\","
                + "\"beneficiaryIdNo\":\"1234567890\","
                + "\"beneficiaryEmail\":\"  Bob.Email@Example.COM  \","
                + "\"requester\":\"alice\""
                + "}";
        Mockito.when(service.createEmailChange(any(CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.class)))
                .thenReturn(buildEmailResponse());

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change/email")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody))
                .andExpect(status().isCreated());

        ArgumentCaptor<CreatePolicyBeneficiaryEmailChangeWorkOrderRequest> captor =
                ArgumentCaptor.forClass(CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.class);
        Mockito.verify(service, times(1)).createEmailChange(captor.capture());
        assertEquals("Bob.Email@Example.COM", captor.getValue().getBeneficiaryEmail());
    }

    @Test
    public void testCreateEmailChange_invalidEmail_expectBadRequest() throws Exception {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        request.setBeneficiaryEmail("bob.example.com");

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/policy-beneficiary-change/email")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0))
                .createEmailChange(any(CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.class));
    }

    private CreatePolicyBeneficiaryChangeWorkOrderRequest buildRequest() {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = new CreatePolicyBeneficiaryChangeWorkOrderRequest();
        request.setPolicyNo("P-20001");
        request.setBeneficiaryName("Bob");
        request.setBeneficiaryIdNo("1234567890");
        request.setBeneficiaryRelation(BeneficiaryRelationType.CHILD);
        request.setBenefitRatio(50);
        request.setRequester("alice");
        return request;
    }

    private PolicyBeneficiaryChangeWorkOrderResponse buildResponse() {
        PolicyBeneficiaryChangeWorkOrderResponse response = new PolicyBeneficiaryChangeWorkOrderResponse();
        response.setWorkOrderId("WO-BEN-10001");
        response.setPolicyNo("P-20001");
        response.setBeneficiaryName("Bob");
        response.setBeneficiaryIdNoMasked("****7890");
        response.setBeneficiaryRelation(BeneficiaryRelationType.CHILD);
        response.setBenefitRatio(50);
        response.setRequester("alice");
        response.setStatus(WorkOrderStatus.SUBMITTED);
        response.setCreatedAt(Instant.parse("2026-05-29T04:00:00Z"));
        return response;
    }

    private CreatePolicyBeneficiaryEmailChangeWorkOrderRequest buildEmailRequest() {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request =
                new CreatePolicyBeneficiaryEmailChangeWorkOrderRequest();
        request.setPolicyNo("P-20001");
        request.setBeneficiaryName("Bob");
        request.setBeneficiaryIdNo("1234567890");
        request.setBeneficiaryEmail("bob@example.com");
        request.setRequester("alice");
        return request;
    }

    private PolicyBeneficiaryChangeWorkOrderResponse buildEmailResponse() {
        PolicyBeneficiaryChangeWorkOrderResponse response = new PolicyBeneficiaryChangeWorkOrderResponse();
        response.setWorkOrderId("WO-BEN-EMAIL-10001");
        response.setPolicyNo("P-20001");
        response.setBeneficiaryName("Bob");
        response.setBeneficiaryIdNoMasked("****7890");
        response.setBeneficiaryEmail("bob@example.com");
        response.setRequester("alice");
        response.setStatus(WorkOrderStatus.SUBMITTED);
        response.setCreatedAt(Instant.parse("2026-05-29T04:00:00Z"));
        return response;
    }
}
