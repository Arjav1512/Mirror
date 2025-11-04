# 🎨 Mirror Design System - Consistency Guide

## ✅ All Design Inconsistencies Fixed

Your entire application now follows a unified, consistent design system.

---

## 📐 Design Tokens

### **Spacing Scale**
```
xs:  0.25rem (4px)
sm:  0.5rem  (8px)
md:  1rem    (16px)
lg:  1.5rem  (24px)
xl:  2rem    (32px)
2xl: 3rem    (48px)
```

### **Border Radius**
```
Small (inputs, code):  8px
Medium (cards):        12px
Large (modals):        16px
Full (circles):        9999px
```

### **Shadows**
```
Card Shadow:     0 4px 6px rgba(0, 0, 0, 0.3)
Hover Shadow:    0 6px 8px rgba(0, 0, 0, 0.4)
Button Shadow:   0 4px 6px rgba(124, 58, 237, 0.3)
```

### **Typography**
```
Font Family: Inter
Headings: 700 (bold)
Body:     400 (regular)
Labels:   600 (semibold)
Buttons:  600 (semibold)
```

---

## 🎨 Color System

### **Backgrounds**
- **App Background**: `#0f172a` (slate-950)
- **Card Background**: `#1e293b` (slate-800)
- **Sidebar**: `#1e293b` (slate-800)
- **Input Background**: `#1e293b` (slate-800)
- **Hover Background**: `#334155` (slate-700)

### **Text**
- **Primary (Headings)**: `#f1f5f9` (slate-100)
- **Secondary (Body)**: `#cbd5e1` (slate-300)
- **Tertiary (Muted)**: `#94a3b8` (slate-400)
- **Placeholder**: `#64748b` (slate-500)

### **Borders**
- **Default**: `#334155` (slate-700)
- **Input**: `#475569` (slate-600)
- **Focus**: `#7c3aed` (violet-600)

### **Accents**
- **Primary**: `#7c3aed` (violet-600)
- **Primary Hover**: `#8b5cf6` (violet-500)
- **Active**: `#a78bfa` (violet-400)
- **Success**: `#10b981` (emerald-500)
- **Error**: `#ef4444` (red-500)
- **Warning**: `#f59e0b` (amber-500)
- **Info**: `#3b82f6` (blue-500)

---

## 📦 Component Specifications

### **1. Cards**
```css
Background: #1e293b
Border: 1px solid #334155
Border Radius: 12px
Padding: 1.5rem (24px)
Shadow: 0 4px 6px rgba(0, 0, 0, 0.3)
Margin: 1rem 0
```

### **2. Buttons (Primary)**
```css
Background: #7c3aed
Hover: #8b5cf6
Color: white
Border Radius: 8px
Padding: 0.75rem 2rem
Font Weight: 600
Shadow: 0 4px 6px rgba(124, 58, 237, 0.3)
```

### **3. Buttons (Secondary)**
```css
Background: #334155
Hover: #475569
Color: #e2e8f0
Border: 1px solid #475569
Border Radius: 8px
```

### **4. Text Inputs**
```css
Background: #1e293b
Border: 1px solid #475569
Border Radius: 8px
Padding: 0.75rem 1rem
Color: #e2e8f0
Focus Border: #7c3aed
Focus Ring: 0 0 0 3px rgba(124, 58, 237, 0.2)
```

### **5. Text Area**
```css
Background: #1e293b
Border: 1px solid #475569
Border Radius: 8px
Padding: 0.75rem 1rem
Min Height: 200px
Line Height: 1.6
Color: #e2e8f0
```

### **6. Tabs**
```css
Border Bottom: 2px solid #334155
Tab Color: #94a3b8
Tab Hover: #a78bfa
Active Color: #a78bfa
Active Border: 2px solid #7c3aed
Padding: 12px 24px
```

### **7. Sidebar**
```css
Background: #1e293b
Border Right: 1px solid #334155
Padding Top: 2rem
```

### **8. Metrics**
```css
Value Size: 2.5rem
Value Color: #f1f5f9
Label Size: 0.875rem
Label Color: #94a3b8
Font Weight: 700/600
```

### **9. Alert Messages**

**Success:**
```css
Background: #064e3b
Border Left: 4px solid #10b981
Color: #d1fae5
```

**Error:**
```css
Background: #450a0a
Border Left: 4px solid #ef4444
Color: #fecaca
```

**Warning:**
```css
Background: #422006
Border Left: 4px solid #f59e0b
Color: #fde68a
```

**Info:**
```css
Background: #1e3a8a
Border Left: 4px solid #3b82f6
Color: #dbeafe
```

### **10. Sentiment Cards**
```css
Background: #1e293b
Border: 1px solid #334155
Border Left: 4px solid (dynamic color)
Border Radius: 12px
Padding: 1.5rem
Shadow: 0 4px 6px rgba(0, 0, 0, 0.3)
```

### **11. Bias Alerts**
```css
Background: #422006
Border Left: 4px solid #fb923c
Border Radius: 8px
Padding: 1rem 1.5rem
Title Color: #fbbf24
Text Color: #fcd34d
```

### **12. Forms**
```css
Background: #1e293b
Border: 1px solid #334155
Border Radius: 12px
Padding: 1.5rem
```

### **13. File Uploader**
```css
Background: #1e293b
Border: 2px dashed #475569
Hover Border: #7c3aed
Border Radius: 12px
Padding: 2rem
```

### **14. Charts (Plotly)**
```css
Border Radius: 12px
Overflow: hidden
Background: transparent
```

### **15. Code Blocks**
```css
Background: #0f172a
Color: #a78bfa
Padding: 0.2rem 0.4rem
Border Radius: 4px
Font: Monaco, Courier New, monospace
```

### **16. Dividers**
```css
Border Top: 1px solid #334155
Margin: 2.5rem 0
```

---

## 🎯 Consistency Rules

### **Always Use:**
1. ✅ Same border radius for similar components
2. ✅ Same shadow depth for cards
3. ✅ Same spacing scale throughout
4. ✅ Same color palette (no random colors)
5. ✅ Same font family (Inter)
6. ✅ Same border colors
7. ✅ Same hover states
8. ✅ Same focus states

### **Never Mix:**
1. ❌ Different border radius on similar elements
2. ❌ Different shadow styles
3. ❌ Different padding values (use scale)
4. ❌ Different text colors for same purpose
5. ❌ Different border styles
6. ❌ Different fonts
7. ❌ Different animation speeds

---

## 📱 Component Usage

### **Landing Page (React)**
All components follow:
- Consistent dark backgrounds
- Same border radius (8px buttons, 12px cards)
- Same shadows
- Same violet accent color
- Same spacing

### **Streamlit App**
All components follow:
- Unified card system (12px radius)
- Consistent input styling (8px radius)
- Unified button styling
- Consistent tabs
- Unified alert system
- Consistent shadows

---

## 🔧 Fixed Inconsistencies

### **Before:**
- ❌ Mixed border radius (0px, 8px, 12px, 16px randomly)
- ❌ Inconsistent shadows (some elements had none)
- ❌ Different padding values
- ❌ Mixed background colors
- ❌ Inconsistent text colors
- ❌ Random border styles
- ❌ Inconsistent spacing

### **After:**
- ✅ Unified border radius system
- ✅ Consistent shadow depth
- ✅ Spacing scale applied
- ✅ Single background palette
- ✅ Hierarchical text colors
- ✅ Consistent border system
- ✅ Systematic spacing

---

## 🎨 Visual Hierarchy

### **Level 1: Primary Elements**
- Main headers: `#f1f5f9`, 700 weight
- Primary buttons: `#7c3aed` with shadow
- Key metrics: Large, bold

### **Level 2: Secondary Elements**
- Subheaders: `#cbd5e1`, 600 weight
- Body text: `#cbd5e1`, 400 weight
- Secondary buttons: `#334155`

### **Level 3: Tertiary Elements**
- Labels: `#94a3b8`, 600 weight
- Muted text: `#94a3b8`, 400 weight
- Placeholders: `#64748b`

### **Level 4: Borders & Dividers**
- Default borders: `#334155`
- Input borders: `#475569`
- Dividers: `#334155`

---

## 📊 Spacing Guidelines

### **Component Spacing**
```
Between cards:     1rem  (16px)
Inside cards:      1.5rem (24px)
Between sections:  2rem  (32px)
Page padding:      2rem  (32px)
Button padding:    0.75rem 2rem
Input padding:     0.75rem 1rem
```

### **Typography Spacing**
```
Heading margin bottom: 1rem
Paragraph margin:      1rem
Label margin bottom:   0.5rem
List item spacing:     0.5rem
```

---

## ✅ Quality Checklist

When adding new components, ensure:

- [ ] Border radius matches similar components
- [ ] Shadow depth is consistent
- [ ] Spacing follows the scale
- [ ] Colors are from the palette
- [ ] Text hierarchy is correct
- [ ] Hover states are defined
- [ ] Focus states are visible
- [ ] Transitions are smooth (0.2s)
- [ ] Font is Inter
- [ ] Background color is correct

---

## 🚀 Implementation Status

### **Frontend (React)** ✅
- Hero: Consistent
- HowItWorks: Consistent
- SignupForm: Consistent
- Footer: Consistent
- All components: Unified

### **Backend (Streamlit)** ✅
- Login page: Consistent
- Main interface: Consistent
- All cards: Unified
- All inputs: Unified
- All buttons: Unified
- All tabs: Unified
- All alerts: Unified
- All charts: Consistent

---

## 🎯 Result

**Your Mirror application now has:**
- ✅ **100% consistent styling** across all components
- ✅ **Unified color palette** with no random colors
- ✅ **Systematic spacing** using defined scale
- ✅ **Consistent shadows** for depth
- ✅ **Unified typography** with clear hierarchy
- ✅ **Professional appearance** throughout
- ✅ **Predictable user experience**

**All design inconsistencies are now fixed!** 🎨✨
