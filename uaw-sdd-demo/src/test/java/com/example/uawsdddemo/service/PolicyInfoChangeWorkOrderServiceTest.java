package com.example.uawsdddemo.service;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.exception.NotFoundException;
import com.example.uawsdddemo.model.dto.CreatePolicyInfoChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyInfoChangeWorkOrderResponse;
import com.example.uawsdddemo.model.entity.PolicyInfoChangeWorkOrder;
import com.example.uawsdddemo.model.enums.ChangeFieldType;
import com.example.uawsdddemo.repository.PolicyInfoChangeWorkOrderRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Optional;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class PolicyInfoChangeWorkOrderServiceTest {

    @Mock
    private PolicyInfoChangeWorkOrderRepository repository;

    @InjectMocks
    private PolicyInfoChangeWorkOrderService service;

    @Test
    public void testCreate_success_expectSubmittedWorkOrder() {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        when(repository.existsSubmittedDuplicate(any(PolicyInfoChangeWorkOrder.class))).thenReturn(false);
        when(repository.save(any(PolicyInfoChangeWorkOrder.class))).thenAnswer(invocation -> invocation.getArgument(0));

        PolicyInfoChangeWorkOrderResponse response = service.create(request);

        assertNotNull(response);
        assertNotNull(response.getWorkOrderId());
        assertEquals("P-10001", response.getPolicyNo());
        assertEquals(ChangeFieldType.HOLDER_PHONE, response.getChangeFieldType());
        assertEquals("13800000000", response.getOldValue());
        assertEquals("13900000000", response.getNewValue());
        assertNull(response.getChangeSummary());
        verify(repository, times(1)).existsSubmittedDuplicate(any(PolicyInfoChangeWorkOrder.class));
        verify(repository, times(1)).save(any(PolicyInfoChangeWorkOrder.class));
    }

    @Test
    public void testCreate_sameOldAndNewValue_expectBadRequest() {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        request.setNewValue(request.getOldValue());

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("newValue must be different from oldValue", exception.getMessage());
        verify(repository, never()).save(any(PolicyInfoChangeWorkOrder.class));
    }

    @Test
    public void testCreate_duplicateSubmittedWorkOrder_expectBadRequest() {
        CreatePolicyInfoChangeWorkOrderRequest request = buildRequest();
        when(repository.existsSubmittedDuplicate(any(PolicyInfoChangeWorkOrder.class))).thenReturn(true);

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("submitted duplicate policy info change work order exists", exception.getMessage());
        verify(repository, never()).save(any(PolicyInfoChangeWorkOrder.class));
    }

    @Test
    public void testGet_existingWorkOrder_expectResponse() {
        PolicyInfoChangeWorkOrder workOrder = PolicyInfoChangeWorkOrder.submitted(
                "P-10001",
                ChangeFieldType.HOLDER_PHONE,
                "13800000000",
                "13900000000",
                "alice");
        when(repository.findById(workOrder.getWorkOrderId())).thenReturn(Optional.of(workOrder));

        PolicyInfoChangeWorkOrderResponse response = service.get(workOrder.getWorkOrderId());

        assertNotNull(response);
        assertEquals(workOrder.getWorkOrderId(), response.getWorkOrderId());
        assertEquals("P-10001", response.getPolicyNo());
        assertEquals("HOLDER_PHONE: 13800000000 -> 13900000000", response.getChangeSummary());
        verify(repository, times(1)).findById(workOrder.getWorkOrderId());
    }

    @Test
    public void testGet_missingWorkOrder_expectNotFound() {
        when(repository.findById("missing")).thenReturn(Optional.empty());

        NotFoundException exception = assertThrows(NotFoundException.class, () -> service.get("missing"));

        assertEquals("policy info change work order not found", exception.getMessage());
        verify(repository, times(1)).findById("missing");
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
}
