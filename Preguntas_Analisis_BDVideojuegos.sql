-- ¿Qué juego vende más, y qué categoría de juegos genera más dinero en promedio por venta?

SELECT 
    j.categoria,
    COUNT(c.id_compra) as total_ventas,
    SUM(c.monto) as ingresos_totales,
    CAST(AVG(c.monto) AS DECIMAL(10,2)) as ticket_promedio
FROM juegos j
JOIN compras_en_plataforma c ON j.id_juego = c.id_juego
GROUP BY j.categoria
ORDER BY ingresos_totales DESC;


-- ¿Cuáles son los usuarios más adictos (que pasan mas tiempo jugando)?

SELECT TOP 10
    u.nombre_usuario,
    u.pais,
    COUNT(s.id_sesion) as cantidad_sesiones,
    SUM(DATEDIFF(MINUTE, s.fecha_inicio, s.fecha_fin)) / 60.0 as horas_jugadas
FROM jugadores u
JOIN sesiones s ON u.id_jugador = s.id_jugador
GROUP BY u.nombre_usuario, u.pais
ORDER BY horas_jugadas DESC;


-- ¿Qué país tiene los usuarios más valiosos (cuánto gasta en promedio un usuario de cada país)?

SELECT 
    u.pais,
    COUNT(DISTINCT u.id_jugador) as total_jugadores,
    SUM(c.monto) as total_gastado,
    CAST(SUM(c.monto) / COUNT(DISTINCT u.id_jugador) AS DECIMAL(10,2)) as ARPU -- Ingreso Promedio por Usuario
FROM jugadores u
JOIN compras_en_plataforma c ON u.id_jugador = c.id_jugador
GROUP BY u.pais
HAVING COUNT(DISTINCT u.id_jugador) > 5 -- Filtramos países con muy pocos datos para evitar sesgos
ORDER BY ARPU DESC;


-- ¿Hay juegos que vendieron mucho (mucha publicidad) pero tienen calificaciones terribles por parte de los usuarios?

SELECT TOP 5
    j.nombre,
    SUM(c.monto) as ingresos_generados,
    AVG(p.puntuacion) as calificacion_promedio
FROM juegos j
JOIN compras_en_plataforma c ON j.id_juego = c.id_juego
LEFT JOIN puntuaciones p ON j.id_juego = p.id_juego
GROUP BY j.nombre
HAVING SUM(c.monto) > 500 AND AVG(p.puntuacion) < 5 -- Juegos con buenas ventas pero nota reprobatoria
ORDER BY ingresos_generados DESC;


-- ¿En qué horario del día se conecta la mayoría de los jugadores?

SELECT 
    DATEPART(HOUR, fecha_inicio) as hora_del_dia,
    COUNT(id_sesion) as volumen_usuarios
FROM sesiones
GROUP BY DATEPART(HOUR, fecha_inicio)
ORDER BY volumen_usuarios DESC;