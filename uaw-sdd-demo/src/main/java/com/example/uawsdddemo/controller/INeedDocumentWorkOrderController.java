package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.model.dto.CreateINeedDocumentWorkOrderRequest;
import com.example.uawsdddemo.model.dto.INeedDocumentWorkOrderResponse;
import com.example.uawsdddemo.service.INeedDocumentWorkOrderService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/work-orders/i-need-document")
public class INeedDocumentWorkOrderController {

    private final INeedDocumentWorkOrderService service;

    public INeedDocumentWorkOrderController(INeedDocumentWorkOrderService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public INeedDocumentWorkOrderResponse create(
            @Valid @RequestBody CreateINeedDocumentWorkOrderRequest request) {
        return service.create(request);
    }
}
