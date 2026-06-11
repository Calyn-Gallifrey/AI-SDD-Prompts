package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;
import java.util.List;

public class INeedDocumentWorkOrderResponse {

    private String workOrderId;
    private String policyNo;
    private String customerName;
    private INeedDocumentRequestType requestType;
    private List<String> documentTypes;
    private String deliveryEmail;
    private String downstreamSubmissionId;
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
        this.deliveryEmail = deliveryEmail;
    }

    public String getDownstreamSubmissionId() {
        return downstreamSubmissionId;
    }

    public void setDownstreamSubmissionId(String downstreamSubmissionId) {
        this.downstreamSubmissionId = downstreamSubmissionId;
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
