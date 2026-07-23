# Security & Differential Privacy Specification

## Security Overview

1. **Authentication & Authorization**:
   - Industry-standard JWT tokens with 24-hour expiration.
   - Passwords and Node API keys hashed with `bcrypt`.
   - Strict Role-Based Access Control (RBAC): `SYSTEM_ADMIN`, `HOSPITAL_ADMIN`, `AUDITOR`.

2. **Data Isolation & HIPAA Compliance**:
   - Zero-Knowledge raw data architecture: Hospital patient records, DICOM images, and diagnostic EHR tables **NEVER** leave the hospital intranet perimeter.
   - Only mathematical weight parameters ($\Delta \theta$) are transmitted over TLS 1.3 encrypted endpoints.

## Differential Privacy (DP-SGD) Implementation

1. **Gradient Clipping**:
   - Local gradients are clipped to a maximum $\ell_2$-norm bound $C = 1.0$:
     $$\bar{g}_t = g_t / \max\left(1, \frac{\|g_t\|_2}{C}\right)$$
2. **Gaussian Noise Addition**:
   - Noise calibrated to the sensitivity and noise multiplier $\sigma = 0.05$ is added to weights prior to aggregation:
     $$\tilde{\theta} = \theta + \mathcal{N}(0, \sigma^2 C^2 \mathbf{I})$$
3. **Moments Accountant Privacy Tracking**:
   - Tracks cumulative privacy budget $(\epsilon, \delta)$ where $\delta = 10^{-5}$.
