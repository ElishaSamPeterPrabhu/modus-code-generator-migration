#!/usr/bin/env python3
"""
Test script for Shadcn to Modus Migration MCP Server

This script tests all MCP tools to ensure they're working correctly.
"""

import json
import sys
import os

# Add the current directory to path to import the server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shadcn_mcp_server_local import (
    get_shadcn_component_mapping,
    get_migration_workflow_guide,
    get_migration_phase_guide,
    get_modus_component_data,
    get_shadcn_to_modus_migration_data,
    list_all_modus_components
)


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_get_shadcn_component_mapping():
    """Test getting shadcn component mappings"""
    print("Testing: get_shadcn_component_mapping()")
    print_separator()
    
    result = get_shadcn_component_mapping()
    data = json.loads(result)
    
    if "error" in data:
        print(f"❌ FAILED: {data['error']}")
        return False
    
    print(f"✅ SUCCESS: Retrieved {len(data.get('shadcn_to_modus', {}))} shadcn → Modus mappings")
    print(f"✅ SUCCESS: Retrieved {len(data.get('modus_to_shadcn', {}))} Modus → shadcn mappings")
    
    # Show a few examples
    print("\nSample mappings:")
    for i, (shadcn, modus) in enumerate(list(data.get('shadcn_to_modus', {}).items())[:5]):
        print(f"  {shadcn} → {modus}")
    
    return True


def test_get_migration_workflow_guide():
    """Test getting migration workflow guide"""
    print("Testing: get_migration_workflow_guide()")
    print_separator()
    
    result = get_migration_workflow_guide()
    
    if isinstance(result, str) and result.startswith("{"):
        data = json.loads(result)
        if "error" in data:
            print(f"❌ FAILED: {data['error']}")
            return False
    
    if len(result) > 100:
        print(f"✅ SUCCESS: Retrieved workflow guide ({len(result)} characters)")
        print(f"\nFirst 200 characters:")
        print(result[:200] + "...")
        return True
    else:
        print(f"❌ FAILED: Workflow guide too short ({len(result)} characters)")
        return False


def test_get_migration_phase_guide():
    """Test getting phase-specific guides"""
    print("Testing: get_migration_phase_guide()")
    print_separator()
    
    phases = ["analyze", "migrate", "verify", "log"]
    all_passed = True
    
    for phase in phases:
        result = get_migration_phase_guide(phase)
        
        if isinstance(result, str) and result.startswith("{"):
            data = json.loads(result)
            if "error" in data:
                print(f"❌ FAILED ({phase}): {data['error']}")
                all_passed = False
                continue
        
        if len(result) > 100:
            print(f"✅ SUCCESS ({phase}): Retrieved guide ({len(result)} characters)")
        else:
            print(f"❌ FAILED ({phase}): Guide too short ({len(result)} characters)")
            all_passed = False
    
    # Test invalid phase
    result = get_migration_phase_guide("invalid")
    data = json.loads(result)
    if "error" in data:
        print(f"✅ SUCCESS (validation): Correctly rejected invalid phase")
    else:
        print(f"❌ FAILED (validation): Should reject invalid phase")
        all_passed = False
    
    return all_passed


def test_get_modus_component_data():
    """Test getting Modus component data"""
    print("Testing: get_modus_component_data()")
    print_separator()
    
    # Test with valid component
    result = get_modus_component_data("button")
    data = json.loads(result)
    
    if "error" in data:
        print(f"❌ FAILED (button): {data['error']}")
        return False
    
    print(f"✅ SUCCESS (button): Retrieved component data")
    print(f"  - Tag: {data.get('tag_name')}")
    print(f"  - Props: {len(data.get('props', []))}")
    print(f"  - Events: {len(data.get('events', []))}")
    print(f"  - Slots: {len(data.get('slots', []))}")
    
    # Test with modus-wc- prefix
    result = get_modus_component_data("modus-wc-text-input")
    data = json.loads(result)
    
    if "error" in data:
        print(f"❌ FAILED (text-input): {data['error']}")
        return False
    
    print(f"✅ SUCCESS (text-input): Retrieved component data with prefix")
    
    # Test invalid component
    result = get_modus_component_data("invalid-component-xyz")
    data = json.loads(result)
    
    if "error" in data and "available_components" in data:
        print(f"✅ SUCCESS (validation): Correctly rejected invalid component")
    else:
        print(f"❌ FAILED (validation): Should reject invalid component")
        return False
    
    return True


def test_get_shadcn_to_modus_migration_data():
    """Test getting migration data for specific components"""
    print("Testing: get_shadcn_to_modus_migration_data()")
    print_separator()
    
    # Test valid component
    result = get_shadcn_to_modus_migration_data("Button")
    data = json.loads(result)
    
    if "error" in data:
        print(f"❌ FAILED (Button): {data['error']}")
        return False
    
    print(f"✅ SUCCESS (Button): Retrieved migration data")
    print(f"  - shadcn: {data.get('shadcn_component')}")
    print(f"  - Modus: {data.get('modus_tag')}")
    print(f"  - Props: {len(data.get('modus_data', {}).get('props', []))}")
    
    # Test component without mapping
    result = get_shadcn_to_modus_migration_data("Command")
    data = json.loads(result)
    
    if data.get('modus_equivalent') is None:
        print(f"✅ SUCCESS (Command): Correctly identified no mapping")
        print(f"  - Note: {data.get('note')}")
    else:
        print(f"❌ FAILED (Command): Should have no mapping")
        return False
    
    return True


def test_list_all_modus_components():
    """Test listing all Modus components"""
    print("Testing: list_all_modus_components()")
    print_separator()
    
    result = list_all_modus_components()
    data = json.loads(result)
    
    if "error" in data:
        print(f"❌ FAILED: {data['error']}")
        return False
    
    total = data.get('total_components', 0)
    components = data.get('components', [])
    
    print(f"✅ SUCCESS: Retrieved {total} components")
    
    # Show a few examples
    print("\nSample components:")
    for component in components[:5]:
        print(f"  - {component['name']} ({component['tag']})")
        print(f"    Props: {component['props_count']}, Events: {component['events_count']}")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("Shadcn to Modus Migration MCP Server - Test Suite")
    print("=" * 80)
    
    tests = [
        ("Component Mapping", test_get_shadcn_component_mapping),
        ("Workflow Guide", test_get_migration_workflow_guide),
        ("Phase Guides", test_get_migration_phase_guide),
        ("Modus Component Data", test_get_modus_component_data),
        ("Migration Data", test_get_shadcn_to_modus_migration_data),
        ("List Components", test_list_all_modus_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ EXCEPTION in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_separator()
    print("TEST SUMMARY")
    print_separator()
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! MCP server is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
