package com.secureupi.backend.exception;

public class MLServiceException extends RuntimeException {
    public MLServiceException(String message) {
        super(message);
    }
}