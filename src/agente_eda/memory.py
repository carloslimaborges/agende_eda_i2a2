from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class AgentMemory:
    dataset_summary: Optional[dict] = None
    insights: List[str] = field(default_factory=list)
    qa_history: List[Dict[str, str]] = field(default_factory=list)

    def store_dataset_summary(self, summary: dict):
        self.dataset_summary = summary

    def add_insight(self, text: str):
        if text and text.strip():
            self.insights.append(text.strip())

    def add_qa(self, question: str, answer: str):
        if question and answer:
            self.qa_history.append({"q": question, "a": answer})

    def conclusions_text(self, last_n_qas: int = 5) -> str:
        parts = []
        if self.dataset_summary:
            parts.append("**Resumo do dataset (compacto):**")
            parts.append(f"- Linhas: {self.dataset_summary.get('rows')} | Colunas: {self.dataset_summary.get('cols')}")
        if self.insights:
            parts.append("**Insights automáticos do agente:**")
            parts += [f"- {i}" for i in self.insights[-5:]]
        if self.qa_history:
            parts.append("**Perguntas e respostas recentes:**")
            for qa in self.qa_history[-last_n_qas:]:
                parts.append(f"- **Q:** {qa['q']}\n  **A:** {qa['a']}")
        return "\n".join(parts) if parts else "Ainda não há conclusões armazenadas."
