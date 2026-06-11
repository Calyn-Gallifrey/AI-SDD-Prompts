package com.example.uawsdddemo.client;

import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;

import java.util.List;

public class INeedDocumentWorkOrderSubmission {

    private final String policyNo;
    private final String customerName;
    private final INeedDocumentRequestType requestType;
    private final List<String> documentTypes;
    private final String deliveryEmail;
    private final String requester;

    public INeedDocumentWorkOrderSubmission(
            String policyNo,
            String customerName,
            INeedDocumentRequestType requestType,
            List<String> documentTypes,
            String deliveryEmail,
            String requester) {
        this.policyNo = policyNo;
        this.customerName = customerName;
        this.requestType = requestType;
        this.documentTypes = List.copyOf(documentTypes);
        this.deliveryEmail = deliveryEmail;
        this.requester = requester;
    }

    public String getPolicyNo() {
        return policyNo;
    }

    public String getCustomerName() {
        return customerName;
    }

    public INeedDocumentRequestType getRequestType() {
        return requestType;
    }

    public List<String> getDocumentTypes() {
        return documentTypes;
    }

    public String getDeliveryEmail() {
        return deliveryEmail;
    }

    public String getRequester() {
        return requester;
    }
}
