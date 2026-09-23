package com.secureupi.backend.repository;

import com.secureupi.backend.model.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByUserId(String userId);
    List<Transaction> findByIsFlaggedTrue();
    List<Transaction> findByRiskLevel(String riskLevel);
}