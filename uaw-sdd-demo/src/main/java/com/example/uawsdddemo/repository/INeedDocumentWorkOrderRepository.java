package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.INeedDocumentWorkOrder;

import java.util.Optional;

public interface INeedDocumentWorkOrderRepository {

    INeedDocumentWorkOrder save(INeedDocumentWorkOrder workOrder);

    Optional<INeedDocumentWorkOrder> findById(String workOrderId);
}
