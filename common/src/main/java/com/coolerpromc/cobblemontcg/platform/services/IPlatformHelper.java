package com.coolerpromc.cobblemontcg.platform.services;

public interface IPlatformHelper {
    String getPlatformName();
    boolean isDevelopmentEnvironment();
    default String getEnvironmentName() {
        return isDevelopmentEnvironment() ? "development" : "production";
    }
}
