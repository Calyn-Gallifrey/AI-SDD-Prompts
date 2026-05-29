package com.example.uawsdddemo.model.entity;

import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

public class PolicyBeneficiaryChangeWorkOrder {

    private final String workOrderId;
    private final String policyNo;
    private final String beneficiaryName;
    private final String beneficiaryIdNo;
    private final BeneficiaryRelationType beneficiaryRelation;
    private final Integer benefitRatio;
    private final String requester;
    private final WorkOrderStatus status;
    private final Instant createdAt;

    public PolicyBeneficiaryChangeWorkOrder(
            String workOrderId,
            String policyNo,
            String beneficiaryName,
            String beneficiaryIdNo,
            BeneficiaryRelationType beneficiaryRelation,
            Integer benefitRatio,
            String requester,
            WorkOrderStatus status,
            Instant createdAt) {
        this.workOrderId = workOrderId;
        this.policyNo = policyNo;
        this.beneficiaryName = beneficiaryName;
        this.beneficiaryIdNo = beneficiaryIdNo;
        this.beneficiaryRelation = beneficiaryRelation;
        this.benefitRatio = benefitRatio;
        this.requester = requester;
        this.status = status;
        this.createdAt = createdAt;
    }

    public static PolicyBeneficiaryChangeWorkOrder submitted(
            String policyNo,
            String beneficiaryName,
            String beneficiaryIdNo,
            BeneficiaryRelationType beneficiaryRelation,
            Integer benefitRatio,
            String requester) {
        return new PolicyBeneficiaryChangeWorkOrder(
                UUID.randomUUID().toString(),
                policyNo,
                beneficiaryName,
                beneficiaryIdNo,
                beneficiaryRelation,
                benefitRatio,
                requester,
                WorkOrderStatus.SUBMITTED,
                Instant.now());
    }

    public String getWorkOrderId() {
        return workOrderId;
    }

    public String getPolicyNo() {
        return policyNo;
    }

    public String getBeneficiaryName() {
        return beneficiaryName;
    }

    public String getBeneficiaryIdNo() {
        return beneficiaryIdNo;
    }

    public BeneficiaryRelationType getBeneficiaryRelation() {
        return beneficiaryRelation;
    }

    public Integer getBenefitRatio() {
        return benefitRatio;
    }

    public String getRequester() {
        return requester;
    }

    public WorkOrderStatus getStatus() {
        return status;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public boolean hasSameSubmittedBeneficiary(PolicyBeneficiaryChangeWorkOrder other) {
        return status == WorkOrderStatus.SUBMITTED
                && Objects.equals(policyNo, other.policyNo)
                && Objects.equals(beneficiaryIdNo, other.beneficiaryIdNo);
    }
}
