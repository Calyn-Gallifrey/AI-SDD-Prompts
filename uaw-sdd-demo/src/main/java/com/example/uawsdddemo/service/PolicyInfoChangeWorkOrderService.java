package com.example.uawsdddemo.service;

import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.exception.NotFoundException;
import com.example.uawsdddemo.model.dto.CreatePolicyInfoChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyInfoChangeWorkOrderResponse;
import com.example.uawsdddemo.model.entity.PolicyInfoChangeWorkOrder;
import com.example.uawsdddemo.repository.PolicyInfoChangeWorkOrderRepository;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class PolicyInfoChangeWorkOrderService {

    private final PolicyInfoChangeWorkOrderRepository repository;

    public PolicyInfoChangeWorkOrderService(PolicyInfoChangeWorkOrderRepository repository) {
        this.repository = repository;
    }

    public PolicyInfoChangeWorkOrderResponse create(CreatePolicyInfoChangeWorkOrderRequest request) {
        if (Objects.equals(request.getOldValue(), request.getNewValue())) {
            throw new BadRequestException("newValue must be different from oldValue");
        }

        PolicyInfoChangeWorkOrder workOrder = PolicyInfoChangeWorkOrder.submitted(
                request.getPolicyNo(),
                request.getChangeFieldType(),
                request.getOldValue(),
                request.getNewValue(),
                request.getRequester());

        if (repository.existsSubmittedDuplicate(workOrder)) {
            throw new BadRequestException("submitted duplicate policy info change work order exists");
        }

        return toResponse(repository.save(workOrder));
    }

    public PolicyInfoChangeWorkOrderResponse get(String workOrderId) {
        PolicyInfoChangeWorkOrder workOrder = repository.findById(workOrderId)
                .orElseThrow(() -> new NotFoundException("policy info change work order not found"));
        return toResponse(workOrder);
    }

    private PolicyInfoChangeWorkOrderResponse toResponse(PolicyInfoChangeWorkOrder workOrder) {
        PolicyInfoChangeWorkOrderResponse response = new PolicyInfoChangeWorkOrderResponse();
        response.setWorkOrderId(workOrder.getWorkOrderId());
        response.setPolicyNo(workOrder.getPolicyNo());
        response.setChangeFieldType(workOrder.getChangeFieldType());
        response.setOldValue(workOrder.getOldValue());
        response.setNewValue(workOrder.getNewValue());
        response.setRequester(workOrder.getRequester());
        response.setStatus(workOrder.getStatus());
        response.setCreatedAt(workOrder.getCreatedAt());
        return response;
    }
}
