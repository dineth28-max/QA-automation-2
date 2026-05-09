package com.mango.automation;

import java.time.Duration;

import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

class LoginFlowTest {
    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--ignore-certificate-errors");
        options.addArguments("--allow-insecure-localhost");
        options.addArguments("--window-size=1440,1080");

        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(25));
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    void userCanLogInAndSeeTheLandingPage() {
        String baseUrl = resolveValue("APP_BASE_URL", "app.baseUrl");
        String username = resolveValue("APP_USERNAME", "app.username", "dineth");
        String password = resolveValue("APP_PASSWORD", "app.password", "dineth@123");

        if (baseUrl.isBlank()) {
            fail("APP_BASE_URL or -Dapp.baseUrl must be set");
        }

        driver.get(baseUrl);

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username"))).sendKeys(username);
        driver.findElement(By.id("password")).sendKeys(password);
        driver.findElement(By.cssSelector("button[type='submit']")).click();

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("nav")));
        wait.until(driver -> driver.getPageSource().contains("Experience the untamed essence of Alphonso."));

        String bodyText = driver.findElement(By.tagName("body")).getText();
        String pageSource = driver.getPageSource();
        
        assertTrue(bodyText.contains("RAW Pressery"), "Expected authenticated navigation to be visible");
        assertTrue(pageSource.contains("Experience the untamed essence of Alphonso."), "Expected hero content after login");
    }

    private String resolveValue(String environmentKey, String systemPropertyKey, String defaultValue) {
        String systemValue = System.getProperty(systemPropertyKey);
        if (systemValue != null && !systemValue.isBlank()) {
            return systemValue;
        }

        String environmentValue = System.getenv(environmentKey);
        if (environmentValue != null && !environmentValue.isBlank()) {
            return environmentValue;
        }

        return defaultValue;
    }

    private String resolveValue(String environmentKey, String systemPropertyKey) {
        return resolveValue(environmentKey, systemPropertyKey, "");
    }
}