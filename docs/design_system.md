Since you are a solo developer, this system focuses on **utility, speed of implementation, and a "Boutique AI" aesthetic.**

---

## 1. The Color Palette: "Precision & Intelligence"

Avoid "tech blue" defaults. Use a palette that feels professional and grounded.

| Element | Hex Code | Purpose |
| --- | --- | --- |
| **Primary** | `#1A1A1A` | Main headings, logo text, and primary buttons. |
| **Accent** | `#00A3FF` | Action items, links, and the "AI" circuit lines in your logo. |
| **Surface** | `#FFFFFF` | Card backgrounds and main content areas. |
| **Background** | `#F4F7F9` | Page background to create subtle contrast with white cards. |
| **Muted** | `#6B7280` | Body text and secondary information. |

---

## 2. Typography: "The Modern Editorial"

Typography is 90% of a minimalist design. Use high-quality, readable fonts.

* **Primary Font:** [Inter](https://rsms.me/inter/) (Free/Google Font). It is designed for screens and feels "engineered."
* **Scale Rules:**
* **H1 (Company Name):** 2.5rem (40px) | Bold | `-0.02em` letter spacing.
* **H2 (Section Headers):** 1.5rem (24px) | Semi-Bold | All Caps + `0.05em` spacing.
* **Body:** 1rem (16px) | Regular | `1.5` line height for readability.
* **Captions:** 0.875rem (14px) | Medium | Muted Color.



---

## 3. Component Styles

Consistency in these elements makes the site feel "real" to visitors.

### **The "App Card"**

Instead of a simple button, use a card to showcase your products:

* **Background:** `#FFFFFF`
* **Border:** `1px solid #E5E7EB`
* **Corner Radius:** `12px` (Soft but professional)
* **Shadow:** `0 4px 6px -1px rgb(0 0 0 / 0.1)` (Very subtle)

### **Buttons**

* **Primary:** Solid `#1A1A1A` with White text. `8px` corner radius.
* **Secondary:** White background, `1px` border of `#1A1A1A`.

---

## 4. Layout & Grid

Use a **Single Column Center-Aligned** layout for the home page, but transition to a **2-Column Grid** for your app list to show growth.

* **Max Width:** `800px` (Keeps text from stretching too far, which looks amateur).
* **Section Spacing:** Use `80px` of vertical space between the Hero (Logo), the Apps, and the About/Contact sections. **White space is what makes a site look expensive.**

---

## 5. Visual Signature: "The Scout Line"

Since your logo features a scout dog with circuit lines, use a **subtle 1px "Circuit Line"** as a horizontal divider between sections instead of a solid line. This ties the "AI" theme into the UI without adding "weird stuff."

---

## Implementation Example (CSS)

If you are coding this yourself, here is a quick "cheat sheet" of variables:

```css
:root {
  --color-primary: #1a1a1a;
  --color-accent: #00a3ff;
  --color-bg: #f4f7f9;
  --color-text: #4b5563;
  --radius: 12px;
  --font-main: 'Inter', system-ui, sans-serif;
}

body {
  background-color: var(--color-bg);
  font-family: var(--font-main);
  color: var(--color-text);
  line-height: 1.6;
}

.card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: var(--radius);
  padding: 2rem;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-4px); /* Adds a "premium" interactive feel */
}
