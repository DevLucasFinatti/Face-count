# 🧠 FaceMesh Counter em Python

Um projeto daora em Python que reconhece **múltiplos rostos** na câmera em tempo real, renderiza uma **malha facial 3D** (Face Mesh) sobre cada um e exibe no console o número de rostos detectados. 😎

---

## 🎥 O que ele faz?

- 📸 Usa a webcam (ou vídeo) para capturar imagens em tempo real  
- 🧬 Detecta até **40 rostos simultaneamente** com precisão  
- 🕸️ Renderiza a **malha facial com 468 pontos de referência**  
- 🔢 Mostra no terminal a **quantidade de rostos detectados**  
- 🤳 Espelha a imagem para visualização estilo "selfie"  

---

## 📦 Requisitos

Antes de rodar, instale as dependências com:

```bash
pip install opencv-python mediapipe
```

---

## 🚀 Como rodar

Clone o repositório:

```bash
git clone https://github.com/DevLucasFinatti/Face-count.git
cd Face-count
```

Execute o script:

```bash
python main.py
```

A janela abrirá com a câmera ativa. Pressione `q` para sair.

---

## 💡 Personalização

Quer usar um vídeo em vez da webcam?  
Troque esta linha no seu `main.py`:

```python
cap = cv2.VideoCapture(0)
```

Por esta:

```python
cap = cv2.VideoCapture('video.mp4')
```

---

## 📁 Estrutura do projeto

```
FaceMesh-Counter/
├── main.py            # Código principal com reconhecimento facial
├── README.md          # Este arquivo incrível 😎
└── requirements.txt   # (Opcional) Dependências do projeto
```

---

## 👨‍💻 Autor

Desenvolvido com 🧠, ☕ e Python por **Lucas Finatti**  
📧 lucas.finatti@hotmail.com

> "Visão computacional é quando o Python enxerga melhor que muita gente." 🔍
