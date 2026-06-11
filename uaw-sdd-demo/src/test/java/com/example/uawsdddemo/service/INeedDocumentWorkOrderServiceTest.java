package com.example.uawsdddemo.service;

import com.example.uawsdddemo.client.INeedDocumentDownstreamClient;
import com.example.uawsdddemo.client.INeedDocumentWorkOrderSubmission;
import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.model.dto.CreateINeedDocumentWorkOrderRequest;
import com.example.uawsdddemo.model.dto.INeedDocumentWorkOrderResponse;
import com.example.uawsdddemo.model.entity.INeedDocumentWorkOrder;
import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;
import com.example.uawsdddemo.repository.INeedDocumentWorkOrderRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Arrays;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class INeedDocumentWorkOrderServiceTest {

    @Mock
    private INeedDocumentWorkOrderRepository repository;

    @Mock
    private INeedDocumentDownstreamClient downstreamClient;

    @InjectMocks
    private INeedDocumentWorkOrderService service;

    @Test
    public void testCreateQueryDocument_success_expectSubmittedWorkOrder() {
        CreateINeedDocumentWorkOrderRequest request = buildRequest(INeedDocumentRequestType.QUERY_DOCUMENT);
        request.setDocumentTypes(Arrays.asList(" policy schedule ", "statement"));
        request.setDeliveryEmail("ignored@example.com");
        when(downstreamClient.submit(any(INeedDocumentWorkOrderSubmission.class))).thenReturn("DOC-10001");
        when(repository.save(any(INeedDocumentWorkOrder.class))).thenAnswer(invocation -> invocation.getArgument(0));

        INeedDocumentWorkOrderResponse response = service.create(request);

        assertEquals("P-30001", response.getPolicyNo());
        assertEquals("Mary", response.getCustomerName());
        assertEquals(INeedDocumentRequestType.QUERY_DOCUMENT, response.getRequestType());
        assertEquals(Arrays.asList("policy schedule", "statement"), response.getDocumentTypes());
        assertNull(response.getDeliveryEmail());
        assertEquals("DOC-10001", response.getDownstreamSubmissionId());
        assertEquals(WorkOrderStatus.SUBMITTED, response.getStatus());
        verify(downstreamClient, times(1)).submit(any(INeedDocumentWorkOrderSubmission.class));
        verify(repository, times(1)).save(any(INeedDocumentWorkOrder.class));
    }

    @Test
    public void testCreateSendDocument_success_expectNormalizedEmail() {
        CreateINeedDocumentWorkOrderRequest request = buildRequest(INeedDocumentRequestType.SEND_DOCUMENT);
        request.setDeliveryEmail("  Customer.Email@Example.COM  ");
        when(downstreamClient.submit(any(INeedDocumentWorkOrderSubmission.class))).thenReturn("DOC-10002");
        when(repository.save(any(INeedDocumentWorkOrder.class))).thenAnswer(invocation -> invocation.getArgument(0));

        INeedDocumentWorkOrderResponse response = service.create(request);

        assertEquals("customer.email@example.com", response.getDeliveryEmail());
        assertEquals("DOC-10002", response.getDownstreamSubmissionId());
        ArgumentCaptor<INeedDocumentWorkOrderSubmission> captor =
                ArgumentCaptor.forClass(INeedDocumentWorkOrderSubmission.class);
        verify(downstreamClient, times(1)).submit(captor.capture());
        assertEquals("customer.email@example.com", captor.getValue().getDeliveryEmail());
    }

    @Test
    public void testCreateSendDocument_missingEmail_expectBadRequest() {
        CreateINeedDocumentWorkOrderRequest request = buildRequest(INeedDocumentRequestType.SEND_DOCUMENT);
        request.setDeliveryEmail(" ");

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("deliveryEmail is required for SEND_DOCUMENT", exception.getMessage());
        verify(downstreamClient, never()).submit(any(INeedDocumentWorkOrderSubmission.class));
        verify(repository, never()).save(any(INeedDocumentWorkOrder.class));
    }

    @Test
    public void testCreate_blankDocumentType_expectBadRequest() {
        CreateINeedDocumentWorkOrderRequest request = buildRequest(INeedDocumentRequestType.QUERY_DOCUMENT);
        request.setDocumentTypes(Arrays.asList("policy schedule", " "));

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("documentTypes must not contain blank value", exception.getMessage());
        verify(downstreamClient, never()).submit(any(INeedDocumentWorkOrderSubmission.class));
        verify(repository, never()).save(any(INeedDocumentWorkOrder.class));
    }

    @Test
    public void testCreate_missingRequestType_expectBadRequest() {
        CreateINeedDocumentWorkOrderRequest request = buildRequest(null);

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("requestType is required", exception.getMessage());
        verify(downstreamClient, never()).submit(any(INeedDocumentWorkOrderSubmission.class));
        verify(repository, never()).save(any(INeedDocumentWorkOrder.class));
    }

    private CreateINeedDocumentWorkOrderRequest buildRequest(INeedDocumentRequestType requestType) {
        CreateINeedDocumentWorkOrderRequest request = new CreateINeedDocumentWorkOrderRequest();
        request.setPolicyNo("P-30001");
        request.setCustomerName("Mary");
        request.setRequestType(requestType);
        request.setDocumentTypes(Arrays.asList("policy schedule"));
        request.setRequester("agent01");
        return request;
    }
}
