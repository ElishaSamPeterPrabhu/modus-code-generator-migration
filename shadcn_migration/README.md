# shadcn/ui to Modus Migration System

Complete migration system for transitioning from shadcn/ui components to Modus V2 web components.

## Overview

shadcn/ui is a collection of React components built on Radix UI primitives with Tailwind CSS styling. This system helps migrate to **Modus V2 web components** (Trimble design system).

## Directory Structure

- `mapping/` - Component mappings between shadcn and Modus
- `md_prompts/` - Phase-specific guidance (analyze, migrate, verify, log, workflow)
- `TOOL_DESCRIPTION.md` - n8n MCP tool integration details
- `README.md` - This file

## Component Mappings

**42 shadcn components** have direct Modus equivalents (Button, Input, Card, Alert, etc.)

**Components without mapping**: Command, Carousel, Form, ScrollArea, AspectRatio, InputOTP, ToggleGroup

## Migration Workflow

1. **Analyze** - Scan codebase, identify components, assess complexity
2. **Migrate** - Transform components, convert Tailwind, map properties
3. **Verify** - Validate mappings, test functionality
4. **Log** - Generate summary reports and action items

## Key Challenges

- **Tailwind CSS** - Convert utility classes to Modus tokens/CSS
- **Radix UI** - Map primitives to Modus equivalents
- **Composition** - Handle sub-component patterns
- **Customization** - Assess project-specific modifications

## Getting Started

1. Review component mappings
2. Read workflow documentation
3. Run analysis on your codebase
4. Migrate incrementally
5. Test continuously

## Tool Integration

Designed for **n8n MCP tool** integration. See `TOOL_DESCRIPTION.md`.

## Best Practices

- Start with simple components
- Test after each migration
- Document Tailwind conversions
- Maintain consistency
- Preserve accessibility
