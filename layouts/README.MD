# AriaStudio Dashboard Framework

AriaStudio is a browser-based dashboard framework designed for **ultra‑wide 301mm × 55mm bar‑shaped LCD screens** with a logical resolution of **1920 × 350 px** (aspect ratio ≈ 5.5:1).

All templates are built with strict layout constraints to ensure predictable rendering and a consistent user experience across different scaling environments.

---

## 📐 Display & Layout Specifications

### Viewport Locking (No Scrollbars)
- `html` and `body` are locked to `100vw × 100vh` with `overflow: hidden !important`.
- No fixed pixel values (e.g., `1920px` or `350px`) are used for dimensions.
- `box-sizing: border-box` is applied globally to prevent overflow.

### Dynamic Vertical Scaling
- The interface uses `flex` layout: `display: flex; flex-direction: column;`.
- Main content areas use `flex: 1; min-height: 0;` to adapt to remaining screen height.
- All child containers (cards, charts, SVG areas) also use `min-height: 0` and `min-width: 0` to avoid forced sizing and overflow.

### Text Overflow Protection
- All text content uses `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`.
- Font sizes are constrained with `clamp()` to prevent text from breaking the layout.

---

## ⚙️ Template Customization

Before deploying any HTML template, please adapt it to your local environment:

- **API Keys** – Set your own Gemini / OpenAI / DeepSeek keys in voice and chat modules.
- **Agent Behaviors** – Update task names and instruction sets for the Codex Agent to match your workflow.
- **Layout Variables** – Adjust CSS spacing, font sizes, or card counts to better fit your screen.

> **Note**: All templates are single‑file HTML. You can modify them directly or create your own from scratch.

---

## 🤖 Template Origin

All HTML templates provided in this repository have been **generated with the assistance of Gemini and OpenAI models**, then manually reviewed and tested for integration with the A527 hardware environment.

If you need custom‑designed templates or enterprise‑level support, feel free to reach out:

📧 **service@dspixel.com**

---

## 📎 Related Resources

- [Bridge Service Documentation](./BRIDGE_SERVICE.md) – Backend API setup and deployment guide.
- [AriaStudio PC Client](./ARIASTUDIO.md) – Desktop driver interface and usage instructions.

---

**Version**: v18 (no AI chat)  
**Last updated**: 2026-08-05
