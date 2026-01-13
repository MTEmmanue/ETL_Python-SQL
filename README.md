# 🚀 UBI-Games Analytics: Pipeline ETL & Análisis SQL

![Status](https://img.shields.io/badge/Status-Completado-green)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2019-red?logo=microsoft-sql-server&logoColor=white)
![ETL](https://img.shields.io/badge/Focus-ETL%20%26%20Data%20Engineering-orange)

<div align="center">
  <img src="Diagrama_Videojuegos.png" alt="Flujo del Proyecto" width="800"/>
</div>

---

## 📖 Descripción del Proyecto

Este repositorio contiene una solución **End-to-End** de Ingeniería de Datos para **UBI-Games**, una plataforma de videojuegos simulada. 

El objetivo principal fue transformar datos crudos y desconectados en una base de datos analítica confiable, permitiendo a la dirección (no técnica) tomar decisiones estratégicas sobre rentabilidad, retención de usuarios y comportamiento de compra.

### 🎯 El Desafío de Negocio
La empresa contaba con múltiples fuentes de datos (archivos CSV) con problemas de calidad:
* Registros huérfanos (sesiones de juegos que no existen).
* Duplicidad en puntuaciones.
* Inconsistencias temporales (fechas de fin anteriores al inicio).
* Transacciones financieras con valores nulos.

**Mi rol:** Diseñar un flujo ETL robusto para limpiar estos datos y centralizarlos en un Data Warehouse en SQL Server.

---

## ⚙️ Arquitectura y Tecnologías

El proyecto sigue un flujo clásico de ETL:

1.  **Extracción (Python):** Lectura automatizada de múltiples fuentes CSV.
2.  **Transformación (Pandas):** * Limpieza de tipos de datos y estandarización de fechas.
    * **Lógica de Integridad Referencial:** Filtrado de registros huérfanos (IDs no existentes en tablas dimensionales).
    * **Reglas de Negocio:** Eliminación de compras con monto nulo y deduplicación de puntuaciones diarias.
3.  **Carga (SQLAlchemy + PyODBC):** Ingesta masiva hacia SQL Server respetando restricciones de claves foráneas.
4.  **Análisis (SQL):** Consultas avanzadas para KPIs de negocio.

**Stack Tecnológico:**
- **Lenguaje:** Python 3.11
- **Librerías:** Pandas, SQLAlchemy, PyODBC.
- **Base de Datos:** Microsoft SQL Server.
- **Control de Versiones:** Git/GitHub.

---

## 📂 Estructura del Repositorio

```bash
├── 📁 Datos/                        # Datasets crudos (CSV) simulados
├── 📁 Python/                       # Scripts de procesamiento
│   └── ETL.py                       # Script principal de Extracción, Transformación y Carga
├── 📁 SQL/                          # Scripts de Base de Datos
│   ├── DDL_JuegosDB.sql             # Creación de tablas, relaciones e índices
│   └── Preguntas_Analisis.sql       # Consultas de negocio (KPIs, Churn, Revenue)
├── Diagrama_Videojuegos.png         # Arquitectura visual del proyecto
└── README.md                        # Documentación del proyecto
