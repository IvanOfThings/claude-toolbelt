# Mobile-First UI Development

Applications are used primarily from mobile devices. Every UI change must be designed and validated mobile-first.

## Rules

- **Default viewport target**: 390px width (iPhone SE). Design at this width first.
- **Progressive enhancement**: use responsive breakpoints (`sm:`, `lg:`) only to enhance on larger screens — never to fix broken mobile layouts.
- **Touch targets**: minimum 44 × 44 px for all interactive elements.
- **No horizontal overflow**: the page must never scroll horizontally on mobile.
- **Validate before declaring done**: resize the browser to 390px and verify the layout before marking a UI task complete.

## Layout principles

Stack content vertically by default. Horizontal layouts are the exception, only introduced at larger breakpoints. Prioritise vertical space efficiency — users scroll, not pan.

## Typography

Base font size must remain readable at mobile width without pinch-to-zoom. Minimum body text: 14px (16px preferred). Never use `font-size` below 12px for any visible text.
