package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.PolicyInfoChangeWorkOrder;

import java.util.Optional;

public interface PolicyInfoChangeWorkOrderRepository {

    PolicyInfoChangeWorkOrder save(PolicyInfoChangeWorkOrder workOrder);

    Optional<PolicyInfoChangeWorkOrder> findById(String workOrderId);

    boolean existsSubmittedDuplicate(PolicyInfoChangeWorkOrder candidate);
}
