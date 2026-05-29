package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.model.dto.CreatePolicyInfoChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyInfoChangeWorkOrderResponse;
import com.example.uawsdddemo.service.PolicyInfoChangeWorkOrderService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/work-orders/policy-info-change")
public class PolicyInfoChangeWorkOrderController {

    private final PolicyInfoChangeWorkOrderService service;

    public PolicyInfoChangeWorkOrderController(PolicyInfoChangeWorkOrderService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PolicyInfoChangeWorkOrderResponse create(@Valid @RequestBody CreatePolicyInfoChangeWorkOrderRequest request) {
        return service.create(request);
    }

    @GetMapping("/{workOrderId}")
    public PolicyInfoChangeWorkOrderResponse get(@PathVariable String workOrderId) {
        return service.get(workOrderId);
    }
}
