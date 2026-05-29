package com.example.uawsdddemo.service;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyBeneficiaryChangeWorkOrderResponse;
import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;
import com.example.uawsdddemo.repository.PolicyBeneficiaryChangeWorkOrderRepository;
import org.springframework.stereotype.Service;

@Service
public class PolicyBeneficiaryChangeWorkOrderService {

    private final PolicyBeneficiaryChangeWorkOrderRepository repository;

    public PolicyBeneficiaryChangeWorkOrderService(PolicyBeneficiaryChangeWorkOrderRepository repository) {
        this.repository = repository;
    }

    public PolicyBeneficiaryChangeWorkOrderResponse create(
            CreatePolicyBeneficiaryChangeWorkOrderRequest request) {
        validateBenefitRatio(request.getBenefitRatio());

        PolicyBeneficiaryChangeWorkOrder workOrder = PolicyBeneficiaryChangeWorkOrder.submitted(
                request.getPolicyNo(),
                request.getBeneficiaryName(),
                request.getBeneficiaryIdNo(),
                request.getBeneficiaryRelation(),
                request.getBenefitRatio(),
                request.getRequester());

        PolicyBeneficiaryChangeWorkOrder saved = repository.saveSubmittedIfAbsent(workOrder)
                .orElseThrow(() -> new BadRequestException(
                        "submitted duplicate policy beneficiary change work order exists"));

        return toResponse(saved);
    }

    private void validateBenefitRatio(Integer benefitRatio) {
        if (benefitRatio == null || benefitRatio < 1 || benefitRatio > 100) {
            throw new BadRequestException("benefitRatio must be between 1 and 100");
        }
    }

    private PolicyBeneficiaryChangeWorkOrderResponse toResponse(PolicyBeneficiaryChangeWorkOrder workOrder) {
        PolicyBeneficiaryChangeWorkOrderResponse response = new PolicyBeneficiaryChangeWorkOrderResponse();
        response.setWorkOrderId(workOrder.getWorkOrderId());
        response.setPolicyNo(workOrder.getPolicyNo());
        response.setBeneficiaryName(workOrder.getBeneficiaryName());
        response.setBeneficiaryIdNoMasked(maskIdNo(workOrder.getBeneficiaryIdNo()));
        response.setBeneficiaryRelation(workOrder.getBeneficiaryRelation());
        response.setBenefitRatio(workOrder.getBenefitRatio());
        response.setRequester(workOrder.getRequester());
        response.setStatus(workOrder.getStatus());
        response.setCreatedAt(workOrder.getCreatedAt());
        return response;
    }

    private String maskIdNo(String idNo) {
        if (idNo == null || idNo.length() <= 4) {
            return "****";
        }
        return "****" + idNo.substring(idNo.length() - 4);
    }
}
