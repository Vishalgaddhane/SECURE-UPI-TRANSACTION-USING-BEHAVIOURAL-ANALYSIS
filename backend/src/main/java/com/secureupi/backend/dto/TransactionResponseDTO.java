package com.secureupi.backend.dto;
 
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
 
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TransactionResponseDTO {
    private Long id;
    private String userId;
    private Double fraudProbability;
    private Double riskScore;
    private String riskLevel;
    private Boolean isFlagged;
    private String securityAction;
    private String explanation;
}
 