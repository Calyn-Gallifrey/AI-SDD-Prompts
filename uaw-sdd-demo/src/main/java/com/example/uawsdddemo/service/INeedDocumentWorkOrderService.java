package com.example.uawsdddemo.service;

import com.example.uawsdddemo.client.INeedDocumentDownstreamClient;
import com.example.uawsdddemo.client.INeedDocumentWorkOrderSubmission;
import com.example.uawsdddemo.exception.BadRequestException;
import com.example.uawsdddemo.model.dto.CreateINeedDocumentWorkOrderRequest;
import com.example.uawsdddemo.model.dto.INeedDocumentWorkOrderResponse;
import com.example.uawsdddemo.model.entity.INeedDocumentWorkOrder;
import com.example.uawsdddemo.model.enums.INeedDocumentRequestType;
import com.example.uawsdddemo.repository.INeedDocumentWorkOrderRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

@Service
public class INeedDocumentWorkOrderService {

    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");

    private final INeedDocumentWorkOrderRepository repository;
    private final INeedDocumentDownstreamClient downstreamClient;

    public INeedDocumentWorkOrderService(
            INeedDocumentWorkOrderRepository repository,
            INeedDocumentDownstreamClient downstreamClient) {
        this.repository = repository;
        this.downstreamClient = downstreamClient;
    }

    public INeedDocumentWorkOrderResponse create(CreateINeedDocumentWorkOrderRequest request) {
        INeedDocumentRequestType requestType = validateRequestType(request.getRequestType());
        List<String> documentTypes = normalizeDocumentTypes(request.getDocumentTypes());
        String deliveryEmail = normalizeDeliveryEmail(requestType, request.getDeliveryEmail());

        INeedDocumentWorkOrderSubmission submission = new INeedDocumentWorkOrderSubmission(
                request.getPolicyNo(),
                request.getCustomerName(),
                requestType,
                documentTypes,
                deliveryEmail,
                request.getRequester());
        String downstreamSubmissionId = downstreamClient.submit(submission);

        INeedDocumentWorkOrder workOrder = INeedDocumentWorkOrder.submitted(
                request.getPolicyNo(),
                request.getCustomerName(),
                requestType,
                documentTypes,
                deliveryEmail,
                request.getRequester(),
                downstreamSubmissionId);

        return toResponse(repository.save(workOrder));
    }

    private INeedDocumentRequestType validateRequestType(INeedDocumentRequestType requestType) {
        if (requestType == null) {
            throw new BadRequestException("requestType is required");
        }
        return requestType;
    }

    private List<String> normalizeDocumentTypes(List<String> documentTypes) {
        if (documentTypes == null || documentTypes.isEmpty()) {
            throw new BadRequestException("documentTypes must not be empty");
        }

        List<String> normalized = new ArrayList<>();
        for (String documentType : documentTypes) {
            if (documentType == null || documentType.trim().isEmpty()) {
                throw new BadRequestException("documentTypes must not contain blank value");
            }
            normalized.add(documentType.trim());
        }
        return normalized;
    }

    private String normalizeDeliveryEmail(INeedDocumentRequestType requestType, String deliveryEmail) {
        if (requestType != INeedDocumentRequestType.SEND_DOCUMENT) {
            return null;
        }

        if (deliveryEmail == null || deliveryEmail.trim().isEmpty()) {
            throw new BadRequestException("deliveryEmail is required for SEND_DOCUMENT");
        }

        String normalizedEmail = deliveryEmail.trim().toLowerCase(Locale.ROOT);
        if (!EMAIL_PATTERN.matcher(normalizedEmail).matches()) {
            throw new BadRequestException("deliveryEmail must be a valid email");
        }
        return normalizedEmail;
    }

    private INeedDocumentWorkOrderResponse toResponse(INeedDocumentWorkOrder workOrder) {
        INeedDocumentWorkOrderResponse response = new INeedDocumentWorkOrderResponse();
        response.setWorkOrderId(workOrder.getWorkOrderId());
        response.setPolicyNo(workOrder.getPolicyNo());
        response.setCustomerName(workOrder.getCustomerName());
        response.setRequestType(workOrder.getRequestType());
        response.setDocumentTypes(workOrder.getDocumentTypes());
        response.setDeliveryEmail(workOrder.getDeliveryEmail());
        response.setDownstreamSubmissionId(workOrder.getDownstreamSubmissionId());
        response.setRequester(workOrder.getRequester());
        response.setStatus(workOrder.getStatus());
        response.setCreatedAt(workOrder.getCreatedAt());
        return response;
    }
}
