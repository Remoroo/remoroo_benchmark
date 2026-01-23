"""Data pipeline with callback hell that needs refactoring.

This code simulates a data processing pipeline with multiple async steps.
Currently implemented with nested callbacks (callback hell pattern).

The pipeline:
1. fetch_data - Get raw data from source
2. validate_data - Check data integrity
3. transform_data - Apply transformations
4. enrich_data - Add metadata
5. save_data - Persist results

GOAL: Refactor to use async/await pattern while keeping same behavior.
The async version should be much more readable.

RULES:
- Each step must remain "async" (use asyncio.sleep to simulate I/O)
- Error handling must be preserved
- The test at the bottom must still pass
"""

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PipelineResult:
    success: bool
    data: Any
    error: Optional[str] = None
    steps_completed: int = 0


# Simulated async operations using callbacks
# THIS IS THE CODE THAT NEEDS REFACTORING!

def fetch_data_callback(source: str, callback: Callable[[Optional[str], Optional[Dict]], None]):
    """Fetch data from source (simulated async with callback)."""
    async def _fetch():
        await asyncio.sleep(0.1)  # Simulate network delay
        if source == "invalid":
            callback("Source not found", None)
        else:
            callback(None, {"raw": f"data_from_{source}", "source": source})
    
    asyncio.create_task(_fetch())


def validate_data_callback(data: Dict, callback: Callable[[Optional[str], Optional[Dict]], None]):
    """Validate data integrity (simulated async with callback)."""
    async def _validate():
        await asyncio.sleep(0.05)  # Simulate processing
        if "raw" not in data:
            callback("Missing raw field", None)
        else:
            callback(None, {**data, "validated": True})
    
    asyncio.create_task(_validate())


def transform_data_callback(data: Dict, callback: Callable[[Optional[str], Optional[Dict]], None]):
    """Transform data (simulated async with callback)."""
    async def _transform():
        await asyncio.sleep(0.05)  # Simulate processing
        transformed = data["raw"].upper()
        callback(None, {**data, "transformed": transformed})
    
    asyncio.create_task(_transform())


def enrich_data_callback(data: Dict, callback: Callable[[Optional[str], Optional[Dict]], None]):
    """Enrich data with metadata (simulated async with callback)."""
    async def _enrich():
        await asyncio.sleep(0.05)  # Simulate API call
        callback(None, {**data, "enriched": True, "timestamp": time.time()})
    
    asyncio.create_task(_enrich())


def save_data_callback(data: Dict, callback: Callable[[Optional[str], Optional[Dict]], None]):
    """Save data to storage (simulated async with callback)."""
    async def _save():
        await asyncio.sleep(0.1)  # Simulate database write
        callback(None, {**data, "saved": True, "id": "record_123"})
    
    asyncio.create_task(_save())


# THE CALLBACK HELL - THIS NEEDS TO BE REFACTORED!

def run_pipeline_callbacks(source: str, final_callback: Callable[[PipelineResult], None]):
    """Run the full pipeline using callbacks.
    
    THIS IS CALLBACK HELL! Look at the nesting:
    
    fetch -> validate -> transform -> enrich -> save
    
    Each level adds more indentation and makes error handling harder.
    
    TODO: Refactor this to use async/await!
    
    The async version should look like:
        async def run_pipeline_async(source: str) -> PipelineResult:
            data = await fetch_data(source)
            data = await validate_data(data)
            data = await transform_data(data)
            data = await enrich_data(data)
            data = await save_data(data)
            return PipelineResult(success=True, data=data, steps_completed=5)
    """
    
    def on_fetch(error, data):
        if error:
            final_callback(PipelineResult(False, None, error, 0))
            return
        
        def on_validate(error, data):
            if error:
                final_callback(PipelineResult(False, None, error, 1))
                return
            
            def on_transform(error, data):
                if error:
                    final_callback(PipelineResult(False, None, error, 2))
                    return
                
                def on_enrich(error, data):
                    if error:
                        final_callback(PipelineResult(False, None, error, 3))
                        return
                    
                    def on_save(error, data):
                        if error:
                            final_callback(PipelineResult(False, None, error, 4))
                            return
                        
                        # Finally done!
                        final_callback(PipelineResult(True, data, None, 5))
                    
                    save_data_callback(data, on_save)
                
                enrich_data_callback(data, on_enrich)
            
            transform_data_callback(data, on_transform)
        
        validate_data_callback(data, on_validate)
    
    fetch_data_callback(source, on_fetch)


# Async versions that SHOULD be implemented
# Currently these are stubs that need implementation

async def fetch_data(source: str) -> Dict:
    """TODO: Implement async version of fetch_data_callback."""
    raise NotImplementedError("Implement this async function!")


async def validate_data(data: Dict) -> Dict:
    """TODO: Implement async version of validate_data_callback."""
    raise NotImplementedError("Implement this async function!")


async def transform_data(data: Dict) -> Dict:
    """TODO: Implement async version of transform_data_callback."""
    raise NotImplementedError("Implement this async function!")


async def enrich_data(data: Dict) -> Dict:
    """TODO: Implement async version of enrich_data_callback."""
    raise NotImplementedError("Implement this async function!")


async def save_data(data: Dict) -> Dict:
    """TODO: Implement async version of save_data_callback."""
    raise NotImplementedError("Implement this async function!")


async def run_pipeline_async(source: str) -> PipelineResult:
    """TODO: Implement the async pipeline using the async functions above.
    
    This should be clean and readable, unlike the callback version!
    
    Handle errors appropriately and track steps_completed.
    """
    raise NotImplementedError("Implement this async pipeline!")


# Test runner

async def test_pipeline():
    """Test both callback and async versions of the pipeline."""
    results = []
    
    # Test 1: Callback version with valid source
    print("Test 1: Callback pipeline with valid source")
    callback_result = None
    
    def capture_result(result):
        nonlocal callback_result
        callback_result = result
    
    run_pipeline_callbacks("test_source", capture_result)
    await asyncio.sleep(0.5)  # Wait for callbacks
    
    print(f"  Result: success={callback_result.success}, steps={callback_result.steps_completed}")
    results.append(("callback_valid", callback_result.success and callback_result.steps_completed == 5))
    
    # Test 2: Callback version with invalid source
    print("\nTest 2: Callback pipeline with invalid source")
    run_pipeline_callbacks("invalid", capture_result)
    await asyncio.sleep(0.2)
    
    print(f"  Result: success={callback_result.success}, error={callback_result.error}")
    results.append(("callback_invalid", not callback_result.success and callback_result.error is not None))
    
    # Test 3: Async version with valid source
    print("\nTest 3: Async pipeline with valid source")
    try:
        async_result = await run_pipeline_async("test_source")
        print(f"  Result: success={async_result.success}, steps={async_result.steps_completed}")
        results.append(("async_valid", async_result.success and async_result.steps_completed == 5))
        
        # Verify data integrity
        if async_result.data:
            has_all_fields = all(k in async_result.data for k in ["raw", "validated", "transformed", "enriched", "saved"])
            results.append(("async_data_complete", has_all_fields))
        else:
            results.append(("async_data_complete", False))
    except NotImplementedError:
        print("  SKIPPED: Async pipeline not implemented yet")
        results.append(("async_valid", False))
        results.append(("async_data_complete", False))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("async_valid", False))
        results.append(("async_data_complete", False))
    
    # Test 4: Async version with invalid source
    print("\nTest 4: Async pipeline with invalid source")
    try:
        async_result = await run_pipeline_async("invalid")
        print(f"  Result: success={async_result.success}, error={async_result.error}")
        results.append(("async_invalid", not async_result.success and async_result.error is not None))
    except NotImplementedError:
        print("  SKIPPED: Async pipeline not implemented yet")
        results.append(("async_invalid", False))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("async_invalid", False))
    
    return results


async def main():
    """Run tests and report results."""
    print("=" * 60)
    print("DATA PIPELINE REFACTORING TEST")
    print("=" * 60)
    print()
    
    results = await test_pipeline()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    passed = 0
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {name}")
        if success:
            passed += 1
    
    refactor_complete = (passed == len(results))
    
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"refactor_complete: {refactor_complete}")
    
    if refactor_complete:
        print("\nSUCCESS: Async refactoring complete!")
    else:
        print("\nFAILED: Async pipeline needs implementation")


if __name__ == "__main__":
    asyncio.run(main())

