package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;
import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import org.junit.Test;

import java.util.Optional;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest {

    private final InMemoryPolicyBeneficiaryChangeWorkOrderRepository repository =
            new InMemoryPolicyBeneficiaryChangeWorkOrderRepository();

    @Test
    public void testSaveSubmittedIfAbsent_duplicateSubmittedBeneficiary_expectEmpty() {
        PolicyBeneficiaryChangeWorkOrder first = buildWorkOrder("P-20001", "1234567890");
        PolicyBeneficiaryChangeWorkOrder duplicate = buildWorkOrder("P-20001", "1234567890");

        Optional<PolicyBeneficiaryChangeWorkOrder> firstSaved = repository.saveSubmittedIfAbsent(first);
        Optional<PolicyBeneficiaryChangeWorkOrder> duplicateSaved = repository.saveSubmittedIfAbsent(duplicate);

        assertTrue(firstSaved.isPresent());
        assertFalse(duplicateSaved.isPresent());
    }

    @Test
    public void testSaveSubmittedIfAbsent_differentPolicy_expectSaved() {
        PolicyBeneficiaryChangeWorkOrder first = buildWorkOrder("P-20001", "1234567890");
        PolicyBeneficiaryChangeWorkOrder second = buildWorkOrder("P-20002", "1234567890");

        Optional<PolicyBeneficiaryChangeWorkOrder> firstSaved = repository.saveSubmittedIfAbsent(first);
        Optional<PolicyBeneficiaryChangeWorkOrder> secondSaved = repository.saveSubmittedIfAbsent(second);

        assertTrue(firstSaved.isPresent());
        assertTrue(secondSaved.isPresent());
    }

    private PolicyBeneficiaryChangeWorkOrder buildWorkOrder(String policyNo, String beneficiaryIdNo) {
        return PolicyBeneficiaryChangeWorkOrder.submitted(
                policyNo,
                "Bob",
                beneficiaryIdNo,
                BeneficiaryRelationType.CHILD,
                50,
                "alice");
    }
}
