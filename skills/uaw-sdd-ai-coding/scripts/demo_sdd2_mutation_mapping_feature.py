#!/usr/bin/env python3
"""在隔离 Git 仓库中预演新增、修改、字段映射与并发控制型 SDD2.0 功能。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Any, Iterable

from demo_sdd2_large_feature import (
    expect_control_failure,
    git_path,
    phase_review,
    read_json,
    read_jsonl,
    require,
    resume_action,
    write_source,
)
from demo_sdd2_small_feature import (
    CONTROL,
    DEMO_SOURCE,
    ROOT,
    DemoFailure,
    approve_demo,
    git,
    record,
    run_control,
    write_asset,
)


FEATURE_RELATIVE = Path(
    "sdd2-features/MutationDemoSprint/policy-contact-change-draft"
)
MAIN_PACKAGE = Path(
    "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/contactdraft"
)
TEST_PACKAGE = Path(
    "uaw-sdd-demo/src/test/java/com/example/uawsdddemo/contactdraft"
)
CONFLICT_EXCEPTION = Path(
    "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/exception/"
    "ConflictException.java"
)
EXCEPTION_HANDLER = Path(
    "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/handler/"
    "ApiExceptionHandler.java"
)
OUTSIDE_SCOPE_FILE = Path(
    "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/"
    "PolicyBeneficiaryChangeWorkOrderController.java"
)

PHASE_CONTRACT = "Phase1-定义新增修改契约与字段映射"
PHASE_DOMAIN = "Phase2-实现草稿实体与并发仓储"
PHASE_SERVICE = "Phase3-实现幂等创建与乐观版本修改"
PHASE_API = "Phase4-实现接口与冲突响应"


def java_bean_source(
    class_name: str,
    fields: Iterable[tuple[str, str, tuple[str, ...]]],
    *,
    imports: Iterable[str] = (),
) -> str:
    field_list = list(fields)
    import_lines = "\n".join(f"import {value};" for value in imports)
    declarations: list[str] = []
    methods: list[str] = []
    for field_type, field_name, annotations in field_list:
        declarations.extend(f"    {annotation}" for annotation in annotations)
        declarations.append(f"    private {field_type} {field_name};")
        suffix = field_name[0].upper() + field_name[1:]
        methods.extend(
            [
                f"    public {field_type} get{suffix}() {{",
                f"        return {field_name};",
                "    }",
                "",
                f"    public void set{suffix}({field_type} {field_name}) {{",
                f"        this.{field_name} = {field_name};",
                "    }",
                "",
            ]
        )
    body = "\n".join(declarations)
    method_body = "\n".join(methods).rstrip()
    imports_block = f"\n{import_lines}\n" if import_lines else "\n"
    return (
        "package com.example.uawsdddemo.contactdraft;\n"
        f"{imports_block}\n"
        f"public class {class_name} {{\n\n"
        f"{body}\n\n"
        f"{method_body}\n"
        "}\n"
    )


def immutable_value_source(
    class_name: str,
    fields: Iterable[tuple[str, str]],
) -> str:
    field_list = list(fields)
    declarations = "\n".join(
        f"    private final {field_type} {field_name};"
        for field_type, field_name in field_list
    )
    parameters = ",\n".join(
        f"            {field_type} {field_name}"
        for field_type, field_name in field_list
    )
    assignments = "\n".join(
        f"        this.{field_name} = {field_name};"
        for _, field_name in field_list
    )
    methods: list[str] = []
    for field_type, field_name in field_list:
        suffix = field_name[0].upper() + field_name[1:]
        methods.extend(
            [
                f"    public {field_type} get{suffix}() {{",
                f"        return {field_name};",
                "    }",
                "",
            ]
        )
    method_body = "\n".join(methods).rstrip()
    return (
        "package com.example.uawsdddemo.contactdraft;\n\n"
        f"public final class {class_name} {{\n\n"
        f"{declarations}\n\n"
        f"    public {class_name}(\n"
        f"{parameters}) {{\n"
        f"{assignments}\n"
        "    }\n\n"
        f"{method_body}\n"
        "}\n"
    )


def create_request_source() -> str:
    return java_bean_source(
        "CreatePolicyContactDraftRequest",
        (
            ("String", "clientRequestId", ("@NotBlank",)),
            ("String", "policyNumber", ("@NotBlank",)),
            ("String", "customerId", ("@NotBlank",)),
            ("String", "email", ()),
            ("String", "mobile", ()),
            ("String", "operatorId", ("@NotBlank",)),
        ),
        imports=("javax.validation.constraints.NotBlank",),
    )


def update_request_source() -> str:
    return java_bean_source(
        "UpdatePolicyContactDraftRequest",
        (
            ("Long", "expectedVersion", ("@NotNull", "@Min(0)")),
            ("String", "email", ()),
            ("String", "mobile", ()),
            ("String", "operatorId", ("@NotBlank",)),
        ),
        imports=(
            "javax.validation.constraints.Min",
            "javax.validation.constraints.NotBlank",
            "javax.validation.constraints.NotNull",
        ),
    )


def response_source() -> str:
    return java_bean_source(
        "PolicyContactDraftResponse",
        (
            ("String", "workOrderId", ()),
            ("String", "clientRequestId", ()),
            ("String", "policyNumber", ()),
            ("String", "customerId", ()),
            ("String", "maskedEmail", ()),
            ("String", "maskedMobile", ()),
            ("PolicyContactDraftStatus", "status", ()),
            ("long", "version", ()),
            ("String", "lastModifiedBy", ()),
            ("Instant", "createdAt", ()),
            ("Instant", "updatedAt", ()),
        ),
        imports=("java.time.Instant",),
    )


def create_command_source() -> str:
    return immutable_value_source(
        "CreatePolicyContactDraftCommand",
        (
            ("String", "idempotencyKey"),
            ("String", "policyNo"),
            ("String", "partyId"),
            ("String", "newEmail"),
            ("String", "newMobile"),
            ("String", "actor"),
        ),
    )


def update_command_source() -> str:
    return immutable_value_source(
        "UpdatePolicyContactDraftCommand",
        (
            ("long", "expectedVersion"),
            ("String", "newEmail"),
            ("String", "newMobile"),
            ("String", "actor"),
        ),
    )


def status_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        public enum PolicyContactDraftStatus {
            DRAFT,
            SUBMITTED
        }
    """


def entity_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import java.time.Instant;
        import java.util.Objects;
        import java.util.UUID;

        public final class PolicyContactChangeDraft {
            private final String workOrderId;
            private final String requestReference;
            private final String policyNo;
            private final String partyId;
            private final String email;
            private final String mobile;
            private final PolicyContactDraftStatus status;
            private final long version;
            private final String createdBy;
            private final String updatedBy;
            private final Instant createdAt;
            private final Instant updatedAt;

            public PolicyContactChangeDraft(
                    String workOrderId,
                    String requestReference,
                    String policyNo,
                    String partyId,
                    String email,
                    String mobile,
                    PolicyContactDraftStatus status,
                    long version,
                    String createdBy,
                    String updatedBy,
                    Instant createdAt,
                    Instant updatedAt) {
                this.workOrderId = workOrderId;
                this.requestReference = requestReference;
                this.policyNo = policyNo;
                this.partyId = partyId;
                this.email = email;
                this.mobile = mobile;
                this.status = status;
                this.version = version;
                this.createdBy = createdBy;
                this.updatedBy = updatedBy;
                this.createdAt = createdAt;
                this.updatedAt = updatedAt;
            }

            public static PolicyContactChangeDraft create(
                    CreatePolicyContactDraftCommand command,
                    Instant now) {
                return new PolicyContactChangeDraft(
                        UUID.randomUUID().toString(),
                        command.getIdempotencyKey(),
                        command.getPolicyNo(),
                        command.getPartyId(),
                        command.getNewEmail(),
                        command.getNewMobile(),
                        PolicyContactDraftStatus.DRAFT,
                        0L,
                        command.getActor(),
                        command.getActor(),
                        now,
                        now);
            }

            public PolicyContactChangeDraft update(
                    UpdatePolicyContactDraftCommand command,
                    Instant now) {
                return new PolicyContactChangeDraft(
                        workOrderId,
                        requestReference,
                        policyNo,
                        partyId,
                        command.getNewEmail(),
                        command.getNewMobile(),
                        status,
                        version + 1L,
                        createdBy,
                        command.getActor(),
                        createdAt,
                        now);
            }

            public PolicyContactChangeDraft submit(String actor, Instant now) {
                return new PolicyContactChangeDraft(
                        workOrderId,
                        requestReference,
                        policyNo,
                        partyId,
                        email,
                        mobile,
                        PolicyContactDraftStatus.SUBMITTED,
                        version + 1L,
                        createdBy,
                        actor,
                        createdAt,
                        now);
            }

            public boolean hasSameCreatePayload(
                    CreatePolicyContactDraftCommand command) {
                return Objects.equals(requestReference, command.getIdempotencyKey())
                        && Objects.equals(policyNo, command.getPolicyNo())
                        && Objects.equals(partyId, command.getPartyId())
                        && Objects.equals(email, command.getNewEmail())
                        && Objects.equals(mobile, command.getNewMobile())
                        && Objects.equals(createdBy, command.getActor());
            }

            public boolean hasSameContacts(
                    UpdatePolicyContactDraftCommand command) {
                return Objects.equals(email, command.getNewEmail())
                        && Objects.equals(mobile, command.getNewMobile());
            }

            public String getWorkOrderId() {
                return workOrderId;
            }

            public String getRequestReference() {
                return requestReference;
            }

            public String getPolicyNo() {
                return policyNo;
            }

            public String getPartyId() {
                return partyId;
            }

            public String getEmail() {
                return email;
            }

            public String getMobile() {
                return mobile;
            }

            public PolicyContactDraftStatus getStatus() {
                return status;
            }

            public long getVersion() {
                return version;
            }

            public String getCreatedBy() {
                return createdBy;
            }

            public String getUpdatedBy() {
                return updatedBy;
            }

            public Instant getCreatedAt() {
                return createdAt;
            }

            public Instant getUpdatedAt() {
                return updatedAt;
            }
        }
    """


def repository_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import java.util.Optional;

        public interface PolicyContactDraftRepository {
            PolicyContactChangeDraft createOrGet(
                    PolicyContactChangeDraft candidate);

            Optional<PolicyContactChangeDraft> findById(String workOrderId);

            boolean replaceIfVersion(
                    PolicyContactChangeDraft updated,
                    long expectedVersion);
        }
    """


def in_memory_repository_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import org.springframework.stereotype.Repository;

        import java.util.HashMap;
        import java.util.Map;
        import java.util.Optional;

        @Repository
        public class InMemoryPolicyContactDraftRepository
                implements PolicyContactDraftRepository {
            private final Map<String, PolicyContactChangeDraft> byId =
                    new HashMap<>();
            private final Map<String, String> idByRequestReference =
                    new HashMap<>();

            @Override
            public synchronized PolicyContactChangeDraft createOrGet(
                    PolicyContactChangeDraft candidate) {
                String existingId = idByRequestReference.get(
                        candidate.getRequestReference());
                if (existingId != null) {
                    return byId.get(existingId);
                }
                byId.put(candidate.getWorkOrderId(), candidate);
                idByRequestReference.put(
                        candidate.getRequestReference(),
                        candidate.getWorkOrderId());
                return candidate;
            }

            @Override
            public synchronized Optional<PolicyContactChangeDraft> findById(
                    String workOrderId) {
                return Optional.ofNullable(byId.get(workOrderId));
            }

            @Override
            public synchronized boolean replaceIfVersion(
                    PolicyContactChangeDraft updated,
                    long expectedVersion) {
                PolicyContactChangeDraft current =
                        byId.get(updated.getWorkOrderId());
                if (current == null
                        || current.getVersion() != expectedVersion
                        || !current.getRequestReference().equals(
                                updated.getRequestReference())) {
                    return false;
                }
                byId.put(updated.getWorkOrderId(), updated);
                return true;
            }
        }
    """


def mapper_source(
    *,
    fixed_alias_mapping: bool,
    fixed_mobile_mask: bool,
) -> str:
    policy_value = (
        "normalizeRequired(request.getPolicyNumber())"
        if fixed_alias_mapping
        else "normalizeRequired(request.getCustomerId())"
    )
    party_value = (
        "normalizeRequired(request.getCustomerId())"
        if fixed_alias_mapping
        else "normalizeRequired(request.getPolicyNumber())"
    )
    mobile_mask = (
        """
                int suffixStart = mobile.length() - 4;
                int desiredPrefix = mobile.startsWith("+86") ? 6 : 3;
                int prefixLength = Math.min(desiredPrefix, suffixStart);
                return mobile.substring(0, prefixLength)
                        + "****"
                        + mobile.substring(suffixStart);
        """
        if fixed_mobile_mask
        else """
                return mobile;
        """
    )
    source = """
        package com.example.uawsdddemo.contactdraft;

        import org.springframework.stereotype.Component;

        import java.util.Locale;

        @Component
        public class PolicyContactDraftMapper {

            public CreatePolicyContactDraftCommand toCreateCommand(
                    CreatePolicyContactDraftRequest request) {
                return new CreatePolicyContactDraftCommand(
                        normalizeRequired(request.getClientRequestId()),
                        __POLICY_VALUE__,
                        __PARTY_VALUE__,
                        normalizeEmail(request.getEmail()),
                        normalizeMobile(request.getMobile()),
                        normalizeRequired(request.getOperatorId()));
            }

            public UpdatePolicyContactDraftCommand toUpdateCommand(
                    UpdatePolicyContactDraftRequest request) {
                return new UpdatePolicyContactDraftCommand(
                        request.getExpectedVersion().longValue(),
                        normalizeEmail(request.getEmail()),
                        normalizeMobile(request.getMobile()),
                        normalizeRequired(request.getOperatorId()));
            }

            public PolicyContactDraftResponse toResponse(
                    PolicyContactChangeDraft draft) {
                PolicyContactDraftResponse response =
                        new PolicyContactDraftResponse();
                response.setWorkOrderId(draft.getWorkOrderId());
                response.setClientRequestId(draft.getRequestReference());
                response.setPolicyNumber(draft.getPolicyNo());
                response.setCustomerId(draft.getPartyId());
                response.setMaskedEmail(maskEmail(draft.getEmail()));
                response.setMaskedMobile(maskMobile(draft.getMobile()));
                response.setStatus(draft.getStatus());
                response.setVersion(draft.getVersion());
                response.setLastModifiedBy(draft.getUpdatedBy());
                response.setCreatedAt(draft.getCreatedAt());
                response.setUpdatedAt(draft.getUpdatedAt());
                return response;
            }

            private String normalizeRequired(String value) {
                return value == null ? null : value.trim();
            }

            private String normalizeEmail(String value) {
                String normalized = normalizeOptional(value);
                return normalized == null
                        ? null
                        : normalized.toLowerCase(Locale.ROOT);
            }

            private String normalizeMobile(String value) {
                String normalized = normalizeOptional(value);
                return normalized == null
                        ? null
                        : normalized.replaceAll("[\\\\s()\\\\-]", "");
            }

            private String normalizeOptional(String value) {
                if (value == null) {
                    return null;
                }
                String trimmed = value.trim();
                return trimmed.isEmpty() ? null : trimmed;
            }

            private String maskEmail(String email) {
                if (email == null) {
                    return null;
                }
                int at = email.indexOf('@');
                if (at <= 0) {
                    return "***";
                }
                return email.substring(0, 1) + "***" + email.substring(at);
            }

            private String maskMobile(String mobile) {
                if (mobile == null) {
                    return null;
                }
                if (mobile.length() <= 7) {
                    return "****";
                }
        __MOBILE_MASK__
            }
        }
    """
    return (
        source.replace("__POLICY_VALUE__", policy_value)
        .replace("__PARTY_VALUE__", party_value)
        .replace("__MOBILE_MASK__", dedent(mobile_mask).strip())
    )


def service_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import com.example.uawsdddemo.exception.BadRequestException;
        import com.example.uawsdddemo.exception.ConflictException;
        import com.example.uawsdddemo.exception.NotFoundException;
        import org.springframework.stereotype.Service;

        import java.time.Instant;

        @Service
        public class PolicyContactDraftService {
            private final PolicyContactDraftRepository repository;
            private final PolicyContactDraftMapper mapper;

            public PolicyContactDraftService(
                    PolicyContactDraftRepository repository,
                    PolicyContactDraftMapper mapper) {
                this.repository = repository;
                this.mapper = mapper;
            }

            public PolicyContactDraftResponse create(
                    CreatePolicyContactDraftRequest request) {
                CreatePolicyContactDraftCommand command =
                        mapper.toCreateCommand(request);
                validateContacts(command.getNewEmail(), command.getNewMobile());
                PolicyContactChangeDraft candidate =
                        PolicyContactChangeDraft.create(command, Instant.now());
                PolicyContactChangeDraft persisted =
                        repository.createOrGet(candidate);
                if (!persisted.hasSameCreatePayload(command)) {
                    throw new ConflictException(
                            "clientRequestId has already been used "
                                    + "with a different payload");
                }
                return mapper.toResponse(persisted);
            }

            public PolicyContactDraftResponse update(
                    String workOrderId,
                    UpdatePolicyContactDraftRequest request) {
                if (request.getExpectedVersion() == null) {
                    throw new BadRequestException(
                            "expectedVersion is required");
                }
                UpdatePolicyContactDraftCommand command =
                        mapper.toUpdateCommand(request);
                validateContacts(command.getNewEmail(), command.getNewMobile());
                PolicyContactChangeDraft current = repository
                        .findById(workOrderId)
                        .orElseThrow(() -> new NotFoundException(
                                "policy contact change draft not found"));
                if (current.getStatus() != PolicyContactDraftStatus.DRAFT) {
                    throw new ConflictException(
                            "only a DRAFT work order can be updated");
                }
                if (current.getVersion() != command.getExpectedVersion()) {
                    throw new ConflictException(
                            "expectedVersion does not match current version");
                }
                if (current.hasSameContacts(command)) {
                    throw new BadRequestException(
                            "contact update does not contain any change");
                }
                PolicyContactChangeDraft updated =
                        current.update(command, Instant.now());
                if (!repository.replaceIfVersion(
                        updated,
                        command.getExpectedVersion())) {
                    throw new ConflictException(
                            "work order was modified concurrently");
                }
                return mapper.toResponse(updated);
            }

            public PolicyContactDraftResponse get(String workOrderId) {
                return mapper.toResponse(repository
                        .findById(workOrderId)
                        .orElseThrow(() -> new NotFoundException(
                                "policy contact change draft not found")));
            }

            private void validateContacts(String email, String mobile) {
                if (email == null && mobile == null) {
                    throw new BadRequestException(
                            "email or mobile must be provided");
                }
                if (email != null
                        && (email.indexOf('@') <= 0
                        || email.endsWith("@"))) {
                    throw new BadRequestException("email format is invalid");
                }
                if (mobile != null
                        && !mobile.matches("\\\\+?[0-9]{8,15}")) {
                    throw new BadRequestException("mobile format is invalid");
                }
            }
        }
    """


def controller_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import javax.validation.Valid;
        import org.springframework.http.HttpStatus;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PathVariable;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.PutMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.ResponseStatus;
        import org.springframework.web.bind.annotation.RestController;

        @RestController
        @RequestMapping("/api/work-orders/policy-contact-change-drafts")
        public class PolicyContactDraftController {
            private final PolicyContactDraftService service;

            public PolicyContactDraftController(
                    PolicyContactDraftService service) {
                this.service = service;
            }

            @PostMapping
            @ResponseStatus(HttpStatus.CREATED)
            public PolicyContactDraftResponse create(
                    @Valid @RequestBody
                    CreatePolicyContactDraftRequest request) {
                return service.create(request);
            }

            @PutMapping("/{workOrderId}")
            public PolicyContactDraftResponse update(
                    @PathVariable String workOrderId,
                    @Valid @RequestBody
                    UpdatePolicyContactDraftRequest request) {
                return service.update(workOrderId, request);
            }

            @GetMapping("/{workOrderId}")
            public PolicyContactDraftResponse get(
                    @PathVariable String workOrderId) {
                return service.get(workOrderId);
            }
        }
    """


def conflict_exception_source() -> str:
    return """
        package com.example.uawsdddemo.exception;

        public class ConflictException extends RuntimeException {

            public ConflictException(String message) {
                super(message);
            }
        }
    """


def exception_handler_source() -> str:
    return """
        package com.example.uawsdddemo.handler;

        import com.example.uawsdddemo.exception.BadRequestException;
        import com.example.uawsdddemo.exception.ConflictException;
        import com.example.uawsdddemo.exception.NotFoundException;
        import org.springframework.http.HttpStatus;
        import org.springframework.http.ResponseEntity;
        import org.springframework.web.bind.MethodArgumentNotValidException;
        import org.springframework.web.bind.annotation.ExceptionHandler;
        import org.springframework.web.bind.annotation.RestControllerAdvice;

        import java.util.LinkedHashMap;
        import java.util.Map;

        @RestControllerAdvice
        public class ApiExceptionHandler {

            @ExceptionHandler(BadRequestException.class)
            public ResponseEntity<Map<String, String>> handleBadRequest(
                    BadRequestException exception) {
                return ResponseEntity.badRequest()
                        .body(errorBody(exception.getMessage()));
            }

            @ExceptionHandler(MethodArgumentNotValidException.class)
            public ResponseEntity<Map<String, String>> handleValidation(
                    MethodArgumentNotValidException exception) {
                return ResponseEntity.badRequest()
                        .body(errorBody("request validation failed"));
            }

            @ExceptionHandler(NotFoundException.class)
            public ResponseEntity<Map<String, String>> handleNotFound(
                    NotFoundException exception) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(errorBody(exception.getMessage()));
            }

            @ExceptionHandler(ConflictException.class)
            public ResponseEntity<Map<String, String>> handleConflict(
                    ConflictException exception) {
                return ResponseEntity.status(HttpStatus.CONFLICT)
                        .body(errorBody(exception.getMessage()));
            }

            private Map<String, String> errorBody(String message) {
                Map<String, String> body = new LinkedHashMap<>();
                body.put("message", message);
                return body;
            }
        }
    """


def write_contract_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "CreatePolicyContactDraftRequest.java",
            create_request_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "UpdatePolicyContactDraftRequest.java",
            update_request_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftResponse.java",
            response_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "CreatePolicyContactDraftCommand.java",
            create_command_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "UpdatePolicyContactDraftCommand.java",
            update_command_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftStatus.java",
            status_source(),
        ),
    ]


def write_domain_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeDraft.java",
            entity_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftRepository.java",
            repository_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "InMemoryPolicyContactDraftRepository.java",
            in_memory_repository_source(),
        ),
    ]


def write_service_phase(
    repo: Path,
    *,
    fixed_alias_mapping: bool,
    fixed_mobile_mask: bool,
) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftMapper.java",
            mapper_source(
                fixed_alias_mapping=fixed_alias_mapping,
                fixed_mobile_mask=fixed_mobile_mask,
            ),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftService.java",
            service_source(),
        ),
    ]


def write_api_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftController.java",
            controller_source(),
        ),
        write_source(
            repo,
            CONFLICT_EXCEPTION,
            conflict_exception_source(),
        ),
        write_source(
            repo,
            EXCEPTION_HANDLER,
            exception_handler_source(),
        ),
    ]


def mapper_test_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import org.junit.Test;

        import java.time.Instant;

        import static org.junit.Assert.assertEquals;
        import static org.junit.Assert.assertNull;

        public class PolicyContactDraftMapperTest {
            private final PolicyContactDraftMapper mapper =
                    new PolicyContactDraftMapper();

            @Test
            public void testCreateMapping_allAliasesAndNormalization_areExact() {
                CreatePolicyContactDraftRequest request = createRequest();

                CreatePolicyContactDraftCommand command =
                        mapper.toCreateCommand(request);

                assertEquals("REQ-9001", command.getIdempotencyKey());
                assertEquals("POL-10001", command.getPolicyNo());
                assertEquals("CUS-70001", command.getPartyId());
                assertEquals("alice@example.com", command.getNewEmail());
                assertEquals("+8613800008000", command.getNewMobile());
                assertEquals("operator-a", command.getActor());
            }

            @Test
            public void testUpdateMapping_versionContactsAndActor_areExact() {
                UpdatePolicyContactDraftRequest request =
                        new UpdatePolicyContactDraftRequest();
                request.setExpectedVersion(7L);
                request.setEmail(" NEW@EXAMPLE.COM ");
                request.setMobile("139-0000-9000");
                request.setOperatorId(" operator-b ");

                UpdatePolicyContactDraftCommand command =
                        mapper.toUpdateCommand(request);

                assertEquals(7L, command.getExpectedVersion());
                assertEquals("new@example.com", command.getNewEmail());
                assertEquals("13900009000", command.getNewMobile());
                assertEquals("operator-b", command.getActor());
            }

            @Test
            public void testResponseMapping_aliasesAndSensitiveValues_areMasked() {
                CreatePolicyContactDraftCommand command =
                        mapper.toCreateCommand(createRequest());
                PolicyContactChangeDraft draft =
                        PolicyContactChangeDraft.create(
                                command,
                                Instant.parse("2026-07-31T08:00:00Z"));

                PolicyContactDraftResponse response =
                        mapper.toResponse(draft);

                assertEquals(draft.getWorkOrderId(), response.getWorkOrderId());
                assertEquals("REQ-9001", response.getClientRequestId());
                assertEquals("POL-10001", response.getPolicyNumber());
                assertEquals("CUS-70001", response.getCustomerId());
                assertEquals("a***@example.com", response.getMaskedEmail());
                assertEquals("+86138****8000", response.getMaskedMobile());
                assertEquals("operator-a", response.getLastModifiedBy());
            }

            @Test
            public void testOptionalContacts_blankValues_becomeNull() {
                CreatePolicyContactDraftRequest request = createRequest();
                request.setEmail(" ");
                request.setMobile(null);

                CreatePolicyContactDraftCommand command =
                        mapper.toCreateCommand(request);

                assertNull(command.getNewEmail());
                assertNull(command.getNewMobile());
            }

            private CreatePolicyContactDraftRequest createRequest() {
                CreatePolicyContactDraftRequest request =
                        new CreatePolicyContactDraftRequest();
                request.setClientRequestId(" REQ-9001 ");
                request.setPolicyNumber(" POL-10001 ");
                request.setCustomerId(" CUS-70001 ");
                request.setEmail(" Alice@Example.COM ");
                request.setMobile(" +86 138-0000-8000 ");
                request.setOperatorId(" operator-a ");
                return request;
            }
        }
    """


def repository_test_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import org.junit.Test;

        import java.time.Instant;

        import static org.junit.Assert.assertEquals;
        import static org.junit.Assert.assertFalse;
        import static org.junit.Assert.assertSame;
        import static org.junit.Assert.assertTrue;

        public class InMemoryPolicyContactDraftRepositoryTest {

            @Test
            public void testCreateOrGet_sameRequestReference_preservesFirst() {
                InMemoryPolicyContactDraftRepository repository =
                        new InMemoryPolicyContactDraftRepository();
                PolicyContactChangeDraft first = draft("REQ-1", "P-1");
                PolicyContactChangeDraft conflicting = draft("REQ-1", "P-2");

                PolicyContactChangeDraft storedFirst =
                        repository.createOrGet(first);
                PolicyContactChangeDraft storedAgain =
                        repository.createOrGet(conflicting);

                assertSame(first, storedFirst);
                assertSame(first, storedAgain);
                assertEquals(
                        "P-1",
                        repository.findById(first.getWorkOrderId())
                                .get()
                                .getPolicyNo());
            }

            @Test
            public void testReplaceIfVersion_matchingVersion_replacesAtomically() {
                InMemoryPolicyContactDraftRepository repository =
                        new InMemoryPolicyContactDraftRepository();
                PolicyContactChangeDraft current = draft("REQ-2", "P-2");
                repository.createOrGet(current);
                UpdatePolicyContactDraftCommand update =
                        new UpdatePolicyContactDraftCommand(
                                0L,
                                "new@example.com",
                                "13900009000",
                                "operator-b");
                PolicyContactChangeDraft changed =
                        current.update(update, Instant.now());

                boolean replaced =
                        repository.replaceIfVersion(changed, 0L);

                assertTrue(replaced);
                assertEquals(
                        1L,
                        repository.findById(current.getWorkOrderId())
                                .get()
                                .getVersion());
            }

            @Test
            public void testReplaceIfVersion_staleVersion_keepsCurrent() {
                InMemoryPolicyContactDraftRepository repository =
                        new InMemoryPolicyContactDraftRepository();
                PolicyContactChangeDraft current = draft("REQ-3", "P-3");
                repository.createOrGet(current);
                UpdatePolicyContactDraftCommand update =
                        new UpdatePolicyContactDraftCommand(
                                0L,
                                "new@example.com",
                                "13900009000",
                                "operator-b");
                PolicyContactChangeDraft changed =
                        current.update(update, Instant.now());

                boolean replaced =
                        repository.replaceIfVersion(changed, 9L);

                assertFalse(replaced);
                assertEquals(
                        0L,
                        repository.findById(current.getWorkOrderId())
                                .get()
                                .getVersion());
            }

            private PolicyContactChangeDraft draft(
                    String requestReference,
                    String policyNo) {
                return PolicyContactChangeDraft.create(
                        new CreatePolicyContactDraftCommand(
                                requestReference,
                                policyNo,
                                "CUS-1",
                                "old@example.com",
                                "13800008000",
                                "operator-a"),
                        Instant.now());
            }
        }
    """


def service_test_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import com.example.uawsdddemo.exception.BadRequestException;
        import com.example.uawsdddemo.exception.ConflictException;
        import com.example.uawsdddemo.exception.NotFoundException;
        import org.junit.Before;
        import org.junit.Test;

        import java.time.Instant;

        import static org.junit.Assert.assertEquals;
        import static org.junit.Assert.assertNotNull;
        import static org.junit.Assert.assertThrows;
        import static org.junit.Assert.assertTrue;

        public class PolicyContactDraftServiceTest {
            private InMemoryPolicyContactDraftRepository repository;
            private PolicyContactDraftService service;

            @Before
            public void setUp() {
                repository = new InMemoryPolicyContactDraftRepository();
                service = new PolicyContactDraftService(
                        repository,
                        new PolicyContactDraftMapper());
            }

            @Test
            public void testCreate_validRequest_returnsDraftVersionZero() {
                PolicyContactDraftResponse response =
                        service.create(createRequest());

                assertNotNull(response.getWorkOrderId());
                assertEquals("POL-10001", response.getPolicyNumber());
                assertEquals("CUS-70001", response.getCustomerId());
                assertEquals(
                        PolicyContactDraftStatus.DRAFT,
                        response.getStatus());
                assertEquals(0L, response.getVersion());
                assertEquals(
                        "a***@example.com",
                        response.getMaskedEmail());
            }

            @Test
            public void testCreate_sameIdempotentPayload_returnsSameWorkOrder() {
                PolicyContactDraftResponse first =
                        service.create(createRequest());
                PolicyContactDraftResponse second =
                        service.create(createRequest());

                assertEquals(first.getWorkOrderId(), second.getWorkOrderId());
                assertEquals(0L, second.getVersion());
            }

            @Test
            public void testCreate_reusedIdWithDifferentPayload_returnsConflict() {
                service.create(createRequest());
                CreatePolicyContactDraftRequest changed = createRequest();
                changed.setCustomerId("CUS-OTHER");

                ConflictException exception = assertThrows(
                        ConflictException.class,
                        () -> service.create(changed));

                assertTrue(exception.getMessage().contains(
                        "different payload"));
            }

            @Test
            public void testCreate_withoutContact_returnsBadRequest() {
                CreatePolicyContactDraftRequest request = createRequest();
                request.setEmail(" ");
                request.setMobile(null);

                BadRequestException exception = assertThrows(
                        BadRequestException.class,
                        () -> service.create(request));

                assertEquals(
                        "email or mobile must be provided",
                        exception.getMessage());
            }

            @Test
            public void testCreate_invalidMobile_returnsBadRequest() {
                CreatePolicyContactDraftRequest request = createRequest();
                request.setMobile("not-a-mobile");

                BadRequestException exception = assertThrows(
                        BadRequestException.class,
                        () -> service.create(request));

                assertEquals(
                        "mobile format is invalid",
                        exception.getMessage());
            }

            @Test
            public void testUpdate_matchingVersion_changesContactsAndVersion() {
                PolicyContactDraftResponse created =
                        service.create(createRequest());
                UpdatePolicyContactDraftRequest update =
                        updateRequest(created.getVersion());

                PolicyContactDraftResponse changed =
                        service.update(created.getWorkOrderId(), update);

                assertEquals(1L, changed.getVersion());
                assertEquals("operator-b", changed.getLastModifiedBy());
                assertEquals(
                        "n***@example.com",
                        changed.getMaskedEmail());
            }

            @Test
            public void testUpdate_staleVersion_returnsConflict() {
                PolicyContactDraftResponse created =
                        service.create(createRequest());
                UpdatePolicyContactDraftRequest update = updateRequest(9L);

                ConflictException exception = assertThrows(
                        ConflictException.class,
                        () -> service.update(
                                created.getWorkOrderId(),
                                update));

                assertEquals(
                        "expectedVersion does not match current version",
                        exception.getMessage());
            }

            @Test
            public void testUpdate_sameContacts_returnsBadRequest() {
                PolicyContactDraftResponse created =
                        service.create(createRequest());
                UpdatePolicyContactDraftRequest update =
                        new UpdatePolicyContactDraftRequest();
                update.setExpectedVersion(0L);
                update.setEmail("ALICE@EXAMPLE.COM");
                update.setMobile("+86 138-0000-8000");
                update.setOperatorId("operator-b");

                BadRequestException exception = assertThrows(
                        BadRequestException.class,
                        () -> service.update(
                                created.getWorkOrderId(),
                                update));

                assertEquals(
                        "contact update does not contain any change",
                        exception.getMessage());
            }

            @Test
            public void testUpdate_submittedWorkOrder_returnsConflict() {
                PolicyContactDraftResponse created =
                        service.create(createRequest());
                PolicyContactChangeDraft current = repository
                        .findById(created.getWorkOrderId())
                        .get();
                PolicyContactChangeDraft submitted =
                        current.submit("reviewer", Instant.now());
                assertTrue(repository.replaceIfVersion(submitted, 0L));
                UpdatePolicyContactDraftRequest update = updateRequest(1L);

                ConflictException exception = assertThrows(
                        ConflictException.class,
                        () -> service.update(
                                created.getWorkOrderId(),
                                update));

                assertEquals(
                        "only a DRAFT work order can be updated",
                        exception.getMessage());
            }

            @Test
            public void testGet_missingWorkOrder_returnsNotFound() {
                NotFoundException exception = assertThrows(
                        NotFoundException.class,
                        () -> service.get("missing"));

                assertEquals(
                        "policy contact change draft not found",
                        exception.getMessage());
            }

            private CreatePolicyContactDraftRequest createRequest() {
                CreatePolicyContactDraftRequest request =
                        new CreatePolicyContactDraftRequest();
                request.setClientRequestId("REQ-9001");
                request.setPolicyNumber("POL-10001");
                request.setCustomerId("CUS-70001");
                request.setEmail("Alice@Example.com");
                request.setMobile("+86 138-0000-8000");
                request.setOperatorId("operator-a");
                return request;
            }

            private UpdatePolicyContactDraftRequest updateRequest(
                    long version) {
                UpdatePolicyContactDraftRequest request =
                        new UpdatePolicyContactDraftRequest();
                request.setExpectedVersion(version);
                request.setEmail("new@example.com");
                request.setMobile("13900009000");
                request.setOperatorId("operator-b");
                return request;
            }
        }
    """


def controller_test_source() -> str:
    return """
        package com.example.uawsdddemo.contactdraft;

        import com.example.uawsdddemo.exception.ConflictException;
        import com.example.uawsdddemo.handler.ApiExceptionHandler;
        import com.fasterxml.jackson.databind.ObjectMapper;
        import org.hamcrest.Matchers;
        import org.junit.Before;
        import org.junit.Test;
        import org.junit.runner.RunWith;
        import org.mockito.InjectMocks;
        import org.mockito.Mock;
        import org.mockito.Mockito;
        import org.mockito.junit.MockitoJUnitRunner;
        import org.springframework.http.MediaType;
        import org.springframework.test.web.servlet.MockMvc;
        import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
        import org.springframework.test.web.servlet.setup.MockMvcBuilders;

        import java.time.Instant;

        import static org.mockito.ArgumentMatchers.any;
        import static org.mockito.ArgumentMatchers.eq;
        import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
        import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

        @RunWith(MockitoJUnitRunner.class)
        public class PolicyContactDraftControllerTest {
            private final ObjectMapper objectMapper = new ObjectMapper();
            private MockMvc mockMvc;

            @Mock
            private PolicyContactDraftService service;

            @InjectMocks
            private PolicyContactDraftController controller;

            @Before
            public void setUp() {
                mockMvc = MockMvcBuilders.standaloneSetup(controller)
                        .setControllerAdvice(new ApiExceptionHandler())
                        .build();
            }

            @Test
            public void testCreate_validRequest_returnsCreatedMaskedResponse()
                    throws Exception {
                Mockito.when(service.create(
                        any(CreatePolicyContactDraftRequest.class)))
                        .thenReturn(response());

                mockMvc.perform(MockMvcRequestBuilders
                                .post("/api/work-orders/"
                                        + "policy-contact-change-drafts")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(
                                        createRequest())))
                        .andExpect(status().isCreated())
                        .andExpect(jsonPath(
                                "$.workOrderId",
                                Matchers.is("WO-9001")))
                        .andExpect(jsonPath(
                                "$.policyNumber",
                                Matchers.is("POL-10001")))
                        .andExpect(jsonPath(
                                "$.maskedMobile",
                                Matchers.is("138****8000")))
                        .andExpect(jsonPath("$.email").doesNotExist())
                        .andExpect(jsonPath("$.mobile").doesNotExist());
            }

            @Test
            public void testCreate_missingBusinessId_returnsBadRequest()
                    throws Exception {
                CreatePolicyContactDraftRequest request = createRequest();
                request.setClientRequestId("");

                mockMvc.perform(MockMvcRequestBuilders
                                .post("/api/work-orders/"
                                        + "policy-contact-change-drafts")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(
                                        request)))
                        .andExpect(status().isBadRequest())
                        .andExpect(jsonPath(
                                "$.message",
                                Matchers.is(
                                        "request validation failed")));

                Mockito.verifyNoInteractions(service);
            }

            @Test
            public void testUpdate_validRequest_returnsOk()
                    throws Exception {
                Mockito.when(service.update(
                        eq("WO-9001"),
                        any(UpdatePolicyContactDraftRequest.class)))
                        .thenReturn(response());

                mockMvc.perform(MockMvcRequestBuilders
                                .put("/api/work-orders/"
                                        + "policy-contact-change-drafts/"
                                        + "WO-9001")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(
                                        updateRequest())))
                        .andExpect(status().isOk())
                        .andExpect(jsonPath(
                                "$.version",
                                Matchers.is(1)));
            }

            @Test
            public void testUpdate_missingVersion_returnsBadRequest()
                    throws Exception {
                UpdatePolicyContactDraftRequest request = updateRequest();
                request.setExpectedVersion(null);

                mockMvc.perform(MockMvcRequestBuilders
                                .put("/api/work-orders/"
                                        + "policy-contact-change-drafts/"
                                        + "WO-9001")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(
                                        request)))
                        .andExpect(status().isBadRequest())
                        .andExpect(jsonPath(
                                "$.message",
                                Matchers.is(
                                        "request validation failed")));
            }

            @Test
            public void testUpdate_versionConflict_returnsConflict()
                    throws Exception {
                Mockito.when(service.update(
                        eq("WO-9001"),
                        any(UpdatePolicyContactDraftRequest.class)))
                        .thenThrow(new ConflictException(
                                "expectedVersion does not match "
                                        + "current version"));

                mockMvc.perform(MockMvcRequestBuilders
                                .put("/api/work-orders/"
                                        + "policy-contact-change-drafts/"
                                        + "WO-9001")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(
                                        updateRequest())))
                        .andExpect(status().isConflict())
                        .andExpect(jsonPath(
                                "$.message",
                                Matchers.containsString(
                                        "expectedVersion")));
            }

            @Test
            public void testGet_existingDraft_returnsOk()
                    throws Exception {
                Mockito.when(service.get("WO-9001"))
                        .thenReturn(response());

                mockMvc.perform(MockMvcRequestBuilders
                                .get("/api/work-orders/"
                                        + "policy-contact-change-drafts/"
                                        + "WO-9001"))
                        .andExpect(status().isOk())
                        .andExpect(jsonPath(
                                "$.status",
                                Matchers.is("DRAFT")));
            }

            private CreatePolicyContactDraftRequest createRequest() {
                CreatePolicyContactDraftRequest request =
                        new CreatePolicyContactDraftRequest();
                request.setClientRequestId("REQ-9001");
                request.setPolicyNumber("POL-10001");
                request.setCustomerId("CUS-70001");
                request.setEmail("alice@example.com");
                request.setMobile("13800008000");
                request.setOperatorId("operator-a");
                return request;
            }

            private UpdatePolicyContactDraftRequest updateRequest() {
                UpdatePolicyContactDraftRequest request =
                        new UpdatePolicyContactDraftRequest();
                request.setExpectedVersion(0L);
                request.setEmail("new@example.com");
                request.setMobile("13900009000");
                request.setOperatorId("operator-b");
                return request;
            }

            private PolicyContactDraftResponse response() {
                PolicyContactDraftResponse response =
                        new PolicyContactDraftResponse();
                response.setWorkOrderId("WO-9001");
                response.setClientRequestId("REQ-9001");
                response.setPolicyNumber("POL-10001");
                response.setCustomerId("CUS-70001");
                response.setMaskedEmail("a***@example.com");
                response.setMaskedMobile("138****8000");
                response.setStatus(PolicyContactDraftStatus.DRAFT);
                response.setVersion(1L);
                response.setLastModifiedBy("operator-a");
                response.setCreatedAt(
                        Instant.parse("2026-07-31T08:00:00Z"));
                response.setUpdatedAt(
                        Instant.parse("2026-07-31T08:00:00Z"));
                return response;
            }
        }
    """


def write_test_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            TEST_PACKAGE / "PolicyContactDraftMapperTest.java",
            mapper_test_source(),
        ),
        write_source(
            repo,
            TEST_PACKAGE
            / "InMemoryPolicyContactDraftRepositoryTest.java",
            repository_test_source(),
        ),
        write_source(
            repo,
            TEST_PACKAGE / "PolicyContactDraftServiceTest.java",
            service_test_source(),
        ),
        write_source(
            repo,
            TEST_PACKAGE / "PolicyContactDraftControllerTest.java",
            controller_test_source(),
        ),
    ]


def run_feature_tests(repo: Path, feature: Path) -> dict[str, Any]:
    return run_control(
        repo,
        "run-unit-test",
        "--feature-dir",
        str(feature),
        "--cwd",
        ".",
        "--timeout-seconds",
        "600",
        "--",
        "mvn",
        "-f",
        "uaw-sdd-demo/pom.xml",
        (
            "-Dtest=PolicyContactDraftMapperTest,"
            "InMemoryPolicyContactDraftRepositoryTest,"
            "PolicyContactDraftServiceTest,"
            "PolicyContactDraftControllerTest"
        ),
        "test",
    )["result"]


def write_unit_summary(
    feature: Path,
    execution: dict[str, Any],
    *,
    conclusion: str,
) -> None:
    counts = execution["test_counts"]
    write_asset(
        feature,
        "unit-test-summary.md",
        "单元测试总结",
        (
            f"控制器执行证据 SHA-256：`{execution['evidence_sha256']}`。\n\n"
            f"冻结范围 SHA-256：`{execution['scope_sha256']}`。\n\n"
            f"实际执行 {counts['total']} 项测试，通过 {counts['passed']} 项，"
            f"失败 {counts['failed']} 项，Error {counts['errors']} 项，"
            f"跳过 {counts['skipped']} 项。结论：{conclusion}。"
        ),
    )


def main() -> int:
    if shutil.which("java") is None:
        raise DemoFailure(
            "当前环境未检测到 Java。请安装或启用 Java 8 及以上版本，"
            "并正确配置 PATH/JAVA_HOME。"
        )
    if not CONTROL.is_file():
        raise DemoFailure(f"缺少 Java 8 控制器 JAR：{CONTROL}")
    doctor = run_control(
        ROOT,
        "doctor",
        "--repo-root",
        str(ROOT),
    )["result"]
    if doctor["java_specification_version"] != "1.8":
        raise DemoFailure(
            "新增/修改型深度 Demo 必须由真实 Java 8 运行；"
            f"当前版本为 {doctor['java_specification_version']}。"
        )
    if shutil.which("mvn") is None:
        raise DemoFailure("当前环境未安装 Maven，无法执行真实 Java 测试。")

    checks: list[dict[str, Any]] = [
        {
            "检查": "Java 8 实机预检",
            "结果": "已通过",
            "版本": doctor["java_specification_version"],
        }
    ]

    with tempfile.TemporaryDirectory(
        prefix="uaw-sdd2-mutation-mapping-demo-"
    ) as temp:
        workspace = Path(temp)
        repo = workspace / "main"
        remote = workspace / "remote.git"
        shutil.copytree(DEMO_SOURCE, repo / "uaw-sdd-demo")
        git(repo, "init", "-q")
        git(
            repo,
            "config",
            "user.email",
            "sdd2-mutation-demo@example.invalid",
        )
        git(repo, "config", "user.name", "SDD2 Mutation Demo")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "mutation demo baseline")
        baseline_commit_count = int(
            git(repo, "rev-list", "--count", "HEAD")
        )
        subprocess.run(
            ["git", "init", "--bare", "-q", str(remote)],
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        git(repo, "remote", "add", "origin", str(remote))

        feature = repo / FEATURE_RELATIVE
        feature.mkdir(parents=True)
        write_asset(
            feature,
            "brief-design.md",
            "人工简要设计",
            (
                "新增保单联系方式变更草稿的创建、查询和修改接口。"
                "创建必须按 clientRequestId 幂等；相同键不同载荷返回冲突。"
                "修改仅允许 DRAFT 状态并使用 expectedVersion 做乐观并发控制。"
                "API 字段与领域字段必须按映射表转换，邮箱和手机号只能脱敏返回。"
                "实现兼容 Java 8，不新增依赖，不改变既有业务接口。"
            ),
        )
        initial = run_control(
            repo,
            "init",
            "--feature-dir",
            str(feature),
            "--feature-id",
            "policy-contact-change-draft",
            "--mode",
            "demo",
        )["result"]
        require(
            initial["next_required_action"]
            == "assemble-proposal-input",
            "初始化后没有停在 Proposal 输入动作。",
        )
        run_control(
            repo,
            "authorize-demo",
            "--feature-dir",
            str(feature),
            "--authorization-text",
            (
                "用户明确授权运行第二轮新增修改与字段映射型完整 Demo，"
                "并由 Demo 模拟每个阶段的人工审核。"
            ),
            "--message-id",
            "current-user-mutation-demo-request",
        )

        blocked_commit = subprocess.run(
            [
                "git",
                "commit",
                "--allow-empty",
                "--no-verify",
                "-m",
                "forbidden mutation demo commit",
            ],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            blocked_commit.returncode != 0
            and "SDD2_COMMIT_BLOCKED"
            in blocked_commit.stdout + blocked_commit.stderr,
            "活动 Feature 没有阻止 git commit --no-verify。",
        )
        blocked_push = subprocess.run(
            ["git", "push", "origin", "HEAD:refs/heads/main"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            blocked_push.returncode != 0
            and "SDD2_COMMIT_BLOCKED"
            in blocked_push.stdout + blocked_push.stderr,
            "活动 Feature 没有阻止 git push。",
        )
        checks.append(
            {
                "检查": "活动流程自动提交与推送",
                "结果": "commit --no-verify 与 push 均被阻断",
            }
        )

        write_asset(
            feature,
            "proposal-input.md",
            "内部规划输入",
            (
                "目标是在现有 Spring Boot 2.7 / Java 8 Demo 中增加独立"
                " contactdraft 业务链路，并复用统一异常处理。"
                "输入包含客户请求号、保单号、客户号、邮箱、手机号和操作人。"
                "创建返回草稿版本 0；重复相同请求返回原工单；冲突载荷返回 409。"
                "修改使用完整联系方式替换和 expectedVersion，成功后版本加一。"
                "响应不得暴露原始邮箱或手机号。"
            ),
        )
        record(repo, feature, "proposal-input")
        write_asset(
            feature,
            "spec.md",
            "需求规格",
            (
                "提供 POST、PUT 和 GET 三个接口。POST 至少包含一种联系方式，"
                "clientRequestId 对标准化后的完整创建载荷幂等；不同载荷冲突。"
                "PUT 仅允许 DRAFT，expectedVersion 必须等于当前版本，"
                "不得接受无变化修改，成功后版本加一。邮箱转小写，手机号移除"
                "空格、括号和连字符。响应只含 maskedEmail、maskedMobile，"
                "保留 API 标识字段，不得泄漏实体中的原始联系方式。"
            ),
        )
        record(repo, feature, "spec")

        expect_control_failure(
            repo,
            "approve",
            "--feature-dir",
            str(feature),
            "--stage",
            "spec",
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            "同意",
            "--message-id",
            "mutation-ambiguous-spec-approval",
            contains=("ambiguous",),
        )
        write_asset(
            feature,
            "design.md",
            "错误提前设计",
            "该文件用于验证 Spec 未批准时不能提前生成 Design。",
        )
        (feature / "field-mapping-draft.csv").write_text(
            "api,domain\npolicyNumber,policyNo\n",
            encoding="utf-8",
        )
        layout = expect_control_failure(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
            contains=(
                "UNEXPECTED_STAGE_ASSET:design.md",
                "UNEXPECTED_FEATURE_FILE:field-mapping-draft.csv",
            ),
        )
        require(
            layout["result"]["next_required_action"]
            == "remove-unexpected-feature-paths-before-current-action",
            "违规资产没有形成唯一清理动作。",
        )
        (feature / "design.md").unlink()
        (feature / "field-mapping-draft.csv").unlink()
        require(
            resume_action(repo, feature) == "request-spec-approval",
            "清理违规资产后没有返回 Spec 人工 Gate。",
        )
        checks.append(
            {
                "检查": "人工审核与文件生成边界",
                "结果": "模糊批准、提前 Design 和散落映射文件均被拒绝",
            }
        )

        approve_demo(
            repo,
            feature,
            "spec",
            "mutation-spec-approval",
        )
        write_asset(
            feature,
            "design.md",
            "技术设计与字段映射",
            (
                "字段映射唯一依据如下：\n\n"
                "| API 请求/响应 | Command | Entity | 说明 |\n"
                "| --- | --- | --- | --- |\n"
                "| clientRequestId | idempotencyKey | requestReference | 幂等键 |\n"
                "| policyNumber | policyNo | policyNo | 保单标识 |\n"
                "| customerId | partyId | partyId | 客户标识 |\n"
                "| email | newEmail | email | 标准化后存储，脱敏返回 |\n"
                "| mobile | newMobile | mobile | 标准化后存储，脱敏返回 |\n"
                "| operatorId | actor | createdBy/updatedBy | 审计人 |\n"
                "| expectedVersion | expectedVersion | version | 乐观锁 |\n\n"
                "使用不可变实体和同步内存仓储实现 createOrGet 与"
                " replaceIfVersion。Service 负责幂等、状态、版本和格式校验；"
                "Mapper 负责别名、标准化及脱敏；统一异常处理将业务冲突映射为 409。"
            ),
        )
        record(repo, feature, "design")
        approve_demo(
            repo,
            feature,
            "design",
            "mutation-design-approval",
        )
        write_asset(
            feature,
            "tasks.md",
            "实现任务",
            (
                f"{PHASE_CONTRACT}；{PHASE_DOMAIN}；{PHASE_SERVICE}；"
                f"{PHASE_API}。每个 Phase 完成后必须单独审核。"
                "四个生产 Phase 通过后冻结范围并执行 Code Review。"
                "首次 Review 与 Auto-fix 关闭后才允许 Unit Test Skill 生成"
                " Mapper、Repository、Service、Controller 四层测试；"
                "测试写入后必须重新冻结并完整复审，才能执行真实测试。"
            ),
        )
        record(repo, feature, "tasks")
        approve_demo(
            repo,
            feature,
            "tasks",
            "mutation-tasks-approval",
        )

        handler_path = repo / EXCEPTION_HANDLER
        original_handler = handler_path.read_text(encoding="utf-8")
        handler_path.write_text(
            original_handler
            + "\n// 未签发实现许可前的错误提前修改。\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            f"{MAIN_PACKAGE.as_posix()}/**",
            "--required-phase",
            PHASE_CONTRACT,
            contains=("PRE_IMPLEMENTATION_CHANGE",),
        )
        premature_state = read_json(
            feature / ".sdd2/feature-state.json"
        )
        require(
            premature_state["stage_status"] == "blocked"
            and premature_state["blocked"]["code"]
            == "PREMATURE_IMPLEMENTATION_CHANGE",
            "提前修改既有文件没有进入 blocked。",
        )
        handler_path.write_text(original_handler, encoding="utf-8")
        require(
            resume_action(repo, feature)
            == "capture-implementation-scope",
            "恢复提前修改后没有返回实现范围签发动作。",
        )
        checks.append(
            {
                "检查": "许可前修改既有生产文件",
                "结果": "已阻断，恢复后仍停在原实现许可动作",
            }
        )

        scope = run_control(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            f"{MAIN_PACKAGE.as_posix()}/**",
            "--allowed-path",
            CONFLICT_EXCEPTION.as_posix(),
            "--allowed-path",
            EXCEPTION_HANDLER.as_posix(),
            "--allowed-path",
            f"{TEST_PACKAGE.as_posix()}/**",
            "--forbidden-path",
            "uaw-sdd-demo/pom.xml",
            "--forbidden-path",
            "uaw-sdd-demo/README.md",
            "--forbidden-path",
            OUTSIDE_SCOPE_FILE.as_posix(),
            "--required-phase",
            PHASE_CONTRACT,
            "--required-phase",
            PHASE_DOMAIN,
            "--required-phase",
            PHASE_SERVICE,
            "--required-phase",
            PHASE_API,
            "--test-path",
            f"{TEST_PACKAGE.as_posix()}/**",
        )["result"]
        require(
            bool(scope.get("implementation_permit_sha256")),
            "实现范围没有签发哈希绑定许可。",
        )
        require(
            len(scope["allowed_paths"]) == 4
            and len(scope["required_phases"]) == 4,
            "实现范围或 Phase 数量与设计不一致。",
        )
        checks.append(
            {
                "检查": "精确实现范围",
                "结果": "新包、单一共享处理器、异常类与测试目录已显式绑定",
            }
        )

        expect_control_failure(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            PHASE_DOMAIN,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {PHASE_DOMAIN} 阶段",
            "--message-id",
            "mutation-phase-order-attack",
            contains=("order violation",),
        )
        production_files = write_contract_phase(repo)
        phase_review(
            repo,
            feature,
            PHASE_CONTRACT,
            "mutation-phase-contract",
        )
        production_files.extend(write_domain_phase(repo))
        phase_review(
            repo,
            feature,
            PHASE_DOMAIN,
            "mutation-phase-domain",
        )
        production_files.extend(
            write_service_phase(
                repo,
                fixed_alias_mapping=False,
                fixed_mobile_mask=False,
            )
        )
        phase_review(
            repo,
            feature,
            PHASE_SERVICE,
            "mutation-phase-service",
        )
        production_files.extend(write_api_phase(repo))
        phase_review(
            repo,
            feature,
            PHASE_API,
            "mutation-phase-api",
        )
        require(
            len(production_files) == 14,
            f"生产变更文件数量不是十四个：{production_files}",
        )
        checks.append(
            {
                "检查": "四阶段实现顺序",
                "结果": "乱序已拒绝，十四个生产变更文件逐阶段批准",
            }
        )

        outside_path = repo / OUTSIDE_SCOPE_FILE
        original_outside = outside_path.read_text(encoding="utf-8")
        outside_path.write_text(
            original_outside + "\n// 错误修改其他业务模块。\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
            contains=(
                "FORBIDDEN_PATH:"
                + OUTSIDE_SCOPE_FILE.as_posix(),
            ),
        )
        blocked_scope_state = read_json(
            feature / ".sdd2/feature-state.json"
        )
        require(
            blocked_scope_state["blocked"]["code"]
            == "IMPLEMENTATION_SCOPE_VIOLATION",
            "其他业务模块修改没有记录确定性阻塞码。",
        )
        outside_path.write_text(original_outside, encoding="utf-8")
        first_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            first_snapshot["code_revision"] == 1,
            "恢复范围后首次冻结修订不是 1。",
        )
        checks.append(
            {
                "检查": "跨业务模块修改",
                "结果": "已阻断并在恢复后形成首个冻结快照",
            }
        )

        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第一版",
            (
                "P0：PolicyContactDraftMapper 将 policyNumber 写入 partyId，"
                "同时将 customerId 写入 policyNo，与 Design 字段映射表相反。"
                "该缺陷会把工单绑定到错误保单和客户，禁止进入测试。"
                "手机号脱敏由后续测试补充边界验证。"
            ),
        )
        record(repo, feature, "code-review-findings")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "failed",
            "--evidence",
            (
                "逐项对照 Design 字段映射表与冻结 Mapper，"
                "复现 policyNumber/customerId 交叉写入。"
            ),
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第一版",
            "字段错配尚未修复，当前资产只记录阻塞状态。",
        )
        record(repo, feature, "auto-fix-summary")
        expect_control_failure(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "错误声称字段映射已经修复。",
            contains=("requires Code Review passed",),
        )

        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftMapper.java",
            mapper_source(
                fixed_alias_mapping=True,
                fixed_mobile_mask=False,
            ),
        )
        second_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            second_snapshot["code_revision"] == 2,
            "字段映射修复后没有形成第二个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第二版",
            (
                "已完整复审第二个冻结范围的十四个生产变更文件。"
                "policyNumber -> policyNo、customerId -> partyId 已与 Design"
                " 映射表一致；幂等键、审计人和 expectedVersion 映射正确。"
                "未发现其他阻断、严重或一般问题。"
            ),
        )
        review_v2 = record(
            repo,
            feature,
            "code-review-findings",
        )["result"]
        require(
            review_v2["artifacts"]["code-review-findings"]["revision"]
            == 2,
            "第二版 Code Review 资产修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第二轮完整复审覆盖十四个生产变更文件，P0 字段错配已关闭。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第二版",
            (
                "修正 Mapper 中 policyNumber 与 customerId 的交叉映射，"
                "重新冻结并逐文件完成第二轮 Code Review。"
            ),
        )
        record(repo, feature, "auto-fix-summary")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "字段错配已修复，第二个冻结范围的 Code Review 已通过。",
        )
        checks.append(
            {
                "检查": "字段映射 Code Review 返工",
                "结果": "P0 错配未放行，修复并全量复审后关闭",
            }
        )

        require(
            resume_action(repo, feature)
            == "generate-or-update-test-source",
            "首次 Review 与 Auto-fix 关闭后没有进入测试源码生成。",
        )
        test_files = write_test_phase(repo)
        require(
            len(test_files) == 4,
            "Unit Test 第一轮没有生成四层测试文件。",
        )
        third_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            third_snapshot["code_revision"] == 3,
            "测试源码生成后没有形成第三个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第三版",
            (
                "Unit Test Skill 第一轮新增 Mapper、Repository、Service、"
                "Controller 四层测试后，已重新检查当前十八个变更文件。"
                "测试覆盖字段别名、标准化、脱敏、幂等、冲突、乐观版本、"
                "草稿状态、无变化修改和 HTTP 201/400/409。"
                "当前冻结范围未发现可执行评审问题。"
            ),
        )
        record(repo, feature, "code-review-findings")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第三轮完整复审绑定四层测试写入后的十八文件冻结范围。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第三版",
            (
                "测试源码使旧冻结范围失效；已重新冻结和完整复审。"
                "本轮没有新增评审发现，因此无需自动修复。"
            ),
        )
        record(repo, feature, "auto-fix-summary")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "not-required",
            "--evidence",
            "第三个冻结范围已完整复审且没有可执行发现。",
        )
        checks.append(
            {
                "检查": "Unit Test 两轮交接",
                "结果": "四层测试仅在首次评审关闭后生成，并重新冻结复审",
            }
        )

        failed_execution = run_feature_tests(repo, feature)
        require(
            failed_execution["outcome"] == "failed",
            f"首次真实测试没有暴露脱敏缺陷：{failed_execution}",
        )
        require(
            failed_execution["test_counts"]["total"] == 23
            and failed_execution["test_counts"]["failed"] == 1
            and failed_execution["test_counts"]["errors"] == 0,
            (
                "首次真实测试应为二十三项中一项失败："
                f"{failed_execution['test_counts']}"
            ),
        )
        write_unit_summary(
            feature,
            failed_execution,
            conclusion="国际区号手机号被原样返回，禁止归档",
        )
        record(repo, feature, "unit-test-summary")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "unit-test",
            "--result",
            "failed",
            "--evidence",
            (
                "控制器真实执行二十三项测试，其中国际区号手机号"
                "脱敏断言失败一项。"
            ),
        )
        archive_before_fix = run_control(
            repo,
            "archive-check",
            "--feature-dir",
            str(feature),
            "--require-archive",
            expected=1,
        )
        require(
            any(
                "QUALITY_GATE_NOT_PASSED:unit-test" in error
                for error in archive_before_fix["result"]["errors"]
            ),
            "脱敏测试失败后 Archive 没有被质量 Gate 阻断。",
        )
        checks.append(
            {
                "检查": "真实脱敏测试失败与提前归档",
                "结果": "二十三项中一项失败，Archive 已阻断",
            }
        )

        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactDraftMapper.java",
            mapper_source(
                fixed_alias_mapping=True,
                fixed_mobile_mask=True,
            ),
        )
        fourth_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            fourth_snapshot["code_revision"] == 4,
            "脱敏修复后没有形成第四个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第四版",
            (
                "真实测试发现国际区号手机号泄漏后，Mapper 改为保留国家码和"
                "前三位号段、隐藏中间四位、仅显示末四位。"
                "已重新检查当前十四个生产文件和四个测试文件；字段别名、"
                "邮箱脱敏、普通手机号及国际区号手机号行为均符合 Spec。"
                "未发现剩余可执行问题。"
            ),
        )
        record(repo, feature, "code-review-findings")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第四轮全量复审绑定脱敏修复后的十八文件冻结范围。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第四版",
            (
                "修复国际区号手机号脱敏，保留前缀和末四位并隐藏中段；"
                "重新冻结、全量复审，字段映射修复保持有效。"
            ),
        )
        record(repo, feature, "auto-fix-summary")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "脱敏缺陷已修复，第四个冻结范围已通过完整 Code Review。",
        )

        passed_execution = run_feature_tests(repo, feature)
        require(
            passed_execution["outcome"] == "passed",
            f"脱敏修复后真实测试没有通过：{passed_execution}",
        )
        require(
            passed_execution["test_counts"]["total"] == 23
            and passed_execution["test_counts"]["passed"] == 23
            and passed_execution["test_counts"]["failed"] == 0
            and passed_execution["test_counts"]["errors"] == 0
            and passed_execution["test_counts"]["skipped"] == 0,
            (
                "修复后测试计数不符合预期："
                f"{passed_execution['test_counts']}"
            ),
        )
        write_unit_summary(
            feature,
            passed_execution,
            conclusion="二十三项新增、修改与字段映射测试全部通过",
        )
        unit_summary_v2 = record(
            repo,
            feature,
            "unit-test-summary",
        )["result"]
        require(
            unit_summary_v2["artifacts"]["unit-test-summary"]["revision"]
            == 2,
            "成功测试后的 Unit Test Summary 没有形成第二版。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "unit-test",
            "--result",
            "passed",
            "--evidence",
            "控制器真实执行二十三项测试，全部通过且无失败、Error 或跳过。",
        )
        approve_demo(
            repo,
            feature,
            "unit-test-summary",
            "mutation-unit-test-summary-v2",
        )
        checks.append(
            {
                "检查": "测试返工与四层业务验收",
                "结果": "脱敏修复、复审后 23/23 通过",
            }
        )

        archive_evidence = run_control(
            repo,
            "prepare-archive",
            "--feature-dir",
            str(feature),
        )["result"]
        write_asset(
            feature,
            "archive.md",
            "归档总结",
            (
                "保单联系方式变更草稿新增与修改功能已完成。"
                "十四个生产变更文件和四个测试文件覆盖显式字段映射、"
                "幂等创建、冲突载荷、草稿状态、乐观版本、无变化修改、"
                "敏感字段脱敏和 HTTP 契约。经历一次 P0 字段错配 Review"
                " 返工和一次真实脱敏测试返工。"
                f"最终范围 SHA-256：`{archive_evidence['scope_sha256']}`；"
                f"测试证据 SHA-256："
                f"`{archive_evidence['unit_test_evidence_sha256']}`；"
                f"归档证据 SHA-256：`{archive_evidence['evidence_sha256']}`。"
            ),
        )
        record(repo, feature, "archive")
        archive_check = run_control(
            repo,
            "archive-check",
            "--feature-dir",
            str(feature),
            "--require-archive",
        )
        require(
            archive_check["result"]["valid"],
            f"最终 Archive 检查失败：{archive_check}",
        )
        approve_demo(
            repo,
            feature,
            "archive",
            "mutation-archive-approval",
        )

        validation = run_control(
            repo,
            "validate",
            "--feature-dir",
            str(feature),
        )
        require(
            validation["result"]["valid"],
            f"最终控制状态无效：{validation}",
        )
        final_state = read_json(
            feature / ".sdd2/feature-state.json"
        )
        final_commit_count = int(
            git(repo, "rev-list", "--count", "HEAD")
        )
        require(
            final_commit_count == baseline_commit_count == 1,
            "新增/修改型 Demo 发生了未授权 Git 提交。",
        )
        require(
            final_state["current_stage"] == "archive"
            and final_state["stage_status"] == "completed",
            "新增/修改型 Demo 最终状态不是 archive/completed。",
        )
        require(
            not git_path(repo, "sdd2-active-feature.json").exists(),
            "Archive 批准后 worktree 活动锁没有释放。",
        )
        public_assets = sorted(
            path.name
            for path in feature.glob("*.md")
            if path.is_file()
        )
        require(
            len(public_assets) == 9,
            f"最终公开资产数量不是九项：{public_assets}",
        )
        approval_records = read_jsonl(
            feature / ".sdd2/gate-approvals.jsonl"
        )
        event_records = read_jsonl(
            feature / ".sdd2/events.jsonl"
        )
        revision_files = sorted(
            (feature / ".sdd2/revisions").glob("*/*.md")
        )
        phase_approvals = [
            approval
            for approval in approval_records
            if approval["stage"].startswith("phase-review:")
        ]
        require(
            len(phase_approvals) == 4,
            "四项生产 Phase Review 没有完整进入追加批准链。",
        )
        require(
            len(approval_records) == 9,
            f"人工批准链应为九条：{len(approval_records)}",
        )
        require(
            len(revision_files) == 16,
            f"资产修订快照应为十六份：{len(revision_files)}",
        )
        remote_ref = subprocess.run(
            [
                "git",
                "--git-dir",
                str(remote),
                "show-ref",
                "--verify",
                "refs/heads/main",
            ],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            remote_ref.returncode != 0,
            "被阻断的 push 仍向临时远端写入分支。",
        )
        checks.append(
            {
                "检查": "最终状态、批准链、资产、锁与 Git",
                "结果": "全部一致且无自动提交推送",
            }
        )

        result = {
            "Demo 结论": "通过",
            "实现功能": "保单联系方式变更草稿创建、查询与修改",
            "功能类型": "新增 + 修改 + 字段映射 + 幂等 + 乐观版本",
            "Java 运行版本": doctor["java_specification_version"],
            "最终阶段": final_state["current_stage"],
            "最终状态": final_state["stage_status"],
            "生产变更文件数量": len(production_files),
            "测试文件数量": len(test_files),
            "最终测试计数": passed_execution["test_counts"],
            "首次失败测试计数": failed_execution["test_counts"],
            "公开资产数量": len(public_assets),
            "不可变修订快照数量": len(revision_files),
            "批准链记录数量": len(approval_records),
            "事件链记录数量": len(event_records),
            "冻结代码修订数量": fourth_snapshot["code_revision"],
            "最终测试证据 SHA-256":
                passed_execution["evidence_sha256"],
            "最终归档证据 SHA-256":
                archive_evidence["evidence_sha256"],
            "Git 提交数": final_commit_count,
            "深度检查点数量": len(checks),
            "检查点": checks,
        }
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DemoFailure as exc:
        print(
            json.dumps(
                {"Demo 结论": "失败", "错误": str(exc)},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
