package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;

public class PolicyBeneficiaryChangeWorkOrderResponse {

    private String workOrderId;
    private String policyNo;
    private String beneficiaryName;
    private String beneficiaryIdNoMasked;
    private BeneficiaryRelationType beneficiaryRelation;
    private Integer benefitRatio;
    private String requester;
    private WorkOrderStatus status;
    private Instant createdAt;

    public String getWorkOrderId() {
        return workOrderId;
    }

    public void setWorkOrderId(String workOrderId) {
        this.workOrderId = workOrderId;
    }

    public String getPolicyNo() {
        return policyNo;
    }

    public void setPolicyNo(String policyNo) {
        this.policyNo = policyNo;
    }

    public String getBeneficiaryName() {
        return beneficiaryName;
    }

    public void setBeneficiaryName(String beneficiaryName) {
        this.beneficiaryName = beneficiaryName;
    }

    public String getBeneficiaryIdNoMasked() {
        return beneficiaryIdNoMasked;
    }

    public void setBeneficiaryIdNoMasked(String beneficiaryIdNoMasked) {
        this.beneficiaryIdNoMasked = beneficiaryIdNoMasked;
    }

    public BeneficiaryRelationType getBeneficiaryRelation() {
        return beneficiaryRelation;
    }

    public void setBeneficiaryRelation(BeneficiaryRelationType beneficiaryRelation) {
        this.beneficiaryRelation = beneficiaryRelation;
    }

    public Integer getBenefitRatio() {
        return benefitRatio;
    }

    public void setBenefitRatio(Integer benefitRatio) {
        this.benefitRatio = benefitRatio;
    }

    public String getRequester() {
        return requester;
    }

    public void setRequester(String requester) {
        this.requester = requester;
    }

    public WorkOrderStatus getStatus() {
        return status;
    }

    public void setStatus(WorkOrderStatus status) {
        this.status = status;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
