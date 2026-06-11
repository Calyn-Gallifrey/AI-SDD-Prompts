package com.example.uawsdddemo.service;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryEmailChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyBeneficiaryChangeWorkOrderResponse;
import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;
import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import com.example.uawsdddemo.repository.PolicyBeneficiaryChangeWorkOrderRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Optional;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class PolicyBeneficiaryChangeWorkOrderServiceTest {

    @Mock
    private PolicyBeneficiaryChangeWorkOrderRepository repository;

    @InjectMocks
    private PolicyBeneficiaryChangeWorkOrderService service;

    @Test
    public void testCreate_success_expectSubmittedWorkOrderWithMaskedIdNo() {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        when(repository.saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class)))
                .thenAnswer(invocation -> Optional.of(invocation.getArgument(0)));

        PolicyBeneficiaryChangeWorkOrderResponse response = service.create(request);

        assertNotNull(response);
        assertNotNull(response.getWorkOrderId());
        assertEquals("P-20001", response.getPolicyNo());
        assertEquals("Bob", response.getBeneficiaryName());
        assertEquals("****7890", response.getBeneficiaryIdNoMasked());
        assertEquals(BeneficiaryRelationType.CHILD, response.getBeneficiaryRelation());
        assertEquals(Integer.valueOf(50), response.getBenefitRatio());
        verify(repository, times(1)).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreate_lowBenefitRatio_expectBadRequest() {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        request.setBenefitRatio(0);

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("benefitRatio must be between 1 and 100", exception.getMessage());
        verify(repository, never()).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreate_highBenefitRatio_expectBadRequest() {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        request.setBenefitRatio(101);

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("benefitRatio must be between 1 and 100", exception.getMessage());
        verify(repository, never()).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreate_duplicateSubmittedWorkOrder_expectBadRequest() {
        CreatePolicyBeneficiaryChangeWorkOrderRequest request = buildRequest();
        when(repository.saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class)))
                .thenReturn(Optional.empty());

        BadRequestException exception = assertThrows(BadRequestException.class, () -> service.create(request));

        assertEquals("submitted duplicate policy beneficiary change work order exists", exception.getMessage());
        verify(repository, times(1)).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreateEmailChange_success_expectSubmittedWorkOrderWithNormalizedEmail() {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        request.setBeneficiaryEmail("  Bob.Email@Example.COM  ");
        when(repository.saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class)))
                .thenAnswer(invocation -> Optional.of(invocation.getArgument(0)));

        PolicyBeneficiaryChangeWorkOrderResponse response = service.createEmailChange(request);

        assertNotNull(response);
        assertNotNull(response.getWorkOrderId());
        assertEquals("P-20001", response.getPolicyNo());
        assertEquals("Bob", response.getBeneficiaryName());
        assertEquals("****7890", response.getBeneficiaryIdNoMasked());
        assertEquals("bob.email@example.com", response.getBeneficiaryEmail());
        assertEquals("alice", response.getRequester());
        verify(repository, times(1)).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreateEmailChange_blankEmail_expectBadRequest() {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        request.setBeneficiaryEmail(" ");

        BadRequestException exception = assertThrows(
                BadRequestException.class,
                () -> service.createEmailChange(request));

        assertEquals("beneficiaryEmail must not be blank", exception.getMessage());
        verify(repository, never()).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreateEmailChange_invalidEmail_expectBadRequest() {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        request.setBeneficiaryEmail("bob.example.com");

        BadRequestException exception = assertThrows(
                BadRequestException.class,
                () -> service.createEmailChange(request));

        assertEquals("beneficiaryEmail must be a valid email", exception.getMessage());
        verify(repository, never()).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
    }

    @Test
    public void testCreateEmailChange_duplicateSubmittedWorkOrder_expectBadRequest() {
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request = buildEmailRequest();
        when(repository.saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class)))
                .thenReturn(Optional.empty());

        BadRequestException exception = assertThrows(
                BadRequestException.class,
                () -> service.createEmailChange(request));

        assertEquals(
                "submitted duplicate policy beneficiary email change work order exists",
                exception.getMessage());
        verify(repository, times(1)).saveSubmittedIfAbsent(any(PolicyBeneficiaryChangeWorkOrder.class));
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
}
