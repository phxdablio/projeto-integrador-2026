from pathlib import Path
import pandas as pd

def salvar_auditoria(auditoria: pd.DataFrame, caminho: str | Path) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    auditoria.to_csv(caminho, index=False, sep=";", encoding="utf-8-sig")
