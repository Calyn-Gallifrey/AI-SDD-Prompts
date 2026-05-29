package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.ChangeFieldType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class CreatePolicyInfoChangeWorkOrderRequest {

    @NotBlank
    private String policyNo;

    @NotNull
    private ChangeFieldType changeFieldType;

    @NotBlank
    private String oldValue;

    @NotBlank
    private String newValue;

    @NotBlank
    private String requester;

    public String getPolicyNo() {
        return policyNo;
    }

    public void setPolicyNo(String policyNo) {
        this.policyNo = policyNo;
    }

    public ChangeFieldType getChangeFieldType() {
        return changeFieldType;
    }

    public void setChangeFieldType(ChangeFieldType changeFieldType) {
        this.changeFieldType = changeFieldType;
    }

    public String getOldValue() {
        return oldValue;
    }

    public void setOldValue(String oldValue) {
        this.oldValue = oldValue;
    }

    public String getNewValue() {
        return newValue;
    }

    public void setNewValue(String newValue) {
        this.newValue = newValue;
    }

    public String getRequester() {
        return requester;
    }

    public void setRequester(String requester) {
        this.requester = requester;
    }
}
