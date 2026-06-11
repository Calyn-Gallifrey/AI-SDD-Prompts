package com.example.uawsdddemo.model.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public class CreatePolicyBeneficiaryEmailChangeWorkOrderRequest {

    @NotBlank
    private String policyNo;

    @NotBlank
    private String beneficiaryName;

    @NotBlank
    private String beneficiaryIdNo;

    @NotBlank
    @Email
    private String beneficiaryEmail;

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

    public String getBeneficiaryEmail() {
        return beneficiaryEmail;
    }

    public void setBeneficiaryEmail(String beneficiaryEmail) {
        this.beneficiaryEmail = beneficiaryEmail == null ? null : beneficiaryEmail.trim();
    }

    public String getRequester() {
        return requester;
    }

    public void setRequester(String requester) {
        this.requester = requester;
    }
}
