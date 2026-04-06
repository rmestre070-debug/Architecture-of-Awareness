# Contributing to Scholarly Prompt Studio

Thanks for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch:
   git checkout -b feature/my-feature
3. Commit your changes:
   git commit -m "Add my feature"
4. Push to your branch:
   git push origin feature/my-feature
5. Open a Pull Request

## Code Style

- Keep functions small and modular
- Use descriptive names
- Avoid unnecessary complexity
- Follow the existing architecture

## Plugins

Plugins must define:

def register(engine):
    # modify engine.modes, engine.suggestions, etc.

## Issues

If you find a bug, open an issue with:
- steps to reproduce
- expected behavior
- actual behavior
- screenshots if possible