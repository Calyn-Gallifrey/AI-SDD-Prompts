package com.example.uawsdddemo.client;

import org.springframework.stereotype.Component;

import java.util.UUID;

@Component
public class InMemoryINeedDocumentDownstreamClient implements INeedDocumentDownstreamClient {

    @Override
    public String submit(INeedDocumentWorkOrderSubmission submission) {
        return "DOC-" + UUID.randomUUID();
    }
}
