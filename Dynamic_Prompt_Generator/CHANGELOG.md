# Changelog  
All notable changes to **Scholarly Prompt Studio** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to **Semantic Versioning**.

---

## [2.0.0] — 2026-04-06  
### Added
- Complete architectural rebuild of `scholarly_studio.py`  
- Stable, Android‑safe brain‑tint system with retry‑until‑ready logic  
- Cleaned and modularized controller structure  
- Improved kernel indicator formatting  
- More robust plugin loader with directory validation  
- Unified suggestion‑engine binding logic  
- Clearer separation of UI, engine, and plugin responsibilities  
- Enhanced readability and maintainability across the entire codebase  

### Changed
- Refactored awareness‑mode handling for clarity and extensibility  
- Reorganized lifecycle events for more predictable startup behavior  
- Improved error handling and fallback behavior  
- Simplified screen‑switching logic  
- Consolidated repeated code into helper methods  
- Cleaned up toast messaging and UX flow  

### Fixed
- Brain icon tint not applying due to KivyMD timing issues  
- Toolbar icon reference inconsistencies across Android builds  
- Occasional crashes during early UI initialization  
- Suggestion chip update inconsistencies  

---

## [1.7.0] — 2026-04-05  
### Added
- Brain pulse animation  
- Mode‑aware tint animation (initial implementation)  
- Kernel pulse feedback  
- Mode badge updates  
- Expanded plugin auto‑loading  

### Changed
- Improved suggestion chip styling  
- Updated screen transitions  
- Cleaned up KV structure  

### Fixed
- Chip visibility issues  
- Indentation and layout inconsistencies  

---

## [1.6.0] — 2026-04-04  
### Added
- Awareness mode dropdown  
- Plugin‑defined modes  
- Kernel indicator  
- History viewer improvements  

### Changed
- Refined Generate/Refine pipelines  
- Improved output handling  

---

## [1.5.0] — 2026-04-03  
### Added
- Full UI rebuild with modernized layout  
- Domain‑aware suggestion engine  
- Cleaned chip creation logic  

---

## [1.0.0] — 2026-03-30  
### Added
- Initial release of Scholarly Prompt Studio  
- Generate, Refine, Output, History screens  
- Basic suggestion engine  
- Plugin architecture foundation  
- Splash screen and navigation bar