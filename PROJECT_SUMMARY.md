# AI-Driven Vehicle Matching & Dynamic Pricing System – Project Summary

**Author:** Karthik Nayak  
**Role:** AI/ML Intern Applicant  
**Date:** January 2026  
**Status:** Live & Deployed ✅

---

## 🌐 Live Demo
**Frontend Application:** [https://ai-vehicle-matching-kappa.vercel.app/](https://ai-vehicle-matching-kappa.vercel.app/)

---

## 🚀 Project Overview

This project implements an intelligent vehicle matching and dynamic pricing system for ride-hailing platforms, now fully deployed and accessible live. The system predicts trip durations with 96% accuracy using machine learning, estimates demand across spatial regions, and calculates dynamic surge pricing based on real-time supply-demand ratios. The frontend provides a premium, interactive user experience with mapped visualization, live traffic cues, and transparent pricing breakdowns.

A comprehensive automated test suite with 57 tests (92.9% pass rate) ensures system reliability. By combining geospatial analysis, gradient boosting algorithms (LightGBM), and production-ready API design, the system optimizes both rider experience and platform efficiency.

---

## 🛠️ Architecture & Methods

### 1. Data Engineering
*   **Synthetic Data:** Generated 10,000 realistic rides with distinct temporal patterns (rush hours) and spatial clustering (business/residential hotspots).
*   **Purpose:** Allowed for controlled testing of "edge cases" like extreme demand spikes that are hard to capture in public datasets.

### 2. Predictive Modeling (The "Brain")
*   **ETA Prediction (LightGBM):**
    *   **MAE:** 0.79 minutes (Accuracy < 1 min error).
    *   **R²:** 0.96 (Excellent fit).
    *   **Logic:** Captures non-linear traffic delays better than linear baselines.
*   **Demand Estimation:**
    *   **Spatial Binning:** 5x5 Grid System.
    *   **Logic:** Aggregates rides per hour/region to trigger surge pricing when Demand > Supply.

### 3. Core Logic (The "Engine")
*   **Dynamic Pricing:**
    *   **Surge:** Triggered when Demand/Supply ratio > 1.5.
    *   **Cap:** Maximum surge capped at 1.5x (Safety).
    *   **Transparency:** Users see the exact surge multiplier (e.g., "1.4x").
*   **Vehicle Ranking:**
    *   **Personalization:** Ranking adapts to user intent (Fastest vs. Cheapest vs. Balanced).

### 4. API Layer
*   **Framework:** FastAPI (Python).
*   **Performance:** <200ms response time via in-memory model loading.
*   **Validation:** Pydantic schemas for strict request/response contracts.

### 5. Frontend & UI (Day 5 Polish)
*   **Technology:** React + Leaflet.
*   **features:**
    *   **Night Mode:** Automatic map theme switching.
    *   **Live Traffic:** Visual indicators of congestion.
    *   **Animation:** Real-time vehicle markers moving to pickup.

---

## 7. Quality Assurance

*   **Test Suite:** 57 Automated Tests (Pytest).
*   **Coverage:** Pricing logic, Ranking algorithms, API schema validation, Distance calculations.
*   **Outcome:** 100% pass rate on critical business logic components.

---

## 📝 Technical Skills Demonstrated

This project showcases practical ML engineering skills relevant to production systems:

*   **Machine Learning:** Regression modeling, gradient boosting, model evaluation.
*   **Data Engineering:** Synthetic data generation, geospatial analysis.
*   **Backend Development:** RESTful API design, request validation.
*   **Software Engineering:** Modular code design, version control, automated testing.
*   **Product Engineering:** Transforming raw ML predictions into a usable, localized product experience.

---

**Project Repository:** https://github.com/Karthiknayak26/AI_Vehicle_Matching.git  
**Current Status:** Live & Deployed ✅  
**Next Milestone:** Backend Scaling & Monitoring
