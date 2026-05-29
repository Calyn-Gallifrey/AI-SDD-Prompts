package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryPolicyBeneficiaryChangeWorkOrderRepository
        implements PolicyBeneficiaryChangeWorkOrderRepository {

    private final Map<String, PolicyBeneficiaryChangeWorkOrder> store = new ConcurrentHashMap<>();

    @Override
    public synchronized Optional<PolicyBeneficiaryChangeWorkOrder> saveSubmittedIfAbsent(
            PolicyBeneficiaryChangeWorkOrder workOrder) {
        boolean duplicate = store.values().stream()
                .anyMatch(existing -> existing.hasSameSubmittedBeneficiary(workOrder));
        if (duplicate) {
            return Optional.empty();
        }
        store.put(workOrder.getWorkOrderId(), workOrder);
        return Optional.of(workOrder);
    }
}
