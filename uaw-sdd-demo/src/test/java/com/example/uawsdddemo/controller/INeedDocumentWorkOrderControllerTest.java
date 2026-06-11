package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.handler.ApiExceptionHandler;
import com.example.uawsdddemo.model.dto.CreateINeedDocumentWorkOrderRequest;
import com.example.uawsdddemo.model.dto.INeedDocumentWorkOrderResponse;
import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;
import com.example.uawsdddemo.service.INeedDocumentWorkOrderService;
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
import java.util.Arrays;
import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(MockitoJUnitRunner.class)
public class INeedDocumentWorkOrderControllerTest {

    private final ObjectMapper objectMapper = new ObjectMapper();

    private MockMvc mockMvc;

    @Mock
    private INeedDocumentWorkOrderService service;

    @InjectMocks
    private INeedDocumentWorkOrderController controller;

    @Before
    public void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setControllerAdvice(new ApiExceptionHandler())
                .build();
    }

    @Test
    public void testCreate_success_expectCreatedResponse() throws Exception {
        CreateINeedDocumentWorkOrderRequest request = buildRequest();
        Mockito.when(service.create(any(CreateINeedDocumentWorkOrderRequest.class)))
                .thenReturn(buildResponse());

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/i-need-document")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.workOrderId", Matchers.is("WO-DOC-10001")))
                .andExpect(jsonPath("$.policyNo", Matchers.is("P-30001")))
                .andExpect(jsonPath("$.requestType", Matchers.is("SEND_DOCUMENT")))
                .andExpect(jsonPath("$.documentTypes[0]", Matchers.is("policy schedule")))
                .andExpect(jsonPath("$.deliveryEmail", Matchers.is("customer@example.com")))
                .andExpect(jsonPath("$.downstreamSubmissionId", Matchers.is("DOC-10001")))
                .andExpect(jsonPath("$.status", Matchers.is("SUBMITTED")));

        Mockito.verify(service, times(1)).create(any(CreateINeedDocumentWorkOrderRequest.class));
    }

    @Test
    public void testCreate_missingPolicyNo_expectBadRequest() throws Exception {
        CreateINeedDocumentWorkOrderRequest request = buildRequest();
        request.setPolicyNo("");

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/i-need-document")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0)).create(any(CreateINeedDocumentWorkOrderRequest.class));
    }

    @Test
    public void testCreate_emptyDocumentTypes_expectBadRequest() throws Exception {
        CreateINeedDocumentWorkOrderRequest request = buildRequest();
        request.setDocumentTypes(Collections.emptyList());

        mockMvc.perform(MockMvcRequestBuilders.post("/api/work-orders/i-need-document")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", Matchers.is("request validation failed")));

        Mockito.verify(service, times(0)).create(any(CreateINeedDocumentWorkOrderRequest.class));
    }

    private CreateINeedDocumentWorkOrderRequest buildRequest() {
        CreateINeedDocumentWorkOrderRequest request = new CreateINeedDocumentWorkOrderRequest();
        request.setPolicyNo("P-30001");
        request.setCustomerName("Mary");
        request.setRequestType(INeedDocumentRequestType.SEND_DOCUMENT);
        request.setDocumentTypes(Arrays.asList("policy schedule"));
        request.setDeliveryEmail("customer@example.com");
        request.setRequester("agent01");
        return request;
    }

    private INeedDocumentWorkOrderResponse buildResponse() {
        INeedDocumentWorkOrderResponse response = new INeedDocumentWorkOrderResponse();
        response.setWorkOrderId("WO-DOC-10001");
        response.setPolicyNo("P-30001");
        response.setCustomerName("Mary");
        response.setRequestType(INeedDocumentRequestType.SEND_DOCUMENT);
        response.setDocumentTypes(Arrays.asList("policy schedule"));
        response.setDeliveryEmail("customer@example.com");
        response.setDownstreamSubmissionId("DOC-10001");
        response.setRequester("agent01");
        response.setStatus(WorkOrderStatus.SUBMITTED);
        response.setCreatedAt(Instant.parse("2026-06-11T06:40:00Z"));
        return response;
    }
}
