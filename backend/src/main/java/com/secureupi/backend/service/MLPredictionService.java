package com.secureupi.backend.service;

import com.secureupi.backend.dto.MLPredictionRequestDTO;
import com.secureupi.backend.dto.MLPredictionResponseDTO;
import com.secureupi.backend.exception.MLServiceException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
@Slf4j
public class MLPredictionService {

    private final RestTemplate restTemplate;

    @Value("${ml.api.url}")
    private String mlApiUrl;

    public MLPredictionResponseDTO getPrediction(MLPredictionRequestDTO request) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<MLPredictionRequestDTO> entity = new HttpEntity<>(request, headers);

        try {
            ResponseEntity<MLPredictionResponseDTO> response = restTemplate.exchange(
                    mlApiUrl,
                    HttpMethod.POST,
                    entity,
                    MLPredictionResponseDTO.class
            );
            return response.getBody();

        } catch (HttpStatusCodeException e) {
            log.error("ML API returned error status {}: {}", e.getStatusCode(), e.getResponseBodyAsString());
            throw new MLServiceException("ML service returned an error: " + e.getStatusCode());

        } catch (ResourceAccessException e) {
            log.error("Could not reach ML API at {}: {}", mlApiUrl, e.getMessage());
            throw new MLServiceException("ML service is unreachable. Is ml_api.py running on " + mlApiUrl + "?");
        }
    }
}