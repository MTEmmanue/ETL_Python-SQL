-- Creación de la Base de datos
CREATE DATABASE Videojuegos
USE Videojuegos;

-- 1. Tabla JUEGOS
CREATE TABLE juegos (
    id_juego INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    fecha_lanzamiento INT,
    puntaje_global DECIMAL(10, 2)
);

-- 2. Tabla JUGADORES
CREATE TABLE jugadores (
    id_jugador INT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    pais VARCHAR(50),
    fecha_registro DATE
);

-- 3. Tabla SESIONES
CREATE TABLE sesiones (
    id_sesion INT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador),
    FOREIGN KEY (id_juego) REFERENCES juegos(id_juego)
);

-- 4. Tabla COMPRAS
CREATE TABLE compras_en_plataforma (
    id_compra INT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador),
    FOREIGN KEY (id_juego) REFERENCES juegos(id_juego)
);

-- 5. Tabla PUNTUACIONES
CREATE TABLE puntuaciones (
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    puntuacion INT,
    fecha DATE NOT NULL,
    PRIMARY KEY (id_jugador, id_juego, fecha),
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador),
    FOREIGN KEY (id_juego) REFERENCES juegos(id_juego)
);

-- Índices recomendados para rendimiento
CREATE INDEX idx_jugadores_pais ON jugadores(pais);
CREATE INDEX idx_juegos_categoria ON juegos(categoria);
CREATE INDEX idx_compras_fecha ON compras_en_plataforma(fecha);
CREATE INDEX idx_sesiones_fecha_inicio ON sesiones(fecha_inicio);

-- Ver que todos los registros fueron existosos
SELECT * FROM juegos
SELECT * FROM jugadores
SELECT * FROM compras_en_plataforma
SELECT * FROM puntuaciones
SELECT * FROM sesiones