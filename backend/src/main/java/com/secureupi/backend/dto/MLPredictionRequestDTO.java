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
public class MLPredictionRequestDTO {
    private String user_id;
    private Double amount;
    private String timestamp;
    private String merchant;
    private String transaction_type;
    private String location;
    private String device_info;
}