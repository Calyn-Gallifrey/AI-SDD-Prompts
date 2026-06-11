package com.example.uawsdddemo.service;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryEmailChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyBeneficiaryChangeWorkOrderResponse;
import com.example.uawsdddemo.model.entity.PolicyBeneficiaryChangeWorkOrder;
import com.example.uawsdddemo.repository.PolicyBeneficiaryChangeWorkOrderRepository;
import org.springframework.stereotype.Service;

import java.util.Locale;
import java.util.regex.Pattern;

@Service
public class PolicyBeneficiaryChangeWorkOrderService {

    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");

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

    public PolicyBeneficiaryChangeWorkOrderResponse createEmailChange(
            CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request) {
        String beneficiaryEmail = normalizeEmail(request.getBeneficiaryEmail());

        PolicyBeneficiaryChangeWorkOrder workOrder = PolicyBeneficiaryChangeWorkOrder.submittedEmailChange(
                request.getPolicyNo(),
                request.getBeneficiaryName(),
                request.getBeneficiaryIdNo(),
                beneficiaryEmail,
                request.getRequester());

        PolicyBeneficiaryChangeWorkOrder saved = repository.saveSubmittedIfAbsent(workOrder)
                .orElseThrow(() -> new BadRequestException(
                        "submitted duplicate policy beneficiary email change work order exists"));

        return toResponse(saved);
    }

    private void validateBenefitRatio(Integer benefitRatio) {
        if (benefitRatio == null || benefitRatio < 1 || benefitRatio > 100) {
            throw new BadRequestException("benefitRatio must be between 1 and 100");
        }
    }

    private String normalizeEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            throw new BadRequestException("beneficiaryEmail must not be blank");
        }

        String normalizedEmail = email.trim().toLowerCase(Locale.ROOT);
        if (!EMAIL_PATTERN.matcher(normalizedEmail).matches()) {
            throw new BadRequestException("beneficiaryEmail must be a valid email");
        }
        return normalizedEmail;
    }

    private PolicyBeneficiaryChangeWorkOrderResponse toResponse(PolicyBeneficiaryChangeWorkOrder workOrder) {
        PolicyBeneficiaryChangeWorkOrderResponse response = new PolicyBeneficiaryChangeWorkOrderResponse();
        response.setWorkOrderId(workOrder.getWorkOrderId());
        response.setPolicyNo(workOrder.getPolicyNo());
        response.setBeneficiaryName(workOrder.getBeneficiaryName());
        response.setBeneficiaryIdNoMasked(maskIdNo(workOrder.getBeneficiaryIdNo()));
        response.setBeneficiaryRelation(workOrder.getBeneficiaryRelation());
        response.setBenefitRatio(workOrder.getBenefitRatio());
        response.setBeneficiaryEmail(workOrder.getBeneficiaryEmail());
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
