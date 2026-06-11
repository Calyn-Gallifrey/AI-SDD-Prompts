package com.example.uawsdddemo.model.entity;

import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

public class INeedDocumentWorkOrder {

    private final String workOrderId;
    private final String policyNo;
    private final String customerName;
    private final INeedDocumentRequestType requestType;
    private final List<String> documentTypes;
    private final String deliveryEmail;
    private final String downstreamSubmissionId;
    private final String requester;
    private final WorkOrderStatus status;
    private final Instant createdAt;

    public INeedDocumentWorkOrder(
            String workOrderId,
            String policyNo,
            String customerName,
            INeedDocumentRequestType requestType,
            List<String> documentTypes,
            String deliveryEmail,
            String downstreamSubmissionId,
            String requester,
            WorkOrderStatus status,
            Instant createdAt) {
        this.workOrderId = workOrderId;
        this.policyNo = policyNo;
        this.customerName = customerName;
        this.requestType = requestType;
        this.documentTypes = List.copyOf(documentTypes);
        this.deliveryEmail = deliveryEmail;
        this.downstreamSubmissionId = downstreamSubmissionId;
        this.requester = requester;
        this.status = status;
        this.createdAt = createdAt;
    }

    public static INeedDocumentWorkOrder submitted(
            String policyNo,
            String customerName,
            INeedDocumentRequestType requestType,
            List<String> documentTypes,
            String deliveryEmail,
            String requester,
            String downstreamSubmissionId) {
        return new INeedDocumentWorkOrder(
                UUID.randomUUID().toString(),
                policyNo,
                customerName,
                requestType,
                documentTypes,
                deliveryEmail,
                downstreamSubmissionId,
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

    public String getDownstreamSubmissionId() {
        return downstreamSubmissionId;
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
}
