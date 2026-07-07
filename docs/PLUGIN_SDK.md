# Plugin SDK Draft

AIMS plugins extend the platform without modifying the core.

## Plugin Types

- ParserPlugin
- ValidatorPlugin
- ExporterPlugin
- AnalyzerPlugin
- StoragePlugin

## Parser Contract

```python
class ParserPlugin:
    def supports(self, path: str) -> bool: ...
    def parse(self, path: str) -> ADFDocument: ...
```

## Rule

Plugins must communicate through ADF and public contracts.
