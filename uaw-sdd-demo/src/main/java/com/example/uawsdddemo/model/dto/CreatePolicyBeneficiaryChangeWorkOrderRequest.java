package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.BeneficiaryRelationType;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class CreatePolicyBeneficiaryChangeWorkOrderRequest {

    @NotBlank
    private String policyNo;

    @NotBlank
    private String beneficiaryName;

    @NotBlank
    private String beneficiaryIdNo;

    @NotNull
    private BeneficiaryRelationType beneficiaryRelation;

    @NotNull
    @Min(1)
    @Max(100)
    private Integer benefitRatio;

    @NotBlank
    private String requester;

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

    public String getBeneficiaryIdNo() {
        return beneficiaryIdNo;
    }

    public void setBeneficiaryIdNo(String beneficiaryIdNo) {
        this.beneficiaryIdNo = beneficiaryIdNo;
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
}
