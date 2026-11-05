# Cotización con mensualidades (plantilla para WhatsApp)

Tu cotización: **$[CONTADO]** de contado (transferencia, efectivo o tarjeta en una exhibición).

Si prefieres pagar con tarjeta de crédito en mensualidades:
- 3 mensualidades de ≈ $[M3] (total $[T3])
- 6 mensualidades de ≈ $[M6] (total $[T6])
- 9 mensualidades de ≈ $[M9] (total $[T9])
- 12 mensualidades de ≈ $[M12] (total $[T12])

Pagando de contado te ahorras hasta $[AHORRO]. ¿Cuál te acomoda? Te mando el link de pago.

Cómo calcular: usa el simulador de cualquier página de servicio, o `python3 -c "import sys; sys.path.insert(0,'tools/pasto'); from mensualidades import planes; print(planes(CONTADO))"`.
Solo ofrece los plazos que aplican al monto (desde $2,000: 3; desde $5,000: 3 y 6; desde $15,000: los cuatro).
Llámalo siempre "mensualidades con tarjeta de crédito"; el total a plazos es mayor que el de contado.
