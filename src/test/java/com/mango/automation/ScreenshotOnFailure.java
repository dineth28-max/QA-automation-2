package com.mango.automation;

import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Instant;
import java.util.Optional;

import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.TestWatcher;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class ScreenshotOnFailure implements TestWatcher {

    @Override
    public void testFailed(ExtensionContext context, Throwable cause) {
        try {
            Object testInstance = context.getRequiredTestInstance();
            Field[] fields = testInstance.getClass().getDeclaredFields();
            for (Field f : fields) {
                if (WebDriver.class.isAssignableFrom(f.getType())) {
                    f.setAccessible(true);
                    Object drv = f.get(testInstance);
                    if (drv instanceof WebDriver) {
                        WebDriver driver = (WebDriver) drv;
                        if (driver instanceof TakesScreenshot) {
                            byte[] bytes = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
                            Path dir = Paths.get("target", "surefire-reports", "screenshots");
                            Files.createDirectories(dir);
                            String method = context.getTestMethod().map(m -> m.getName()).orElse("unknown-method");
                            String cls = context.getTestClass().map(c -> c.getSimpleName()).orElse("unknown-class");
                            String ts = String.valueOf(Instant.now().toEpochMilli());
                            Path file = dir.resolve(cls + "-" + method + "-" + ts + ".png");
                            Files.write(file, bytes);
                        }
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("ScreenshotOnFailure: failed to capture screenshot: " + e.getMessage());
        }
    }

    @Override
    public void testSuccessful(ExtensionContext context) {
        // no-op
    }

    @Override
    public void testDisabled(ExtensionContext context, Optional<String> reason) {
        // no-op
    }

    @Override
    public void testAborted(ExtensionContext context, Throwable cause) {
        // no-op
    }
}
