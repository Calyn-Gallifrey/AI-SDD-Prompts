package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.INeedDocumentWorkOrder;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryINeedDocumentWorkOrderRepository implements INeedDocumentWorkOrderRepository {

    private final Map<String, INeedDocumentWorkOrder> store = new ConcurrentHashMap<>();

    @Override
    public INeedDocumentWorkOrder save(INeedDocumentWorkOrder workOrder) {
        store.put(workOrder.getWorkOrderId(), workOrder);
        return workOrder;
    }

    @Override
    public Optional<INeedDocumentWorkOrder> findById(String workOrderId) {
        return Optional.ofNullable(store.get(workOrderId));
    }
}
