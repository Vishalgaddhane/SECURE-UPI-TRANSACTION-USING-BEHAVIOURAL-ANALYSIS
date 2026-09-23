package com.secureupi.backend.controller;

import com.secureupi.backend.dto.AdminStatsDTO;
import com.secureupi.backend.dto.TransactionRequestDTO;
import com.secureupi.backend.dto.TransactionResponseDTO;
import com.secureupi.backend.model.Transaction;
import com.secureupi.backend.repository.TransactionRepository;
import com.secureupi.backend.service.TransactionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/transactions")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:5173")
public class TransactionController {

    private final TransactionService transactionService;
    private final TransactionRepository transactionRepository;

    @PostMapping
    public ResponseEntity<TransactionResponseDTO> submitTransaction(
            @Valid @RequestBody TransactionRequestDTO request) {
        TransactionResponseDTO response = transactionService.processTransaction(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<Transaction>> getAllTransactions() {
        return ResponseEntity.ok(transactionRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Transaction> getTransactionById(@PathVariable Long id) {
        return transactionRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/flagged")
    public ResponseEntity<List<Transaction>> getFlaggedTransactions() {
        return ResponseEntity.ok(transactionRepository.findByIsFlaggedTrue());
    }

    @GetMapping("/risk/{level}")
    public ResponseEntity<List<Transaction>> getTransactionsByRiskLevel(@PathVariable String level) {
        String capitalized = level.substring(0, 1).toUpperCase() + level.substring(1).toLowerCase();
        return ResponseEntity.ok(transactionRepository.findByRiskLevel(capitalized));
    }

    @GetMapping("/stats")
    public ResponseEntity<AdminStatsDTO> getStats() {
        List<Transaction> all = transactionRepository.findAll();

        long low = all.stream().filter(t -> "Low".equalsIgnoreCase(t.getRiskLevel())).count();
        long medium = all.stream().filter(t -> "Medium".equalsIgnoreCase(t.getRiskLevel())).count();
        long high = all.stream().filter(t -> "High".equalsIgnoreCase(t.getRiskLevel())).count();
        long flagged = all.stream().filter(t -> Boolean.TRUE.equals(t.getIsFlagged())).count();

        AdminStatsDTO stats = AdminStatsDTO.builder()
                .total(all.size())
                .lowCount(low)
                .mediumCount(medium)
                .highCount(high)
                .flaggedCount(flagged)
                .build();

        return ResponseEntity.ok(stats);
    }
}