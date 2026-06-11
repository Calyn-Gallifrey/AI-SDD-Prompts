package com.example.uawsdddemo.repository;

import com.example.uawsdddemo.model.entity.INeedDocumentWorkOrder;
import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import org.junit.Test;

import java.util.Arrays;
import java.util.Optional;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class InMemoryINeedDocumentWorkOrderRepositoryTest {

    private final InMemoryINeedDocumentWorkOrderRepository repository =
            new InMemoryINeedDocumentWorkOrderRepository();

    @Test
    public void testSaveAndFindById_existingWorkOrder_expectFound() {
        INeedDocumentWorkOrder workOrder = INeedDocumentWorkOrder.submitted(
                "P-30001",
                "Mary",
                INeedDocumentRequestType.QUERY_DOCUMENT,
                Arrays.asList("policy schedule"),
                null,
                "agent01",
                "DOC-10001");

        INeedDocumentWorkOrder saved = repository.save(workOrder);
        Optional<INeedDocumentWorkOrder> found = repository.findById(saved.getWorkOrderId());

        assertTrue(found.isPresent());
        assertEquals("P-30001", found.get().getPolicyNo());
        assertEquals("DOC-10001", found.get().getDownstreamSubmissionId());
    }
}
