package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;

import java.util.Optional;

public interface PolicyBeneficiaryChangeWorkOrderRepository {

    Optional<PolicyBeneficiaryChangeWorkOrder> saveSubmittedIfAbsent(
            PolicyBeneficiaryChangeWorkOrder workOrder);
}
