package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.List;

public class CreateINeedDocumentWorkOrderRequest {

    @NotBlank
    private String policyNo;

    @NotBlank
    private String customerName;

    @NotNull
    private INeedDocumentRequestType requestType;

    @NotEmpty
    @Size(max = 10)
    private List<String> documentTypes;

    @Email
    private String deliveryEmail;

    @NotBlank
    private String requester;

    public String getPolicyNo() {
        return policyNo;
    }

    public void setPolicyNo(String policyNo) {
        this.policyNo = policyNo;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public INeedDocumentRequestType getRequestType() {
        return requestType;
    }

    public void setRequestType(INeedDocumentRequestType requestType) {
        this.requestType = requestType;
    }

    public List<String> getDocumentTypes() {
        return documentTypes;
    }

    public void setDocumentTypes(List<String> documentTypes) {
        this.documentTypes = documentTypes;
    }

    public String getDeliveryEmail() {
        return deliveryEmail;
    }

    public void setDeliveryEmail(String deliveryEmail) {
        this.deliveryEmail = deliveryEmail == null ? null : deliveryEmail.trim();
    }

    public String getRequester() {
        return requester;
    }

    public void setRequester(String requester) {
        this.requester = requester;
    }
}
