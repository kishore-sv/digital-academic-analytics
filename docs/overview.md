# Project Overview

## Project Title

**Digital Academic Performance Monitoring and Institutional Analytics System**

## Project ID

PRJ_649

## Team

**SMK**

| Member | Roll Number |
|--------|-------------|
| Srivatsa Kamble | 20231CSE0257 |
| Kishore S V | 20231CSE0260 |
| Mohan A | 20231CSE0273 |

## Guide

Nayeem Akhtar Sholapur

## Purpose

A software-only platform that enables educational institutions to monitor student academic performance, generate institutional analytics, predict outcomes using machine learning, and identify at-risk students — all within a secure multi-tenant architecture.

## Technology Scope

| Layer | Technologies |
|-------|-------------|
| Client | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Bun |
| Backend | FastAPI, Python, SQLAlchemy, uv |
| Database | PostgreSQL |
| ML | Pandas, NumPy, Scikit-learn, Pickle (.pkl) |

## Scope Exclusions

The following are **not** part of the current implementation scope:

- Hardware, ESP32, RFID, sensors, physical IoT devices
- GIS (on hold / removed)
- Blockchain, smart contracts (on hold / removed)
- Kubernetes, Kafka, Spark, Redis
- Microservices architecture

The project uses a **monolithic software architecture**: Next.js frontend + FastAPI backend + PostgreSQL + separate ML development directory.

## Related Documentation

- [Architecture](architecture.md)
- [Features](features.md)
- [User Roles](user-roles.md)
- [Authentication](authentication.md)
- [Multi-Tenancy](multi-tenancy.md)
