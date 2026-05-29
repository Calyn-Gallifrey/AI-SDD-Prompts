package com.example.uawsdddemo.controller;

import com.example.uawsdddemo.model.dto.CreatePolicyBeneficiaryChangeWorkOrderRequest;
import com.example.uawsdddemo.model.dto.PolicyBeneficiaryChangeWorkOrderResponse;
import com.example.uawsdddemo.service.PolicyBeneficiaryChangeWorkOrderService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/work-orders/policy-beneficiary-change")
public class PolicyBeneficiaryChangeWorkOrderController {

    private final PolicyBeneficiaryChangeWorkOrderService service;

    public PolicyBeneficiaryChangeWorkOrderController(PolicyBeneficiaryChangeWorkOrderService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PolicyBeneficiaryChangeWorkOrderResponse create(
            @Valid @RequestBody CreatePolicyBeneficiaryChangeWorkOrderRequest request) {
        return service.create(request);
    }
}
