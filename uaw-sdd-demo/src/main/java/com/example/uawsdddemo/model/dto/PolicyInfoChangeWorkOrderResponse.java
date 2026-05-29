package com.example.uawsdddemo.model.dto;

import com.example.uawsdddemo.model.enums.ChangeFieldType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;

public class PolicyInfoChangeWorkOrderResponse {

    private String workOrderId;
    private String policyNo;
    private ChangeFieldType changeFieldType;
    private String oldValue;
    private String newValue;
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
