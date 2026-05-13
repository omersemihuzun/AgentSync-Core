---
name: Nexus Autonomous Command
colors:
  surface: '#0e1416'
  surface-dim: '#0e1416'
  surface-bright: '#343a3c'
  surface-container-lowest: '#090f11'
  surface-container-low: '#171c1f'
  surface-container: '#1b2023'
  surface-container-high: '#252b2d'
  surface-container-highest: '#303638'
  on-surface: '#dee3e6'
  on-surface-variant: '#bcc9ce'
  inverse-surface: '#dee3e6'
  inverse-on-surface: '#2b3134'
  outline: '#869398'
  outline-variant: '#3d494d'
  surface-tint: '#4cd6fb'
  primary: '#4cd6fb'
  on-primary: '#003642'
  primary-container: '#00b4d8'
  on-primary-container: '#00414f'
  inverse-primary: '#00677d'
  secondary: '#bbc6e2'
  on-secondary: '#263046'
  secondary-container: '#3e4960'
  on-secondary-container: '#adb8d3'
  tertiary: '#ffb77d'
  on-tertiary: '#4d2600'
  tertiary-container: '#eb8f3b'
  on-tertiary-container: '#5d2f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#b3ebff'
  primary-fixed-dim: '#4cd6fb'
  on-primary-fixed: '#001f27'
  on-primary-fixed-variant: '#004e5f'
  secondary-fixed: '#d7e2ff'
  secondary-fixed-dim: '#bbc6e2'
  on-secondary-fixed: '#101b30'
  on-secondary-fixed-variant: '#3c475d'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#0e1416'
  on-background: '#dee3e6'
  surface-variant: '#303638'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 24px
  gutter: 16px
  stack-sm: 4px
  stack-md: 12px
  stack-lg: 24px
---

## Brand & Style

The design system is engineered for high-stakes autonomous SME management, where precision and clarity are paramount. The brand personality is authoritative yet innovative, evoking the feeling of a futuristic mission control center. It targets tech-savvy business owners and operations managers who require real-time oversight of AI-driven workflows.

The visual style is **Glassmorphic Modern**, characterized by semi-transparent surfaces, high-tech neon accents, and a deep sense of layered depth. It prioritizes data density without sacrificing legibility, utilizing crisp lines and subtle gradients to guide the user's eye through complex information hierarchies.

## Colors

The palette is anchored in a professional dark-mode spectrum to reduce eye strain during prolonged monitoring. 

- **Primary Background (#0D1B2A):** Used for the base canvas of the application.
- **Secondary Background (#1B263B):** Reserved for sidebars, navigation rails, and card containers to create structural separation.
- **Accent (#00B4D8):** A vibrant cyan used for primary actions, active states, and data highlights.
- **Text (#E0E1DD):** An off-white chosen to provide high contrast against navy backgrounds without the harshness of pure white.
- **Semantic Status:** 
    - **Critical/High:** A vivid Red/Orange for immediate attention.
    - **Normal/Manual:** A golden Yellow for items requiring human intervention.
    - **Low/Approve:** A bright Green for autonomous successes and healthy metrics.

## Typography

The design system employs a dual-font strategy. **Outfit** is used for headlines and display text to provide a geometric, modern flair. **Inter** is used for body copy and UI labels to ensure maximum readability and a functional, systematic feel. 

For technical data points or AI-generated logs, a monospaced font (JetBrains Mono) is recommended to reinforce the "data-driven" aesthetic. On mobile devices, `display-lg` should scale down to 32px to maintain layout integrity.

## Layout & Spacing

This design system utilizes a **12-column fluid grid** for desktop, collapsing to 4 columns for mobile. 

- **Grid:** 24px margins with 16px gutters.
- **Rhythm:** An 8px linear scale governs all spacing.
- **Reflow:** On tablet, sidebars collapse into a slim icon-only rail to prioritize the dashboard real estate. 
- **Density:** High-density layouts are preferred for data tables, while "Hero" dashboard cards utilize more generous padding (32px) to emphasize key KPIs.

## Elevation & Depth

Depth in this system is achieved through **Glassmorphism** and tonal layering rather than traditional heavy shadows.

- **Surface Level 0:** The Deep Navy background (#0D1B2A).
- **Surface Level 1 (Cards):** Dark Navy (#1B263B) with a 60% opacity, a 16px backdrop blur, and a 1px inner border (#FFFFFF10).
- **Surface Level 2 (Modals/Popovers):** Dark Navy with 80% opacity, 32px backdrop blur, and a subtle outer glow using the primary accent color at 5% opacity.
- **Visual Cues:** Interactive elements use a "glow" effect on hover, where the inner border brightness increases from 10% to 30%.

## Shapes

The shape language is "Rounded," striking a balance between approachable software and professional hardware interfaces. 

- **Buttons & Inputs:** 0.5rem (8px) radius.
- **Cards & Modals:** 1rem (16px) radius for a distinct containerized feel.
- **Status Badges:** Fully pill-shaped (rounded-full) to differentiate them from interactive buttons.
- **Data Tables:** Outer corners are rounded at 8px, while internal cell dividers remain sharp to maintain a "grid" feel.

## Components

- **Glass Cards:** Feature a subtle top-to-bottom gradient (Secondary Background to Transparent) and a 1px stroke.
- **Buttons:** 
    - *Primary:* Solid Cyan with black text for maximum contrast.
    - *Secondary:* Ghost style with Cyan border and text.
    - *Hover:* Scale 1.02x with a soft cyan outer glow.
- **Data Tables:** Crisp, borderless rows with a subtle separator line (#FFFFFF08). Zebra-striping is avoided; instead, use a high-contrast hover state on rows.
- **Status Badges:** Use a "dot + label" format. The dot should have a CSS "pulse" animation if the status is "Critical."
- **Inputs:** Dark Navy background with a 1px border. On focus, the border transitions to Cyan and the field gains a subtle inner glow.
- **Animations:** 
    - Page transitions use a 300ms fade-in with a 10px Y-axis slide.
    - Hover states use a 150ms "Ease-Out" scale effect.