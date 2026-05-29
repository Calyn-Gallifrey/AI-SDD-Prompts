package com.example.uawsdddemo.model.entity;

import com.example.uawsdddemo.model.enums.ChangeFieldType;
import com.example.uawsdddemo.model.enums.WorkOrderStatus;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

public class PolicyInfoChangeWorkOrder {

    private final String workOrderId;
    private final String policyNo;
    private final ChangeFieldType changeFieldType;
    private final String oldValue;
    private final String newValue;
    private final String requester;
    private WorkOrderStatus status;
    private final Instant createdAt;

    public PolicyInfoChangeWorkOrder(
            String workOrderId,
            String policyNo,
            ChangeFieldType changeFieldType,
            String oldValue,
            String newValue,
            String requester,
            WorkOrderStatus status,
            Instant createdAt) {
        this.workOrderId = workOrderId;
        this.policyNo = policyNo;
        this.changeFieldType = changeFieldType;
        this.oldValue = oldValue;
        this.newValue = newValue;
        this.requester = requester;
        this.status = status;
        this.createdAt = createdAt;
    }

    public static PolicyInfoChangeWorkOrder submitted(
            String policyNo,
            ChangeFieldType changeFieldType,
            String oldValue,
            String newValue,
            String requester) {
        return new PolicyInfoChangeWorkOrder(
                UUID.randomUUID().toString(),
                policyNo,
                changeFieldType,
                oldValue,
                newValue,
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

    public ChangeFieldType getChangeFieldType() {
        return changeFieldType;
    }

    public String getOldValue() {
        return oldValue;
    }

    public String getNewValue() {
        return newValue;
    }

    public String getRequester() {
        return requester;
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

    public boolean hasSameBusinessKey(PolicyInfoChangeWorkOrder other) {
        return Objects.equals(policyNo, other.policyNo)
                && changeFieldType == other.changeFieldType
                && Objects.equals(newValue, other.newValue)
                && status == WorkOrderStatus.SUBMITTED;
    }
}
