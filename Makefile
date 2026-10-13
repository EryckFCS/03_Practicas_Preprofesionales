# ==============================================================================
# CAPITAL NODE MAKEFILE — PRÁCTICAS PREPROFESIONALES (OCTAVO CICLO)
# ==============================================================================

.PHONY: help status sync audit-hours

help:
	@echo "Comandos disponibles:"
	@echo "  make status       - Muestra el estado del nodo y archivos en lake/"
	@echo "  make sync         - Prepara notas en lake/knowledge/ para ingesta RAG"
	@echo "  make audit-hours  - Ejecuta auditoria de horas acumuladas en bitacoras"

status:
	@echo "=== ESTADO DEL NODO: PRACTICAS PREPROFESIONALES (ARQUITECTURA) ==="
	@echo "Archivos raw en lake/raw:"
	@dir lake\raw
	@echo "Knowledge files (lake/knowledge):"
	@dir lake\knowledge
	@echo "Grabaciones locales en grabaciones/:"
	@dir grabaciones

sync:
	@echo "Indexando conocimiento del nodo en RAG Exocortex..."

audit-hours:
	@python scripts\auditar_horas.py
