# Grabaciones de Audio y Video — Prácticas Preprofesionales

Directorio para almacenar los archivos multimedia brutos de reuniones con supervisores, talleres de inducción, defensas de informes, coordinaciones de obra o sesiones de trabajo.

## Reglas Operativas:

1. **Exclusión de Git Automática:**
   - Todo archivo `.mp4`, `.mp3`, `.m4a`, `.wav`, `.mkv`, `.avi`, `.mov` está excluido de control de versiones vía `.gitignore`.
   - Esto evita la degradación y sobrepeso del repositorio local y remoto.

2. **Nomenclatura Recomendada:**
   - `YYYY-MM-DD_reunion_supervisor_[tema].mp4`
   - `YYYY-MM-DD_levantamiento_campo_[sitio].m4a`
   - `YYYY-MM-DD_tutoria_academica.mp3`

3. **Flujo de Procesamiento a Transcripción:**
   - Una vez colocado el audio/video aquí, ejecute transcripción automática (Whisper / Gemini) hacia `transcripciones/` o la sesión correspondiente.
   - Solo el archivo de texto markdown `.md` resultante es versionado e integrado a la memoria del sistema.
