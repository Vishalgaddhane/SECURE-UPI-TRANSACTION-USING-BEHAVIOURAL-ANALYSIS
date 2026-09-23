package com.secureupi.backend.dto;
 
import lombok.Getter;
import lombok.Setter;
 
import java.util.Map;
 
@Getter
@Setter
public class MLPredictionResponseDTO {
    private Double fraud_probability;
    private Double risk_score;
    private String risk_level;
    private Boolean is_flagged;
    private Boolean is_known_user;
    private Map<String, Double> explanation;
}
 