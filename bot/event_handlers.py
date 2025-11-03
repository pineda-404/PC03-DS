class EventHandler:
    """Coordina la detección y procesamiento de incidentes."""

    def handle_commit(self, commit_message):
        """
        Detecta incidentes en mensajes de commit.

        Returns:
            Dict con 'title' y 'severity', o None si no es incidente
        """
        return self._parse_incident(commit_message)

    def _parse_incident(self, msg):
        if not msg.startswith("incident:"):
            return None

        content = msg.replace("incident:", "").strip()
        if not content:
            return None

        severity = "P3"
        title = content

        for priority in ["P0", "P1", "P2", "P3"]:
            if priority in content:
                severity = priority
                title = content.replace(priority, "").strip().lstrip("- ").strip()
                break

        # Normalizar espacios múltiples dentro del título
        if title:
            title = " ".join(title.split())

        return {"title": title, "severity": severity} if title else None
