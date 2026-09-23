package com.secureupi.backend.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Setter
public class TransactionRequestDTO {

    @NotBlank
    private String userId;

    @NotNull
    @DecimalMin(value = "0.01")
    private BigDecimal amount;

    @NotBlank
    private String merchant;

    @NotBlank
    private String transactionType;

    @NotBlank
    private String location;

    @NotBlank
    private String deviceInfo;

    private LocalDateTime transactionTime;
}