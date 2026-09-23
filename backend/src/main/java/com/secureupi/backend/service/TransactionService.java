package com.secureupi.backend.service;

import com.secureupi.backend.dto.MLPredictionRequestDTO;
import com.secureupi.backend.dto.MLPredictionResponseDTO;
import com.secureupi.backend.dto.TransactionRequestDTO;
import com.secureupi.backend.dto.TransactionResponseDTO;
import com.secureupi.backend.model.Transaction;
import com.secureupi.backend.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tools.jackson.databind.json.JsonMapper;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
@RequiredArgsConstructor
@Slf4j
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final MLPredictionService mlPredictionService;
    private final JsonMapper jsonMapper;

    @Transactional
    public TransactionResponseDTO processTransaction(TransactionRequestDTO request) {

        LocalDateTime txnTime = request.getTransactionTime() != null
                ? request.getTransactionTime()
                : LocalDateTime.now();

        MLPredictionRequestDTO mlRequest = MLPredictionRequestDTO.builder()
                .user_id(request.getUserId())
                .amount(request.getAmount().doubleValue())
                .timestamp(txnTime.format(DateTimeFormatter.ISO_DATE_TIME))
                .merchant(request.getMerchant())
                .transaction_type(request.getTransactionType())
                .location(request.getLocation())
                .device_info(request.getDeviceInfo())
                .build();

        MLPredictionResponseDTO mlResponse = mlPredictionService.getPrediction(mlRequest);

        String securityAction = determineSecurityAction(mlResponse.getRisk_level());

        Transaction transaction = Transaction.builder()
                .userId(request.getUserId())
                .amount(request.getAmount())
                .merchant(request.getMerchant())
                .transactionType(request.getTransactionType())
                .location(request.getLocation())
                .deviceInfo(request.getDeviceInfo())
                .transactionTime(txnTime)
                .fraudProbability(mlResponse.getFraud_probability())
                .riskScore(mlResponse.getRisk_score())
                .riskLevel(mlResponse.getRisk_level())
                .isFlagged(mlResponse.getIs_flagged())
                .securityAction(securityAction)
                .explanation(toJson(mlResponse.getExplanation()))
                .build();

        Transaction saved = transactionRepository.save(transaction);
        log.info("Transaction saved for user {} — risk={}, action={}",
                saved.getUserId(), saved.getRiskLevel(), saved.getSecurityAction());

        return mapToResponseDTO(saved);
    }

    private String determineSecurityAction(String riskLevel) {
        if (riskLevel == null) {
            return "VERIFICATION_REQUIRED";
        }
        return switch (riskLevel.toLowerCase()) {
            case "low" -> "APPROVED";
            case "medium" -> "VERIFICATION_REQUIRED";
            case "high" -> "BLOCKED";
            default -> "VERIFICATION_REQUIRED";
        };
    }

    private String toJson(Object obj) {
        try {
            return jsonMapper.writeValueAsString(obj);
        } catch (Exception e) {
            log.warn("Failed to serialize explanation to JSON", e);
            return "{}";
        }
    }

    private TransactionResponseDTO mapToResponseDTO(Transaction t) {
        return TransactionResponseDTO.builder()
                .id(t.getId())
                .userId(t.getUserId())
                .fraudProbability(t.getFraudProbability())
                .riskScore(t.getRiskScore())
                .riskLevel(t.getRiskLevel())
                .isFlagged(t.getIsFlagged())
                .securityAction(t.getSecurityAction())
                .explanation(t.getExplanation())
                .build();
    }
}