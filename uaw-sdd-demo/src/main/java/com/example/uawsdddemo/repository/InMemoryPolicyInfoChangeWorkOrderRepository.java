package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.PolicyInfoChangeWorkOrder;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryPolicyInfoChangeWorkOrderRepository implements PolicyInfoChangeWorkOrderRepository {

    private final Map<String, PolicyInfoChangeWorkOrder> store = new ConcurrentHashMap<>();

    @Override
    public PolicyInfoChangeWorkOrder save(PolicyInfoChangeWorkOrder workOrder) {
        store.put(workOrder.getWorkOrderId(), workOrder);
        return workOrder;
    }

    @Override
    public Optional<PolicyInfoChangeWorkOrder> findById(String workOrderId) {
        return Optional.ofNullable(store.get(workOrderId));
    }

    @Override
    public boolean existsSubmittedDuplicate(PolicyInfoChangeWorkOrder candidate) {
        return store.values().stream().anyMatch(existing -> existing.hasSameBusinessKey(candidate));
    }
}
